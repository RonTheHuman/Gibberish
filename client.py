import socket_util as su
import json
from os import system


sock = su.client("192.168.68.137", 12345)
vals_to_req = 2
state = "start"
srch_req_id = None
while True:
    print("\nEnter action")
    if state == "start":
        print("b: go back (exit)\na: add forum\n"
              "s[]: pick search type\n\tsl: by latest\n"
              "m: show more forums\ne: enter forum")
        action = input()
        if action == "b":
            sock.close()
            break
        if action == "sl":
            vals_requested = 0
            srch_req_id = 0
            print("Search type set as 'latest'")
        elif action == "a":
            print("Enter forum name:")
            name = input()
            print("Enter forum description:")
            desc = input()
            print(su.send_request(sock, 1, (name, desc)))
            vals_requested = 0
        elif action == "m":
            if srch_req_id is None:
                print("Choose a search type first")
                continue
            forums = su.send_request(sock, srch_req_id, (vals_requested, vals_to_req))
            if len(forums) == 0:
                print("No more forums")
                continue
            vals_requested += len(forums)
            for forum_id, name, desc in forums:
                print(f"id: {forum_id}| Name: {name}, description: {desc}")
        elif action == "e":
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
        print("Posts in forum")
        for post_id, title, user in posts:
            print(f"id: {post_id}| Title: {title}, posted by: {user}")
        action = input()
        if action == "b":
            state = "start"
            srch_req_id = None
            vals_requested = 0
            continue
        if action == "m":
            posts = su.send_request(sock, 2, (forum_id, vals_requested, vals_to_req))
            if len(posts) == 0:
                print("No more posts")
                continue
            vals_requested += len(posts)
            for post_id, title, user in posts:
                print(f"id: {post_id}| Title: {title}, posted by: {user}")
        elif action == "a":
            print("Enter post title:")
            title = input()
            print("Enter post content:")
            content = input()
            print(su.send_request(sock, 3, (forum_id, title, content)))
            vals_requested = 0
        elif action == "e":
            print("Enter post id")
            post_id = int(input())
            state = "post"
            vals_requested = 0

    elif state == "post":
        print("b: go back\nm: show more comments\na: add comment")
        post_text = su.send_request(sock, 4, (forum_id, post_id))
        comments = su.send_request(sock, 5, (forum_id, post_id, vals_requested, vals_to_req))
        vals_requested += len(comments)
        print(f"Post content:\n{post_text}")
        print("Comments on post")
        for text, user in comments:
            print(f"{text}, posted by: {user}")
        action = input()
        if action == "b":
            state = "forum"
            vals_requested = 0
            continue
        if action == "m":
            comments = su.send_request(sock, 5, (forum_id, post_id, vals_requested, vals_to_req))
            if len(comments) == 0:
                print("No more comments")
                continue
            vals_requested += len(comments)
            for text, user in comments:
                print(f"{text}, posted by: {user}")
        elif action == "a":
            print("Enter comment text:")
            text = input()
            print(su.send_request(sock, 6, (forum_id, post_id, text)))
            vals_requested = 0
