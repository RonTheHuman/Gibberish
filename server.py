import socket_util as su
import json
from functools import reduce


forum_id = 0  # global


def reply(req_id, data):
    data = data.decode()
    if req_id == 0:
        start, end = json.loads(data)
        to_send = list()
        for forum in dbase[start:end]:
            to_send.append((forum["id"], forum["name"], forum["description"]))
        return json.dumps(to_send).encode()
    if req_id == 1:
        name, desc = json.loads(data)
        forum = forum_template.copy()
        forum["name"] = name
        forum["description"] = desc
        global forum_id
        forum["id"] = forum_id
        forum_id += 1
        dbase.append(forum)
        return json.dumps("Added to database").encode()


forum_template = {"id": None,
         "name": None,
         "description": None,
         "kwrds": None,
         "users": None,
         "posts": None}

post_template = {"user": None,
        "title": None,
        "text": None,
        "img_path": None,
        "comments": None}

comment_template = {"user": None,
           "text": None,
           "img_path": None}

user_template = {"name": None,
        "hashed_pass": None,
        "forums": None}

dbase = list()
su.server(12345, reply)
