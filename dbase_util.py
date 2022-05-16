import pymongo
from bson import objectid
import RAKE as rake

secondary_kwrds = 20
pk_amount = ck_amount = secondary_kwrds  # post keyword amount, comment keyword amount


def forum(name, desc):
    forum = {"_id": None,
             "name": name,
             "description": desc,
             "desc_kwrds": [kwrd[0] for kwrd in rake_obj.run(name + ". " + desc)],
             "post_kwrds": list(),
             "cmnt_kwrds": list(),
             "users": list(),
             "user_count": 0,
             "posts": list()}
    return forum


def post(title, text, user):
    post = {"user": user, "title": title, "text": text, "img_path": None, "comments": list()}
    return post


def comment(text, user):
    comment = {"user": user, "text": text, "img_path": None}
    return comment


def user(uname, pswrd):
    user = {"uname": uname, "password": pswrd, "forums": None}
    return user


def add_forum(forum):
    forum["_id"] = forum_db.find_one_and_update({"next_forum_id": {"$exists": True}},
                                                {"$inc": {"next_forum_id": 1}})["next_forum_id"]
    forum_db.insert_one(forum)


def add_post(post, forum_id):
    post_id = post_db.insert_one(post).inserted_id
    rake_data = post["title"] + ". " + post["text"]
    post_kwrds = rake_obj.run(rake_data)[:5]
    post_kwrds = [kwrd[0] for kwrd in post_kwrds]
    update_dict = {"$push": {"posts": post_id, "post_kwrds": {"$each": post_kwrds, "$slice": -pk_amount}}}
    if not forum_db.find_one({"_id": forum_id, "users": post["user"]}):
        update_dict["$push"]["users"] = post["user"]
        update_dict["$inc"] = {}
        update_dict["$inc"]["user_count"] = 1
    forum_db.update_one({"_id": forum_id}, update_dict)


def add_comment(comment, post_id, forum_id):
    insert_res = cmnt_db.insert_one(comment)
    rake_data = comment["text"]
    cmnt_kwrds = rake_obj.run(rake_data)[:5]
    cmnt_kwrds = [kwrd[0] for kwrd in cmnt_kwrds]
    update_dict = {"$push": {"cmnt_kwrds": {"$each": cmnt_kwrds, "$slice": -ck_amount}}}
    post_db.update_one({"_id": objectid.ObjectId(post_id)}, {"$push": {"comments": insert_res.inserted_id}})
    if not forum_db.find_one({"_id": forum_id, "users": comment["user"]}):
        update_dict["$push"]["users"] = comment["user"]
        update_dict["$inc"] = {}
        update_dict["$inc"]["user_count"] = 1
    forum_db.update_one({"_id": forum_id}, update_dict)


def add_user(user):
    user_db.insert_one(user)


def get_forum_data(data, slc=None, text_sort=None, kwrd_sort=None, user_sort=False, forum_id=None):
    data_dict = {x: 1 for x in data}
    if "_id" not in data:
        data_dict["_id"] = 0
    if forum_id is not None:
        return forum_db.find_one({"_id": forum_id}, data_dict)
    find_dict = {"next_forum_id": {"$exists": False}}
    if text_sort:
        find_dict["name"] = {"$regex": text_sort, "$options": "i"}
    elif kwrd_sort:
        find_dict["$text"] = {"$search": kwrd_sort}
    forum_data = forum_db.find(find_dict, data_dict)
    if kwrd_sort:
        forum_data.sort([("score", {"$meta": "textScore"})])
    elif not text_sort:
        forum_data.sort([("_id", pymongo.DESCENDING)])
    if user_sort:
        forum_data.sort([("user_count", pymongo.DESCENDING)])
    forum_data = list(forum_data)
    if text_sort:
        forum_data.sort(key=lambda x: len(x["name"]))
    if slc:
        return forum_data[slc[0]:slc[1]]
    return forum_data


def get_post_data(data, forum_id=None, slc=None, post_id=None):
    data_dict = {x: 1 for x in data}
    if "_id" not in data:
        data_dict["_id"] = 0
    if slc is not None:
        post_ids = forum_db.find_one({"_id": forum_id})["posts"]
        all_data = list(post_db.find({"_id": {"$in": post_ids}}, data_dict))[slc[0]:slc[1]]
        for post_data in all_data:
            post_data["_id"] = str(post_data["_id"])
        return all_data
    elif post_id is not None:
        return post_db.find_one({"_id": objectid.ObjectId(post_id)}, data_dict)
    else:
        raise Exception("Invalid post data request")


def get_comment_data(data, post_id, slc):
    data_dict = {x: 1 for x in data}
    if "_id" not in data:
        data_dict["_id"] = 0
    comment_ids = post_db.find_one({"_id": objectid.ObjectId(post_id)})["comments"]
    return list(cmnt_db.find({"_id": {"$in": comment_ids}}, data_dict))[slc[0]:slc[1]]


def get_user_data(data, uname=None):
    data_dict = {x: 1 for x in data}
    if "_id" not in data:
        data_dict["_id"] = 0
    if uname:
        return user_db.find_one({"uname": uname}, data_dict)
    return list(user_db.find({}, data_dict).sort("uname", pymongo.ASCENDING))


def user_exists(uname, pswrd=None):
    srch = {"uname": uname}
    if pswrd:
        srch["password"] = pswrd
    return bool(user_db.find_one(srch))


def warn_user(uname, msg):
    user_db.update_one({"uname": uname}, {"$set": {"warning": msg}})


def ban_user(uname, msg, end_date):
    user_db.update_one({"uname": uname}, {"$set": {"ban": {"message": msg, "end_date": end_date}}})


def remove_user_data(uname, field):
    user_db.update_one({"uname": uname}, {"$unset": {field: ""}})


def remove_keyword(forum_id, kwrd):
    forum_db.update_one({"_id": forum_id}, {"$pull": {"kwrds": kwrd}})


def add_keyword(forum_id, kwrd):
    forum_db.update_one({"_id": forum_id}, {"$push": {"kwrds": kwrd}})


def find_similar_forum(name):
    kwrd_search = list(forum_db.find({"$text": {"$search": name}},
                                     {"_id": 0, "name": 1, "description": 1, "score": {"$meta": "textScore"}}
                                     ).sort([("score", pymongo.DESCENDING)]))
    if not kwrd_search:
        return None
    if kwrd_search[0]["score"] >= 4:
        del kwrd_search[0]["score"]
        return kwrd_search[0]
    else:
        return None


# def add_to_blacklist(uname):
#     user_db.update_one({"_id": "blacklist"}, {"$push": {"users": uname}})
#
#
# def check_in_blacklist(uname):
#     user_db.find_one({"_id": "blacklist", "users": uname})


client = pymongo.MongoClient("mongodb+srv://RonTheHuman:mongomyak2022@cluster0.6rgbh"
                             ".mongodb.net/Gibberish?retryWrites=true&w=majority")
dbase = client["Gibberish"]
forum_db = dbase["forums"]
post_db = dbase["posts"]
cmnt_db = dbase["comments"]
user_db = dbase["users"]
if not forum_db.find_one({}):
    print("creating new dbase")
    forum_db.insert_one({"next_forum_id": 0})
rake_obj = rake.Rake(rake.SmartStopList())
