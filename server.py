import socket_util as su
import dbase_util as du
import json


def reply(req_id, data, ip):
    data = json.loads(data.decode())
    to_send = ""
    if req_id == 0:  # Get forums
        start, amount = data
        to_send = list()
        to_send = du.get_forum_data(("_id", "name", "description"), slc=(start, start+amount))
    elif req_id == 1:  # add forum
        name, desc = data
        forum = du.forum(name, desc)
        du.add_forum(forum)
    elif req_id == 2:  # Get posts: id, title, user
        forum_id, start, amount = data
        to_send = du.get_post_data(("_id", "title", "user"), forum_id=forum_id, slc=(start, start+amount))
    elif req_id == 3:  # add post
        forum_id, title, text, uname = data
        post = du.post(title, text, uname)
        du.add_post(post, forum_id)
    elif req_id == 4:  # get post text
        post_id = data
        to_send = du.get_post_data(("text", ), post_id=post_id)
    elif req_id == 5:  # get comments
        post_id, start, amount = data
        to_send = du.get_comment_data(("text", "user"), post_id, slc=(start, start+amount))
    elif req_id == 6:  # add comment
        post_id, text, uname = data
        comment = du.comment(text, uname)
        du.add_comment(comment, post_id)
    elif req_id == 7:  # check if sign in is vaild
        uname, pswrd = data
        to_send = du.user_exists(uname, pswrd)
    elif req_id == 8:  # check if user name is unique
        uname = data
        to_send = not du.user_exists(uname)
    elif req_id == 9:
        uname, pswrd = data  # add user
        du.add_user(du.user(uname, pswrd))
    elif req_id == 10:  # get all forums
        to_send = du.get_forum_data(("_id", "name", "description"))
    elif req_id == 11:  # get forms sorted by text
        start, amount, search_text = data
        to_send = du.get_forum_data(("_id", "name", "description"), slc=(start, start+amount), text_sort=search_text)
    elif req_id == 12:  # get forms sorted by keywords
        start, amount, search_kwrd = data
        to_send = du.get_forum_data(("_id", "name", "description"), slc=(start, start+amount), kwrd_sort=search_kwrd)
    else:
        raise Exception("Invalid server request error")
    return json.dumps(to_send).encode()


su.server(12345, reply)
