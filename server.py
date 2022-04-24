import socket_util as su
from functools import reduce
from select import select


def reply(req_id, data):
    if req_id == 0:
        dbase.append(data.decode())
        dbase.sort()
        return su.add_len_bytes("ack".encode())
    elif req_id == 1:
        start, end = data.decode().split(",")
        send_data = reduce(lambda x, y: f"{x}, {y}", dbase[int(start):int(end)]).encode()
        return su.add_len_bytes(send_data)


dbase = ["text", "undulation", "werewolf", "porch", "qwerty", "apple"]
dbase.sort()

su.server(12345, reply)
