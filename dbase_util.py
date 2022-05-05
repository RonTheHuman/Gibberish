import json


forum_template = \
    {"id": None,
     "name": None,
     "description": None,
     "kwrds": None,
     "users": None,
     "posts": list(),
     "last_post_id": 0}

post_template = \
    {"id": None,
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


def save_dbase():
    with open("dbase.txt", mode="w") as dbase_f:
        dbase_f.write(json.dumps(dbase))


def forum(name, desc):
    forum = forum_template.copy()
    forum["name"] = name
    forum["description"] = desc
    return forum


def add_forum(forum):
    dbase["forums"].append(forum)
    forum["id"] = dbase["last_forum_id"]
    dbase["last_forum_id"] += 1


def find_forum(forum_id):
    for forum in dbase["forums"]:
        if forum["id"] == forum_id:
            break
    return forum


def get_forum_data(data, slice=None, forum_id=None):
    if slice is not None:
        all_data = list()
        forums = dbase["forums"][slice[0]:slice[1]]
        for forum in forums:
            forum_data = list()
            for d in data:
                forum_data.append(forum[d])
            all_data.append(forum_data)
        return all_data
    elif forum_id is not None:
        forum = find_forum(forum_id)
        forum_data = list()
        for d in data:
            forum_data.append(forum[d])
        return forum_data
    else:
        raise Exception("Invalid get_type of form data request from databse")


def post(title, text, user):
    post = post_template.copy()
    post["title"] = title
    post["text"] = text
    post["user"] = user
    return post


def add_post(post, forum_id):
    forum = find_forum(forum_id)
    post["id"] = forum["last_post_id"]
    forum["last_post_id"] += 1
    forum["posts"].append(post)


def find_post(forum, post_id):
    for post in forum["posts"]:
        if post["id"] == post_id:
            break
    return post


def get_post_data(data, forum_id, slice=None, post_id=None):
    forum = find_forum(forum_id)
    if slice is not None:
        all_data = list()
        posts = forum["posts"][slice[0]:slice[1]]
        for post in posts:
            post_data = list()
            for d in data:
                post_data.append(post[d])
            all_data.append(post_data)
        return all_data
    elif post_id is not None:
        post = find_post(forum, post_id)
        post_data = list()
        for d in data:
            post_data.append(post[d])
        return post_data
    else:
        raise Exception("Invalid get_type of post data request from databse")


def comment(text, user):
    comment = comment_template.copy()
    comment["user"] = user
    comment["text"] = text
    return comment


def add_comment(forum_id, post_id, comment):
    post = find_post(find_forum(forum_id), post_id)
    post["comments"].append(comment)


def get_comment_data(data, forum_id, post_id, slice=None):
    post = find_post(find_forum(forum_id), post_id)
    if slice is not None:
        all_data = list()
        comments = post["comments"][slice[0]:slice[1]]
        for comment in comments:
            comment_data = list()
            for d in data:
                comment_data.append(comment[d])
            all_data.append(comment_data)
        return all_data
    else:
        raise Exception("Invalid get_type of post data request from databse")


with open("dbase.txt") as f:
    dbase = json.loads(f.read())
if dbase is None:
    dbase = {"last_forum_id": 0, "forums": list()}
