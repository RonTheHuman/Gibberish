import socket_util as su
import json
from functools import reduce


def reply(req_id, data, ip):
    data = json.loads(data.decode())
    if req_id == 0:  # Get an [amount] of forums from index [start]
        start, amount = data
        to_send = list()
        for forum in dbase["forums"][start:start+amount]:
            to_send.append((forum["id"], forum["name"], forum["description"]))
    elif req_id == 1:  # add forum
        name, desc = data
        forum = forum_template.copy()
        forum["name"] = name
        forum["description"] = desc
        forum["id"] = dbase["last_forum_id"]
        dbase["last_forum_id"] += 1
        dbase["forums"].append(forum)
        with open("dbase.txt", mode="w") as f:
            f.write(json.dumps(dbase))
        to_send = "Added to database"
    elif req_id == 2:  # Get posts: id, title, user
        forum_id, start, amount = data
        to_send = list()
        for forum in dbase["forums"]:
            if forum["id"] == forum_id:
                break
        for post in forum["posts"][start:start+amount]:
            to_send.append((post["id"], post["title"], post["user"]))
    elif req_id == 3:  # add post
        forum_id, title, text = data
        post = post_template.copy()
        for forum in dbase["forums"]:
            if forum["id"] == forum_id:
                break
        post["id"] = forum["last_post_id"]
        forum["last_post_id"] += 1
        post["title"] = title
        post["text"] = text
        post["user"] = ip
        forum["posts"].append(post)
        with open("dbase.txt", mode="w") as f:
            f.write(json.dumps(dbase))
        to_send = "Added to database"
    elif req_id == 4:  # get post text
        forum_id, post_id = data
        for forum in dbase["forums"]:
            if forum["id"] == forum_id:
                break
        for post in forum["posts"]:
            if post["id"] == post_id:
                break
        to_send = post["text"]
    elif req_id == 5:  # get comments
        forum_id, post_id, start, amount = data
        to_send = list()
        for forum in dbase["forums"]:
            if forum["id"] == forum_id:
                break
        for post in forum["posts"]:
            if post["id"] == post_id:
                break
        for comment in post["comments"][start:start+amount]:
            to_send.append((comment["text"], comment["user"]))
    elif req_id == 6:  # add comment
        forum_id, post_id, text = data
        for forum in dbase["forums"]:
            if forum["id"] == forum_id:
                break
        for post in forum["posts"]:
            if post["id"] == post_id:
                break
        comment = comment_template.copy()
        comment["user"] = ip
        comment["text"] = text
        post["comments"].append(comment)
        with open("dbase.txt", mode="w") as f:
            f.write(json.dumps(dbase))
        to_send = "Added to database"
    else:
        to_send = "Invalid request error"

    return json.dumps(to_send).encode()



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

with open("dbase.txt") as f:
    dbase = json.loads(f.read())
if dbase is None:
    dbase = {"last_forum_id": 0, "forums": list()}
su.server(12345, reply)
