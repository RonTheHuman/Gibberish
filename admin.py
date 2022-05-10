import socket_util as su

sock = su.client("192.168.68.137", 12345)

state = "menu"
while True:
    print("\nEnter action:")
    if state == "menu":
        print("b: exit\nf: forum view\nu: user view\ns: enter settings\nt: edit time")
        action = input()
        if action == "b":
            sock.close()
            exit()
        elif action == "f":
            state = "forums"
        elif action == "u":
            state = "users"
        elif action == "s":
            state = "settings"
        elif action == "t":
            pass
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
        elif action == "rk":
            print("Enter keyword index to remove")
            kwrd_i = int(input())
            if kwrd_i < len(forum_data["kwrds"]):
                su.send_request(sock, 17, (forum_id, forum_data["kwrds"][kwrd_i]))
            else:
                print("Invalid index")
        elif action == "ak":
            print("Enter keyword to add")
            kwrd = input()
            if kwrd not in forum_data["kwrds"]:
                su.send_request(sock, 18, (forum_id, kwrd))



# with open("wordlist_10000.txt") as f:
#     words = f.read().splitlines()
# for word in words:
#     su.send_request(sock, 1, (word, word*2))
