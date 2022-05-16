import socket_util as su
from hashlib import sha256
import random


sock = su.client("192.168.68.137", 12345)
vals_to_req = 10
state = "sign_in"
srch_req_id = None
while True:
    if state != "sign_in":
        warning_msg = su.send_request(sock, 45, uname)
        if warning_msg:
            print("RECIEVED WARNING:")
            print(warning_msg, "\n")
        ban_data = su.send_request(sock, 46, uname)
        if ban_data:
            print(f"You are banned from the forum.\nBan message: {ban_data['message']}\n"
                  f"ban end: {ban_data['end_date']}")
            print("enter any key to sign out")
            input()
            state = "sign_in"
            continue
    print("\nEnter action")
    if state == "sign_in":
        print("Sign In: i\nSign up: u")
        print("Join Anonymously (with ip): a")
        print("b: go back (exit)")
        action = input()
        if action == "b":
            sock.close()
            break
        elif action == "i":
            print("Enter user name")
            uname = input()
            print("Enter password")
            pswrd = input().encode()
            pswrd = sha256(pswrd).hexdigest()
            correct = su.send_request(sock, 40, (uname, pswrd))
            if correct:
                print("Signed in Successfully")
                state = "browse"
            else:
                print("Incorrect user name or password")
        elif action == "u":
            print("Enter user name")
            unique = False
            while not unique:
                uname = input()
                unique = su.send_request(sock, 41, uname)
                if not unique:
                    sugg = f"{uname}{random.randint(10000000, 1000000000)}"
                    sugg_unique = su.send_request(sock, 41, sugg)
                    while not sugg_unique:
                        sugg = f"{uname}{random.randint(10000000, 100000000)}"
                        sugg_unique = su.send_request(sock, 41, sugg)
                    print(f"User name already exists, try another one.\n"
                          f"suggestion: {sugg}")
            print("Enter password")
            pswrd = input().encode()
            pswrd = sha256(pswrd).hexdigest()
            su.send_request(sock, 3, (uname, pswrd))
            print("Signed up Successfully")
            state = "browse"
        elif action == "a":
            uname = sock.getsockname()[0]
            first_time_anonymous = su.send_request(sock, 41, uname)
            if first_time_anonymous:
                su.send_request(sock, 3, (uname, None))
            state = "browse"
            print("Joined successfully")

    elif state == "browse":
        print("b: go back\na: add forum\n"
              "s[]: pick search type\n\t"
              "sl: by latest\n\tsn: search by name\n\tsk: search by keywords\n"
              "m: show more forums\ne: enter forum")
        action = input()
        if action == "b":
            state = "sign_in"
            continue
        if action == "sl":  # set search
            vals_requested = 0
            srch_req_id = 10
            print("Search type set as 'latest'")
        elif action == "sn":
            vals_requested = 0
            srch_req_id = 11
            print("Enter name: ")
            search_name = input()
            print(f"Searching by name {search_name}")
        elif action == "sk":
            vals_requested = 0
            srch_req_id = 12
            print("Enter keyword: ")
            search_kwrd = input()
            print(f"Searching by keyword {search_kwrd}")
        elif action == "a":  # add forum
            print("Enter forum name:")
            name = input()
            unique_f = su.send_request(sock, 18, name)
            if not unique_f:
                print("Forum name already taken")
                continue
            similar_forum = su.send_request(sock, 17, name)
            if similar_forum is not None:
                print("Our algorithm detected a similar forum: ")
                print(f"Name: {similar_forum['name']}\nDescription: {similar_forum['description']}")
                print("Are you sure you want to create this forum?\ny: yes\nn: no")
                action = input()
                while action != "y" and action != "n":
                    print("Invalid input, enter again")
                    action = input()
                if action == "n":
                    continue
            print("Enter forum description:")
            desc = input()
            su.send_request(sock, 0, (name, desc))
            print("Added to database")
            vals_requested = 0
        elif action == "m":  # show forums
            if srch_req_id is None:
                print("Choose a search type first")
                continue
            data = [vals_requested, vals_to_req]
            if srch_req_id == 11:
                data.append(search_name)
            elif srch_req_id == 12:
                data.append(search_kwrd)
            forum_data_arr = su.send_request(sock, srch_req_id, data)
            if len(forum_data_arr) == 0:
                print("No more forums")
                continue
            vals_requested += len(forum_data_arr)
            for forum_data in forum_data_arr:
                print(f"id: {forum_data['_id']}| Name: {forum_data['name']}, description: {forum_data['description']}")
        elif action == "e":  # enter forum
            print("Enter forum id")
            forum_id = int(input())
            state = "forum"
            vals_requested = 0

    elif state == "forum":
        print("b: go back\nm: show more posts\na: add post\ne: enter post")
        post_data_arr = su.send_request(sock, 20, (forum_id, vals_requested, vals_to_req))
        vals_requested += len(post_data_arr)
        print("Posts in forum")  # show initial posts
        for post_data in post_data_arr:
            print(f"id: {post_data['_id']}| Title: {post_data['title']}, posted by: {post_data['user']}")
        action = input()
        if action == "b":
            state = "browse"
            srch_req_id = None
            vals_requested = 0
            continue
        if action == "m":  # show posts
            post_data_arr = su.send_request(sock, 20, (forum_id, vals_requested, vals_to_req))
            if len(post_data_arr) == 0:
                print("No more posts")
                continue
            vals_requested += len(post_data_arr)
            for post_data in post_data_arr:
                print(f"id: {post_data['_id']}| Title: {post_data['title']}, posted by: {post_data['user']}")
        elif action == "a":  # add post
            print("Enter post title:")
            title = input()
            print("Enter post content:")
            content = input()
            su.send_request(sock, 1, (forum_id, title, content, uname))
            print("Added to database")
            vals_requested = 0
        elif action == "e":  # enter post
            print("Enter post id")
            post_id = input()
            state = "post"
            vals_requested = 0

    elif state == "post":
        print("b: go back\nm: show more comments\na: add comment")
        post = su.send_request(sock, 21, post_id)
        comment_data_arr = su.send_request(sock, 30, (post_id, vals_requested, vals_to_req))
        vals_requested += len(comment_data_arr)
        print(f"Post content:\n{post['text']}")
        print("Comments on post")  # show initial comments
        for comment_data in comment_data_arr:
            print(f"{comment_data['text']}, posted by: {comment_data['user']}")
        action = input()
        if action == "b":
            state = "forum"
            vals_requested = 0
            continue
        if action == "m":  # show comments
            comment_data_arr = su.send_request(sock, 30, (post_id, vals_requested, vals_to_req))
            if len(comment_data_arr) == 0:
                print("No more comments")
                continue
            vals_requested += len(comment_data_arr)
            for comment_data in comment_data_arr:
                print(f"{comment_data['text']}, posted by: {comment_data['user']}")
        elif action == "a":  # add comment
            print("Enter comment text:")
            text = input()
            su.send_request(sock, 2, (forum_id, post_id, text, uname))
            print("Added to database")
            vals_requested = 0
