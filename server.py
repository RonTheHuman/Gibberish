import socket_util as su
import dbase_util as du
import json


def reply(req_id, data, ip):
    data = json.loads(data.decode())
    print("test")
    to_send = ""

    if req_id == 0:  # add forum
        name, desc = data
        forum = du.forum(name, desc)
        du.add_forum(forum)
    elif req_id == 1:  # add post
        forum_id, title, text, uname = data
        post = du.post(title, text, uname)
        du.add_post(post, forum_id)
    elif req_id == 2:  # add comment
        forum_id, post_id, text, uname = data
        comment = du.comment(text, uname)
        du.add_comment(comment, post_id, forum_id)
    elif req_id == 3:
        uname, pswrd = data  # add user
        du.add_user(du.user(uname, pswrd))

    elif req_id == 10:  # Get forums sorted by latest (id decreasing)
        if len(data) == 0:
            slc = None
        else:
            start, amount = data
            slc = (start, start+amount)
        to_send = du.get_forum_data(("_id", "name", "description", "user_count"), slc=slc)
    elif req_id == 11:  # get forums sorted by text
        if len(data) == 1:
            slc = None
            search_text = data
        else:
            start, amount, search_text = data
            slc = (start, start + amount)
        to_send = du.get_forum_data(("_id", "name", "description", "user_count"), slc=slc, text_sort=search_text)
    elif req_id == 12:  # get forums sorted by keywords
        if len(data) == 1:
            slc = None
            search_kwrd = data[0]
        else:
            start, amount, search_kwrd = data
            slc = (start, start + amount)
        to_send = du.get_forum_data(("_id", "name", "description", "user_count"), slc=slc, kwrd_sort=search_kwrd)
    elif req_id == 13:  # get forums sorted by user amount
        if len(data) == 0:
            slc = None
        else:
            start, amount = data
            slc = (start, start+amount)
        to_send = du.get_forum_data(("_id", "name", "description", "user_count"), slc=slc, user_sort=True)
    elif req_id == 14:  # get all forum information, for admin
        forum_id = data
        to_send = du.get_forum_data(("_id", "name", "description", "user_count", "users", "kwrds"), forum_id=forum_id)

    elif req_id == 20:  # Get posts: id, title, user
        forum_id, start, amount = data
        to_send = du.get_post_data(("_id", "title", "user"), forum_id=forum_id, slc=(start, start+amount))
    elif req_id == 21:  # get post text
        post_id = data
        to_send = du.get_post_data(("text", ), post_id=post_id)

    elif req_id == 30:  # get comments: text, user
        post_id, start, amount = data
        to_send = du.get_comment_data(("text", "user"), post_id, slc=(start, start+amount))

    elif req_id == 40:  # check if sign in is vaild
        uname, pswrd = data
        to_send = du.user_exists(uname, pswrd)
    elif req_id == 41:  # check if user name is unique
        uname = data
        to_send = not du.user_exists(uname)

    elif req_id == 50:  # remove keyword from forum
        forum_id, kwrd = data
        du.remove_keyword(forum_id, kwrd)
    elif req_id == 51:  # add keyword to forum
        forum_id, kwrd = data
        du.add_keyword(forum_id, kwrd)

    else:
        raise Exception("Invalid server request error")
    return json.dumps(to_send).encode()


su.server(12345, reply)
