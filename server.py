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
         "posts": None}

post = {"user": None,
        "title": None,
        "text": None,
        "img_path": None,
        "comments": None}

comment = {"user": None,
           "text": None,
           "img_path": None}

user = {"name": None,
        "hashed_pass": None,
        "forums": None}

dbase = list()
dbase.sort()

su.server(12345, reply)
