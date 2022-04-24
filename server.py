import socket_util as su
from functools import reduce


def reply(req_id, data):
    if req_id == 0:
        dbase.append(str.lower(data.decode()))
        dbase.sort()
        return su.add_len_bytes("ack".encode())
    elif req_id == 1:
        start, end = data.decode().split(",")
        send_data = reduce(lambda x, y: f"{x}, {y}", dbase[int(start):int(end)]).encode()
        return su.add_len_bytes(send_data)


forum = {"id": None,
         "name": None,
         "description": None,
         "kwrds": None,
         "users": None,
         "posts": None}   # maybe not needed?

post = {"user": None,
        "name": None,
        "text": None,
        "img_path": None,
        "comments": None}  # maybe not needed?

comment = {"user": None,
           "text": None,
           "img_path": None,
           "likes": None,
           "dislikes": None}

user = {"name": None,
        "hashed_pass": None,
        "forums": None}

dbase = ["text", "ornery", "werewolf", "porch", "qwerty", "apple"]
dbase.sort()

su.server(12345, reply)
