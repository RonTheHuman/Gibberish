import socket_util as su

sock = su.client("172.16.2.92", 12345)

state = "menu"
while True:
    if state == "menu":
        print("b: back (exit)\nf: forum view\nu: user view")
        # print(s: enter settings\nt: edit time)
        action = input()
        if action == "b":
            sock.close()
            exit()
        elif action == "f":
            state = "forums"
        elif action == "u":
            state = "users"
        # elif action == "s":
        #     state = "settings"
        # elif action == "t":
        #     state = "time"
        else:
            print("Invalid action")
    elif state == "forums":
        print("b: back\nsl: sort by creation date\nst: sort by text\nsk: sort by keyword\nsu: sort by amount of users"
              "\ne: enter forum")
        action = input()
        if action == "b":
            state = "settings"
        elif action == "sl":
            print("All forms:")
            forum_data_arr = su.send_request(sock, 10)
            for forum_data in forum_data_arr:
                print(f"id: {forum_data['_id']}| Name: {forum_data['name']}, description: {forum_data['description']}, "
                      f"{forum_data['user_count']} users")
        elif action == "st":
            print("Enter text")
            text = input()
            print("All forms:")
            forum_data_arr = su.send_request(sock, 11, (text, ))
            for forum_data in forum_data_arr:
                print(f"id: {forum_data['_id']}| Name: {forum_data['name']}, description: {forum_data['description']}, "
                      f"{forum_data['user_count']} users")
        elif action == "sk":
            print("Enter keyword")
            kwrd = input()
            print("All forms:")
            forum_data_arr = su.send_request(sock, 12, (kwrd, ))
            for forum_data in forum_data_arr:
                print(f"id: {forum_data['_id']}| Name: {forum_data['name']}, description: {forum_data['description']}, "
                      f"{forum_data['user_count']} users")
        elif action == "su":
            print("All forms:")
            forum_data_arr = su.send_request(sock, 13)
            for forum_data in forum_data_arr:
                print(f"id: {forum_data['_id']}| Name: {forum_data['name']}, description: {forum_data['description']}, "
                      f"{forum_data['user_count']} users")
        elif action == "e":
            print("Enter forum id:")
            forum_id = int(input())
            state = "forum"
    elif state == "forum":
        print("b: back\nrk: remove keyword\nak: add keyword")
        forum_data = su.send_request(sock, 14, forum_id)
        print(f"id: {forum_data['_id']}| Name: {forum_data['name']}, description: {forum_data['description']}\n "
              f"{forum_data['user_count']} users: {forum_data['users']}\nkeywords: {forum_data['kwrds']}")
        action = input()
        if action == "b":
            state = "forums"
        elif action == "ak":
            print("Enter keyword to add")
            kwrd = input()
            if kwrd not in forum_data["kwrds"]:
                su.send_request(sock, 15, (forum_id, kwrd))
        elif action == "rk":
            print("Enter keyword index to remove")
            kwrd_i = int(input())
            if kwrd_i < len(forum_data["kwrds"]):
                su.send_request(sock, 16, (forum_id, forum_data["kwrds"][kwrd_i]))
            else:
                print("Invalid index")
    elif state == "users":
        users = su.send_request(sock, 42)
        for user in users:
            print(f"User name: {user['uname']}, Hashed password: {user['password']}\n"
                  f"warning: {user.get('warning')}\n"
                  f"ban: {user.get('ban')}\n")
        print("b: back\nbu: ban user\nwu: warn user")
        action = input()
        if action == "b":
            state = "menu"
        elif action == "bu":
            print("Enter user name:")
            uname = input()
            while su.send_request(sock, 41, uname):
                print("Invalid user name")
                print("Enter user name:")
                uname = input()
            if su.send_request(sock, 46, uname):
                print("Ban already exists, you will be overriding it."
                      "\na: abort\nc: continue")
                action = input()
                while action != "a" and action != "c":
                    print("Invalid action, enter again")
                    action = input()
                if action == "a":
                    continue
            print("Enter ban duration - weeks:")
            weeks = int(input())
            print("minutes:")
            minutes = int(input())
            print("Enter ban message")
            msg = input()
            su.send_request(sock, 44, (uname, msg, weeks, minutes))
        elif action == "wu":
            print("Enter user name:")
            uname = input()
            while su.send_request(sock, 41, uname):
                print("Invalid user name")
                print("Enter user name:")
                uname = input()
            if su.send_request(sock, 45, uname):
                print("user is already warned, and hasn't entered since")
                continue
            print("Enter warning message")
            msg = input()
            su.send_request(sock, 43, (uname, msg))

# with open("wordlist_10000.txt") as f:
#     words = f.read().splitlines()
# for word in words:
#     su.send_request(sock, 1, (word, word*2))
