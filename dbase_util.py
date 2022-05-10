import pymongo
from bson import objectid
import RAKE as rake


forum_template = \
    {"_id": None,
     "name": None,
     "description": None,
     "kwrds": list(),
     "users": [],
     "user_count": 0,
     "posts": list()}

post_template = \
    {"user": None,
     "title": None,
     "text": None,
     "img_path": None,
     "comments": list()}

comment_template = \
    {"user": None,
     "text": None,
     "img_path": None}

user_template = \
    {"uname": None,
     "password": None,
     "forums": None}


def forum(name, desc):
    forum = forum_template.copy()
    forum["name"] = name
    forum["description"] = desc
    forum["kwrds"].extend([kwrd[0] for kwrd in rake_obj.run(name)])
    desc_kwrds = rake_obj.run(desc)
    for kwrd in desc_kwrds:
        if kwrd[0] not in forum["kwrds"]:
            forum["kwrds"].append(kwrd[0])
    return forum


def add_forum(forum):
    forum["_id"] = forum_db.find_one_and_update({"next_forum_id": {"$exists": True}},
                                                {"$inc": {"next_forum_id": 1}})["next_forum_id"]
    forum_db.insert_one(forum)


def get_forum_data(data, slc=None, text_sort=None, kwrd_sort=None, user_sort=False, forum_id=None):
    data_dict = {x: 1 for x in data}
    if "_id" not in data:
        data_dict["_id"] = 0
    if forum_id:
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


def remove_keyword(forum_id, kwrd):
    forum_db.update_one({"_id": forum_id}, {"$pull": {"kwrds": kwrd}})


def add_keyword(forum_id, kwrd):
    forum_db.update_one({"_id": forum_id}, {"$push": {"kwrds": kwrd}})


def post(title, text, user):
    post = post_template.copy()
    post["title"] = title
    post["text"] = text
    post["user"] = user
    return post


def add_post(post, forum_id):
    post_id = post_db.insert_one(post).inserted_id
    update_dict = {"$push": {"posts": post_id}}
    if not forum_db.find_one({"_id": forum_id, "users": post["user"]}):
        update_dict["$push"]["users"] = post["user"]
        update_dict["$inc"] = {}
        update_dict["$inc"]["user_count"] = 1
    forum_db.update_one({"_id": forum_id}, update_dict)


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


def comment(text, user):
    comment = comment_template.copy()
    comment["user"] = user
    comment["text"] = text
    return comment


def add_comment(comment, post_id, forum_id):
    insert_res = cmnt_db.insert_one(comment)
    post_db.update_one({"_id": objectid.ObjectId(post_id)}, {"$push": {"comments": insert_res.inserted_id}})
    forum_db.update_one({"_id": forum_id, "users": {"$nin": [comment["user"]]}},
                        {"$push": {"users": comment["user"]}, "$inc": {"user_count": 1}})


def get_comment_data(data, post_id, slc):
    data_dict = {x: 1 for x in data}
    if "_id" not in data:
        data_dict["_id"] = 0
    comment_ids = post_db.find_one({"_id": objectid.ObjectId(post_id)})["comments"]
    return list(cmnt_db.find({"_id": {"$in": comment_ids}}, data_dict))[slc[0]:slc[1]]


def user(uname, pswrd):
    user = user_template.copy()
    user["uname"] = uname
    user["password"] = pswrd
    return user


def user_exists(uname, pswrd=None):
    srch = {"uname": uname}
    if pswrd:
        srch["password"] = pswrd
    return bool(user_db.find_one(srch))


def add_user(user):
    user_db.insert_one(user)


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
