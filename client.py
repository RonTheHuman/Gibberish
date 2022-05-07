import socket_util as su
from hashlib import sha256
import random


sock = su.client("192.168.68.137", 12345)
vals_to_req = 10
state = "sign_in"
srch_req_id = None
while True:
    print("\nEnter action")
    if state == "sign_in":
        print("Sign In: i\nSign up: u\nJoin Anonymously (with ip): a\nb: go back (exit)")
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
            correct = su.send_request(sock, 7, (uname, pswrd))
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
                unique = su.send_request(sock, 8, uname)
                if not unique:
                    print(f"User name already exists, try another one.\n"
                          f"suggestion: {uname}{random.randint(10000, 100000)}")
            print("Enter password")
            pswrd = input().encode()
            pswrd = sha256(pswrd).hexdigest()
            su.send_request(sock, 9, (uname, pswrd))
            print("Signed up Successfully")
            state = "browse"
        elif action == "a":
            uname = sock.getsockname()[0]
            print("Joined successfully")

    elif state == "browse":
        print("b: go back (exit)\na: add forum\n"
              "s[]: pick search type\n\tsl: by latest\n"
              "m: show more forums\ne: enter forum")
        action = input()
        if action == "b":
            state = "sign_in"
        if action == "sl":  # set search
            vals_requested = 0
            srch_req_id = 0
            print("Search type set as 'latest'")
        elif action == "a":  # add forum
            print("Enter forum name:")
            name = input()
            print("Enter forum description:")
            desc = input()
            su.send_request(sock, 1, (name, desc))
            print("Added to database")
            vals_requested = 0
        elif action == "m":  # show forums
            if srch_req_id is None:
                print("Choose a search type first")
                continue
            forums = su.send_request(sock, srch_req_id, (vals_requested, vals_to_req))
            if len(forums) == 0:
                print("No more forums")
                continue
            vals_requested += len(forums)
            for forum in forums:
                print(f"id: {forum['_id']}| Name: {forum['name']}, description: {forum['description']}")
        elif action == "e":  # enter forum
            print("Enter forum id")
            forum_id = int(input())
            state = "forum"
            vals_requested = 0
        else:
            print("Invalid action")
            send_req = False

    elif state == "forum":
        print("b: go back\nm: show more posts\na: add post\ne: enter post")
        posts = su.send_request(sock, 2, (forum_id, vals_requested, vals_to_req))
        vals_requested += len(posts)
        print("Posts in forum")  # show initial posts
        for post in posts:
            print(f"id: {post['_id']}| Title: {post['title']}, posted by: {post['user']}")
        action = input()
        if action == "b":
            state = "browse"
            srch_req_id = None
            vals_requested = 0
            continue
        if action == "m":  # show posts
            posts = su.send_request(sock, 2, (forum_id, vals_requested, vals_to_req))
            if len(posts) == 0:
                print("No more posts")
                continue
            vals_requested += len(posts)
            for post in posts:
                print(f"id: {post['_id']}| Title: {post['title']}, posted by: {post['user']}")
        elif action == "a":  # add post
            print("Enter post title:")
            title = input()
            print("Enter post content:")
            content = input()
            su.send_request(sock, 3, (forum_id, title, content, uname))
            print("Added to database")
            vals_requested = 0
        elif action == "e":  # enter post
            print("Enter post id")
            post_id = int(input())
            state = "post"
            vals_requested = 0

    elif state == "post":
        print("b: go back\nm: show more comments\na: add comment")
        post = su.send_request(sock, 4, post_id)
        comments = su.send_request(sock, 5, (post_id, vals_requested, vals_to_req))
        vals_requested += len(comments)
        print(f"Post content:\n{post['text']}")
        print("Comments on post")  # show initial comments
        for comment in comments:
            print(f"{comment['text']}, posted by: {comment['user']}")
        action = input()
        if action == "b":
            state = "forum"
            vals_requested = 0
            continue
        if action == "m":  # show comments
            comments = su.send_request(sock, 5, (post_id, vals_requested, vals_to_req))
            if len(comments) == 0:
                print("No more comments")
                continue
            vals_requested += len(comments)
            for comment in comments:
                print(f"{comment['text']}, posted by: {comment['user']}")
        elif action == "a":  # add comment
            print("Enter comment text:")
            text = input()
            su.send_request(sock, 6, (post_id, text, uname))
            print("Added to database")
            vals_requested = 0
