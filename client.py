import socket_util as su
import json
from os import system


def clear():
    system("cls")


sock = su.client("192.168.68.137", 12345)
vals_to_req = 10
state = "start"
while True:
    print("\nEnter action")
    if state == "start":
        print("b: go back (exit)\na: add forum\n"
              "s[]: search forum\n\tsl: by latest\n\tsn: by name\n\tsk: by keywords")
        action = input()
        if action == "b":
            sock.close()
            break
        if action == "sl":
            forums = list()
            vals_requested = 0
            last_srch_req_id = 0
            state = "search"
            forums = su.send_request(sock, 0, (vals_requested, vals_to_req))
            vals_requested += len(forums)
            print("Forums: ")
            for id, name, desc in forums:
                print(f"id: {id}| Name: {name}, description: {desc}")
        elif action == "a":
            print("Enter forum name:")
            name = input()
            print("Enter forum description:")
            desc = input()
            print(su.send_request(sock, 1, (name, desc)))
        else:
            print("Invalid action")
            send_req = False

    elif state == "search":
        print("b: go back (start)\nm: show more forums\ne: enter forum")
        action = input()
        if action == "b":
            state = "start"
            continue
        if action == "m":
            forums = su.send_request(sock, last_srch_req_id, (vals_requested, vals_to_req))
            len_forums = len(forums)
            if len_forums == 0:
                print("No more forums")
                continue
            for i, x in enumerate(forums):
                print(f"{i + vals_requested}: {x}")
            vals_requested += len_forums
        elif action == "e":
            print("Enter forum id")
            f_i = input()
            to_enter = forums[int(f_i)]
            state = "forum"
        else:
            print("Invalid action")
            send_req = False

    elif state == "forum":
        pass
