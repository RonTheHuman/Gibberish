import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import socket_util as su

"""
globals (yes I know they're bad but just imagine that this file is a class and actually its a private variable)
I mean seriously globals as a concept are used all of the time in classes why is it suddenly bad here?
passing everything in functions makes them unreadable and ugly.
plus passing a tkinter var around has the same "problem" as globals.
rant over
"""
state = "sign_in"
last_srch_type = None
last_query = None
starting_val_i = 0
vals_to_req = 9


def change_min_window_size(w, h):
    old_off_x = root.winfo_x()
    old_off_y = root.winfo_y()
    old_w = root.winfo_width()
    old_h = root.winfo_height()
    root.minsize(width=w, height=h)
    root.update()
    offset_x = old_off_x - int((root.winfo_width() - old_w) / 2)
    offset_y = old_off_y - int((root.winfo_height() - old_h) / 2)
    if offset_x <= 0:
        offset_x = 10
    if offset_y <= 0:
        offset_y = 10
    root.geometry(f"+{offset_x}+{offset_y}")


def destroy_children(widget):
    for child in widget.winfo_children():
        child.destroy()


def stretch_config(widget, column_w, row_w):
    for i, w in enumerate(column_w):
        widget.columnconfigure(i, weight=w)
    for i, w in enumerate(row_w):
        widget.rowconfigure(i, weight=w)


def back(main_frame):
    if state == "browse":
        sign_in_screen(main_frame)
    elif state == "forum":
        browse_screen(main_frame)
    elif state == "post":
        forum_screen(main_frame)


def tk_exit(root):
    sock.close()
    root.quit()
    exit()


def change_page(list, list_type, dir, next_button, prev_button):
    global last_srch_type
    global starting_val_i
    global vals_to_req
    global last_query
    starting_val_i += vals_to_req * dir
    if list_type == "forum":
        show_forums(last_srch_type, list, next_button, prev_button, last_query)
    else:
        raise Exception("Invalid list type in page change function")


def show_forums(srch_type, forum_list, next_button, prev_button, query=None):
    global last_srch_type
    global starting_val_i
    global vals_to_req
    global last_query
    last_srch_type = srch_type
    last_query = query
    if query == "":
        messagebox.showwarning("Empty query", "Query cannot be empty")
        return
    data = [starting_val_i, vals_to_req]
    if srch_type == "latest":
        srch_req_id = 10
    elif srch_type == "text":
        srch_req_id = 11
        data.append(query)
    elif srch_type == "keyword":
        srch_req_id = 12
        data.append(query)
    else:
        raise Exception("Invalid forum search type")
    destroy_children(forum_list)
    ttk.Label(forum_list, text="No forums found!").grid(row=0)
    forum_data_arr = su.send_request(sock, srch_req_id, data)
    i = 0
    for i, forum_data in enumerate(forum_data_arr):
        forum = ttk.Frame(forum_list, relief="ridge", padding=10)
        forum.grid(sticky="EW", pady=5, row=i)
        stretch_config(forum, (1, 4, 1), ())
        ttk.Label(forum, text=f"Id: {forum_data['_id']}"). \
            grid(row=0, column=0, padx=5, sticky="NSEW")
        ttk.Label(forum, text=f"Name: {forum_data['name']}"). \
            grid(row=0, column=1, padx=5, sticky="NSEW")
        _id = forum_data['_id']
        name = forum_data['name']
        desc = forum_data['description']
        bt = ttk.Button(forum, text="Join",
                   command=lambda _id=_id, name=name, desc=desc: forum_screen(main_frame, _id, name, desc)). \
            grid(row=0, column=2, padx=5, sticky="NSEW")
        desc = forum_data["description"]
        if len(desc) > 70:
            desc = desc[:70]
            desc = desc[:desc.rfind(" ")] + " ..."
        ttk.Label(forum, text=f"Description: {desc}"). \
            grid(row=1, column=0, columnspan=3, pady=5, sticky="NSEW")
    if starting_val_i == 0:
        prev_button["state"] = tk.DISABLED
    else:
        prev_button["state"] = tk.ACTIVE
    if i < vals_to_req - 1:
        next_button["state"] = tk.DISABLED
    else:
        next_button["state"] = tk.ACTIVE


def show_posts(post_list, next_button, prev_button, forum_id):
    global starting_val_i
    global vals_to_req
    ttk.Label(post_list, text="No posts yet!").grid()
    post_data_arr = su.send_request(sock, 20, (forum_id, starting_val_i, vals_to_req))
    for post_data in post_data_arr:
        post = ttk.Frame(post_list, relief="ridge", padding=10)
        post.grid(pady=5, sticky="NEW")
        stretch_config(post, (5, 1), ())
        ttk.Label(post, text=f"Title: {post_data['title']}"). \
            grid(row=0, column=0, pady=2, sticky="NSEW")
        ttk.Label(post, text=f"By user: {post_data['user']}"). \
            grid(row=1, column=0, pady=2, sticky="NSEW")
        ttk.Button(post, text="Enter", command=lambda: post_screen(main_frame, forum_id, post_data["_id"])). \
            grid(row=0, column=1, padx=5, sticky="NSEW")


def sign_in_screen(main_frame):
    global state
    state = "sign_in"
    navigation_menu.entryconfigure("Back", state=tk.DISABLED)

    destroy_children(main_frame)
    stretch_config(main_frame, (1, ), (1, ))
    content_frame = ttk.Frame(main_frame)
    content_frame.grid()
    ttk.Label(content_frame, text="Welcome to GIBBERISH", padding=20, relief="groove").\
        grid(row=0, column=0, sticky="NSEW")
    ttk.Button(content_frame, text="Sign In").\
        grid(row=1, column=0, sticky="NSEW")
    ttk.Button(content_frame, text="Sign Up").\
        grid(row=2, column=0, sticky="NSEW")
    ttk.Button(content_frame, text="Enter Anonymously", command=lambda: browse_screen(main_frame)).\
        grid(row=3, column=0, sticky="NSEW")
    change_min_window_size(300, 300)


def browse_screen(main_frame):
    global state
    global starting_val_i
    starting_val_i = 0
    state = "browse"
    navigation_menu.entryconfigure("Back", state=tk.ACTIVE)
    destroy_children(main_frame)
    stretch_config(main_frame, (1, 1), (0, ))

    search_frame = ttk.Frame(main_frame)
    search_frame.grid(sticky="NEW", row=0, columnspan=2, pady=10)
    stretch_config(search_frame, (1, )*6, (1, )*2)

    ttk.Button(main_frame, text="Create forum"). \
        grid(row=1, columnspan=2, pady=20)

    forum_list = ttk.Labelframe(main_frame, text="Forums", padding=10, relief="solid", borderwidth=10)
    forum_list.grid(sticky="NEW", padx=20, row=2, columnspan=2)
    stretch_config(forum_list, (1, ), (1, )*10)

    query_str = tk.StringVar(search_frame, value=None)
    next_button = ttk.Button(main_frame, text="Next page", state=tk.DISABLED,
                             command=lambda: change_page(forum_list, "forum", 1, next_button, prev_button))
    next_button.grid(row=3, column=1, sticky="w", padx=10, pady=10)
    prev_button = ttk.Button(main_frame, text="Previous page", state=tk.DISABLED,
                             command=lambda: change_page(forum_list, "forum", -1, next_button, prev_button))
    prev_button.grid(row=3, column=0, sticky="e", padx=10, pady=10)

    ttk.Button(search_frame, text="Show Latest",
               command=lambda: show_forums("latest", forum_list, next_button, prev_button)). \
        grid(row=0, column=0, rowspan=2, sticky="NSEW")
    ttk.Separator(search_frame, orient=tk.VERTICAL). \
        grid(row=0, column=1, rowspan=2, sticky="NS", padx=10)

    ttk.Label(search_frame, text="Query:"). \
        grid(row=0, column=2)
    ttk.Entry(search_frame, textvariable=query_str). \
        grid(row=0, column=3, columnspan=2, sticky="EW", pady=5)
    ttk.Label(search_frame, text="Search by: "). \
        grid(row=1, column=2)
    ttk.Button(search_frame, text="Text",
               command=lambda: show_forums("text", forum_list, next_button, prev_button, query=query_str.get(), )). \
        grid(row=1, column=3)
    ttk.Button(search_frame, text="Keyword",
               command=lambda: show_forums("keyword", forum_list, next_button, prev_button, query=query_str.get())). \
        grid(row=1, column=4)
    ttk.Separator(search_frame, orient=tk.VERTICAL). \
        grid(row=0, column=5, rowspan=2, sticky="NS", padx=10)

    ttk.Label(search_frame, text="Id: "). \
        grid(row=0, column=6)
    ttk.Entry(search_frame). \
        grid(row=0, column=7, sticky="EW", pady=5)
    ttk.Button(search_frame, text="Quick join"). \
        grid(row=1, column=6, columnspan=2, sticky="EW")

    ttk.Label(forum_list, text="No forums searched for yet!").grid(row=0)
    change_min_window_size(700, 1100)


def forum_screen(main_frame, forum_id, forum_name, forum_desc):
    global state
    global starting_val_i
    starting_val_i = 0
    state = "forum"
    destroy_children(main_frame)
    stretch_config(main_frame, (1, 1), (0, ))

    top_frame = ttk.Frame(main_frame)
    top_frame.grid(sticky="NEW", padx=20, pady=10, columnspan=2)
    stretch_config(top_frame, (4, 0, 1), (1, )*2)

    post_list = ttk.Labelframe(main_frame, text="Posts", padding=10, borderwidth=10)
    post_list.grid(row=1, column=0, pady=10, sticky="NEW", columnspan=2)
    stretch_config(post_list, (1,), (1,) * 10)

    next_button = ttk.Button(main_frame, text="Next page", state=tk.DISABLED,
                             command=lambda: change_page(post_list, "post", 1, next_button, prev_button))
    next_button.grid(row=2, column=1, sticky="w", padx=10)
    prev_button = ttk.Button(main_frame, text="Previous page", state=tk.DISABLED,
                             command=lambda: change_page(post_list, "post", -1, next_button, prev_button))
    prev_button.grid(row=2, column=0, sticky="e", padx=10)

    ttk.Label(top_frame, wraplength=500, text=f"In forum: {forum_name}"). \
        grid(row=0, column=0, sticky="w")
    ttk.Label(top_frame, wraplength=500, text=f"Descrpition: {forum_desc*5}"). \
        grid(row=1, column=0, sticky="w")
    ttk.Separator(top_frame, orient=tk.VERTICAL). \
        grid(row=0, column=1, rowspan=2, sticky="NS", padx=10)
    ttk.Button(top_frame, text="Create post"). \
        grid(row=0, column=2, rowspan=2, sticky="EW")

    show_posts(post_list, next_button, prev_button, forum_id)

    change_min_window_size(700, 1000)


def post_screen(main_frame, forum_id, post_id):
    global state
    global starting_val_i
    starting_val_i = 0
    state = "post"
    destroy_children(main_frame)
    stretch_config(main_frame, (1, ), (0, ))

    top_frame = ttk.Frame(main_frame)
    top_frame.grid(sticky="NEW", padx=20, pady=10)
    stretch_config(top_frame, (1, )*3, (1, )*2)
    ttk.Label(top_frame, wraplength=400, text="In post: Any tips for a beginner programmer?"). \
        grid(row=0, column=0, sticky="w")
    ttk.Label(top_frame, wraplength=500, padding=10, relief="solid",
              text="I started programming a month ago and I know the basics. Any general tips? "
                   "And any tips about networking in python?"). \
        grid(row=1, column=0, columnspan=3, pady=5, sticky="w")
    ttk.Label(top_frame, text="By user: RonTheHuman"). \
        grid(row=2, column=0, sticky="w")
    ttk.Separator(top_frame, orient=tk.VERTICAL). \
        grid(row=2, column=1, rowspan=2, sticky="NS", padx=10)
    ttk.Button(top_frame, text="Add comment"). \
        grid(row=2, column=2, sticky="NSEW")

    comment_list = ttk.Labelframe(main_frame, text="Comments", padding=10, borderwidth=10)
    comment_list.grid(row=1, column=0, pady=10, sticky="NEW")
    stretch_config(comment_list, (1, ), (1, )*10)
    ttk.Label(comment_list, text="No comments yet!").grid()
    for x in range(3):
        comment = ttk.Frame(comment_list, relief="ridge", padding=10)
        comment.grid(pady=5, sticky="NEW")
        stretch_config(comment, (5, 1), ())
        ttk.Label(comment, text="Never give up!"). \
            grid(row=0, column=0, pady=2, sticky="NSEW")
        ttk.Label(comment, text="By user: Mr. George"). \
            grid(row=1, column=0, pady=2, sticky="NSEW")
    change_min_window_size(700, 1000)

sock = su.client("192.168.68.137", 12345)

root = tk.Tk()
root.option_add('*tearOff', tk.FALSE)
root.resizable(False, False)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

main_frame = ttk.Frame(root, padding=10, relief="sunken")
main_frame.grid(padx=10, pady=10, sticky="NSEW")

menubar = tk.Menu(root)
root['menu'] = menubar
navigation_menu = tk.Menu(menubar)
navigation_menu.add_command(label="Back", command=lambda: back(main_frame))
navigation_menu.add_command(label="Exit", command=lambda: tk_exit(root))
menubar.add_cascade(menu=navigation_menu, label='Navigation')

sign_in_screen(main_frame)

root.update()
offsetx = int((root.winfo_screenwidth() - root.winfo_width())/2)
offsety = int((root.winfo_screenheight() - root.winfo_height())/2)
root.geometry(f"+{offsetx}+{offsety}")
root.mainloop()
