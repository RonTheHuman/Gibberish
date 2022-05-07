import socket_util as su
import dbase_util as du
import json


def reply(req_id, data, ip):
    data = json.loads(data.decode())
    if req_id == 0:  # Get forums
        start, amount = data
        to_send = list()
        to_send = du.get_forum_data(("_id", "name", "description"), slice=(start, start+amount))
    elif req_id == 1:  # add forum
        name, desc = data
        forum = du.forum(name, desc)
        du.add_forum(forum)
        to_send = "Added to database"
    elif req_id == 2:  # Get posts: id, title, user
        forum_id, start, amount = data
        to_send = du.get_post_data(("_id", "title", "user"), forum_id=forum_id, slice=(start, start+amount))
    elif req_id == 3:  # add post
        forum_id, title, text = data
        post = du.post(title, text, ip)
        du.add_post(post, forum_id)
        to_send = "Added to database"
    elif req_id == 4:  # get post text
        post_id = data
        to_send = du.get_post_data(("text", ), post_id=post_id)
    elif req_id == 5:  # get comments
        post_id, start, amount = data
        to_send = du.get_comment_data(("text", "user"), post_id, (start, start+amount))
    elif req_id == 6:  # add comment
        post_id, text = data
        comment = du.comment(text, ip)
        du.add_comment(comment, post_id)
        to_send = "Added to database"
    else:
        to_send = "Invalid request error"
    return json.dumps(to_send).encode()


su.server(12345, reply)
