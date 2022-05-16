import tkinter as tk
from tkinter import ttk


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


def sign_in_screen(main_frame):
    destroy_children(main_frame)
    change_min_window_size(300, 300)
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


def browse_screen(main_frame):
    destroy_children(main_frame)
    change_min_window_size(500, 1000)
    stretch_config(main_frame, (1, ), (0, ))

    search_frame = ttk.Frame(main_frame)
    search_frame.grid(sticky="NEW")
    stretch_config(search_frame, (1, )*6, (1, )*2)
    ttk.Button(search_frame, text="Show Latest"). \
        grid(row=0, column=0, rowspan=2, sticky="NSEW")
    ttk.Separator(search_frame, orient=tk.VERTICAL). \
        grid(row=0, column=1, rowspan=2, sticky="NS", padx=10)

    ttk.Label(search_frame, text="Query:"). \
        grid(row=0, column=2)
    ttk.Entry(search_frame). \
        grid(row=0, column=3, columnspan=2, sticky="EW", pady=5)
    ttk.Label(search_frame, text="Search by: "). \
        grid(row=1, column=2)
    ttk.Button(search_frame, text="Text"). \
        grid(row=1, column=3)
    ttk.Button(search_frame, text="Keyword"). \
        grid(row=1, column=4)
    ttk.Separator(search_frame, orient=tk.VERTICAL). \
        grid(row=0, column=5, rowspan=2, sticky="NS", padx=10)

    ttk.Label(search_frame, text="Id: "). \
        grid(row=0, column=6)
    ttk.Entry(search_frame). \
        grid(row=0, column=7, sticky="EW", pady=5)
    ttk.Button(search_frame, text="Quick join"). \
        grid(row=1, column=6, columnspan=2, sticky="EW")

    forum_list = ttk.Labelframe(main_frame, text="Forums", padding=10, relief="solid", borderwidth=10)
    forum_list.grid(sticky="NEW", padx=20, pady=10)
    stretch_config(forum_list, (1, ), (1, )*10)
    ttk.Label(forum_list, text="No forums searched/found!").grid()
    for x in range(3):
        forum = ttk.Frame(forum_list, relief="ridge", padding=10)
        forum.grid(sticky="EW", pady=5)
        stretch_config(forum, (1, 4, 1), ())
        ttk.Label(forum, text="Id: 0"). \
            grid(row=0, column=0, padx=5, sticky="NSEW")
        ttk.Label(forum, text="Name: Programming"). \
            grid(row=0, column=1, padx=5, sticky="NSEW")
        ttk.Button(forum, text="Join"). \
            grid(row=0, column=2, padx=5, sticky="NSEW")
        ttk.Label(forum, text="Descpription: ."). \
            grid(row=1, column=0, columnspan=3, pady=5, sticky="NSEW")


def forum_screen(main_frame):
    destroy_children(main_frame)
    change_min_window_size(500, 1000)
    stretch_config(main_frame, (1, ), (0, ))

    top_frame = ttk.Frame(main_frame)
    top_frame.grid(sticky="NEW", padx=20, pady=10)
    stretch_config(top_frame, (1, )*3, (1, )*2)
    ttk.Label(top_frame, wraplength=400, text="In forum: Programming"). \
        grid(row=0, column=0, sticky="w")
    ttk.Label(top_frame, wraplength=500, text="Descrpition: For general questions about programming in all programming languages."). \
        grid(row=1, column=0, sticky="w")
    ttk.Separator(top_frame, orient=tk.VERTICAL). \
        grid(row=0, column=1, rowspan=2, sticky="NS", padx=10)
    ttk.Button(top_frame, text="Create post"). \
        grid(row=0, column=2, rowspan=2, sticky="NSEW")

    post_list = ttk.Labelframe(main_frame, text="Posts", padding=10, borderwidth=10)
    post_list.grid(row=1, column=0, pady=10, sticky="NEW")
    stretch_config(post_list, (1, ), (1, )*10)
    ttk.Label(post_list, text="No posts yet!").grid()
    for x in range(3):
        post = ttk.Frame(post_list, relief="ridge", padding=10)
        post.grid(pady=5, sticky="NEW")
        stretch_config(post, (5, 1), ())
        ttk.Label(post, text="Title: Any tips for a beginner programmer?"). \
            grid(row=0, column=0, pady=2, sticky="NSEW")
        ttk.Label(post, text="By user: RonTheHuman"). \
            grid(row=1, column=0, pady=2, sticky="NSEW")
        ttk.Button(post, text="Enter"). \
            grid(row=0, column=1, padx=5, sticky="NSEW")


def post_screen(main_frame):
    destroy_children(main_frame)
    change_min_window_size(500, 1000)
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
navigation_menu.add_command(label="Back")
navigation_menu.add_command(label="Exit")
menubar.add_cascade(menu=navigation_menu, label='Navigation')

sign_in_screen(main_frame)
# browse_screen(main_frame)
# forum_screen(main_frame)
# post_screen(main_frame)

root.update()
offsetx = int((root.winfo_screenwidth() - root.winfo_width())/2)
offsety = int((root.winfo_screenheight() - root.winfo_height())/2)
root.geometry(f"+{offsetx}+{offsety}")
root.mainloop()
