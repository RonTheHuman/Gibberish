import json
import pymongo


forum_template = \
    {"_id": None,
     "name": None,
     "description": None,
     "kwrds": None,
     "users": None,
     "posts": list(),
     "next_post_id": 0}

post_template = \
    {"_id": None,
     "user": None,
     "title": None,
     "text": None,
     "img_path": None,
     "comments": list()}

comment_template = \
    {"user": None,
     "text": None,
     "img_path": None}

user_template = \
    {"name": None,
     "hashed_pass": None,
     "forums": None}


def forum(name, desc):
    forum = forum_template.copy()
    forum["name"] = name
    forum["description"] = desc
    return forum


def add_forum(forum):
    forum["_id"] = forum_db.find_one_and_update({"next_forum_id": {"$exists": True}},
                                                {"$inc": {"next_forum_id": 1}})["next_forum_id"]
    forum_db.insert_one(forum)


def get_forum_data(data, slice=None):
    data_dict = {x: 1 for x in data}
    if "_id" not in data:
        data_dict["_id"] = 0
    if slice is not None:
        forum_data = list(forum_db.find({"next_forum_id": {"$exists": False}}, data_dict))[slice[0]:slice[1]]
        return forum_data
    else:
        raise Exception("Invalid forum data request")


def post(title, text, user):
    post = post_template.copy()
    post["title"] = title
    post["text"] = text
    post["user"] = user
    return post


def add_post(post, forum_id):
    post["_id"] = forum_db.find_one({"_id": forum_id})["next_post_id"]
    post_db.insert_one(post)
    forum_db.update_one({"_id": forum_id}, {"$inc": {"next_post_id": 1}, "$push": {"posts": post["_id"]}})


def get_post_data(data, forum_id=None, slice=None, post_id=None):
    data_dict = {x: 1 for x in data}
    if "_id" not in data:
        data_dict["_id"] = 0
    if slice is not None:
        post_ids = forum_db.find_one({"_id": forum_id})["posts"]
        return list(post_db.find({"_id": {"$in": post_ids}}, data_dict))[slice[0]:slice[1]]
    elif post_id is not None:
        return post_db.find_one({"_id": post_id}, data_dict)
    else:
        raise Exception("Invalid post data request")


def comment(text, user):
    comment = comment_template.copy()
    comment["user"] = user
    comment["text"] = text
    return comment


def add_comment(comment, post_id):
    insert_res = cmnt_db.insert_one(comment)
    post_db.update_one({"_id": post_id}, {"$push": {"comments": insert_res.inserted_id}})


def get_comment_data(data, post_id, slice=None):
    data_dict = {x: 1 for x in data}
    if "_id" not in data:
        data_dict["_id"] = 0
    if slice is not None:
        comment_ids = post_db.find_one({"_id": post_id})["comments"]
        return list(cmnt_db.find({"_id": {"$in": comment_ids}}, data_dict))[slice[0]:slice[1]]
    else:
        raise Exception("Invalid get_type of post data request from databse")


client = pymongo.MongoClient("mongodb+srv://RonTheHuman:mongomyak2022@cluster0.6rgbh"
                             ".mongodb.net/Gibberish?retryWrites=true&w=majority")
dbase = client["Gibberish"]
forum_db = dbase["forums"]
post_db = dbase["posts"]
cmnt_db = dbase["comments"]
if len(list(forum_db.find({}).limit(1))) == 0:
    print("creating new dbase")
    forum_db.insert_one({"next_forum_id": 0})
