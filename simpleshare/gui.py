# gui.py
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import ttk

import sys
import socket
import time
from os import path
from threading import Thread

from simpleshare.util import is_port_open, MCASTGROUP, PORT
from simpleshare.server import broadcast_info, wait_for_replies, send_file
from simpleshare.client import reply_if_server_available, recv_file


class Simpleshare(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("Simpleshare")
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        self.grid(row=0, column=0, sticky='n')

        self.lb_title = ttk.Label(self, text="Simpleshare")
        self.lb_title.config(font=(None, 15))

        self.frm_home = Home(master=self)
        self.frm_upload = Upload(master=self)
        self.frm_download = Download(master=self)

        self.lb_title.grid(row=1, column=0, columnspan=3, pady=10)
        self.frm_home.grid(row=2, column=0, columnspan=3, sticky='news')
        self.frm_upload.grid(row=2, column=0, columnspan=3, sticky='news')
        self.frm_download.grid(row=2, column=0, columnspan=3, sticky='news')

        self.frm_home.grid_columnconfigure(1, weight=1)
        self.frm_home.grid_rowconfigure(1, weight=1)

        self.raise_frame("home")
    # init

    def raise_frame(self, frame_name):
        if frame_name == "home":
            self.frm_home.tkraise()
        elif frame_name == "upload":
            self.frm_upload.tkraise()
        elif frame_name == "download":
            self.frm_download.tkraise()
        else:
            raise Exception("frame name not found")
    # raise_frame

# Simpleshare


class Home(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        # self.pack()
        self.create_widgets()
    # init

    def create_widgets(self):
        # Widgets
        self.btn_upload = ttk.Button(self, text="Upload a file",
                                     command=self.show_upload)
        self.btn_download = ttk.Button(self, text="Download a file",
                                       command=self.show_download)

        # Layout
        self.btn_upload.grid(row=1, column=0, padx=5, sticky="n")
        self.btn_download.grid(row=1, column=1, padx=5, sticky="n")
    # create_widgets

    def show_upload(self):
        print("Switch to upload page")
        frm_ip = IPChooser(self.master)
        self.master.wait_window(frm_ip.top)
        print(frm_ip.value)
        self.master.frm_upload.set_ip(frm_ip.value)
        self.master.raise_frame("upload")
    # show_upload

    def show_download(self):
        print("Switch to download page")
        self.master.raise_frame("download")
    # show_download

# Home


class Upload(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.my_ip = None
        self.filename = None
        self.timeout_text = tk.StringVar(value="Timeout: 2 mins...")
        self.filename_text = tk.StringVar(value="Select a file...")

        self.create_widgets()
    # init

    def create_widgets(self):
        self.btn_file = ttk.Button(self, command=self.handle_btn_file,
                                   text="Select File...")
        self.lb_timout = ttk.Label(self, textvariable=self.timeout_text)
        self.lb_filename = ttk.Label(self, textvariable=self.filename_text)
        self.btn_share = ttk.Button(self, command=self.handle_btn_share,
                                    text="Share")

        self.btn_file.grid(row=0, column=0, padx=5)
        self.lb_filename.grid(row=0, column=1, padx=5)
        self.btn_share.grid(row=1, column=0, columnspan=2, pady=10)
        self.lb_timout.grid(row=2, column=0, columnspan=2)
    # create_widgets

    def handle_btn_file(self):
        print("Select file?")
        filename = askopenfilename()
        if not filename:
            return
        self.filename_text.set(filename.split("/")[-1])
        self.filename = filename
    # handle_btn_file

    def handle_btn_share(self):
        if not self.filename:
            messagebox.showerror("Error", "You must select a filename")
            return

        print(f"Sharing {self.filename_text.get()} for 2 mins")
        # Send "broadcast" every 5 secs, this is the name of it, and what port
        #  to send your replies to.
        broadcast_thread = Thread(target=broadcast_info, args=(
            self.my_ip, MCASTGROUP, self.filename_text.get(), PORT, PORT+1))
        broadcast_thread.daemon = True
        broadcast_thread.start()

        # listen to replies, see if they want the file while the broadcast
        # is active.
        # #TODO: Make this stop when the bcast thread stops...
        while broadcast_thread.is_alive():
            reply = wait_for_replies(self.my_ip, self.filename_text.get(),
                                     PORT+1)
            req_fn = reply.split(":")[1]
            # print(f"reply: {req_fn}")
            send_file(self.my_ip, self.filename_text.get(), PORT+2)

        broadcast_thread.join()
    # handle_btn_share

    def set_ip(self, ip):
        self.my_ip = ip
    # set_ip

# Upload


class Download(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.create_widgets()
    # init

    def create_widgets(self):
        self.lb_files_avail = ttk.Label(self, text="Files available:")
        self.btn_test = ttk.Button(self, text="Add test item",
                                   command=lambda: self.add_to_list("Test"))
        self.btn_download = ttk.Button(self, text="Download",
                                       command=self.download_file)
        self.listbox = tk.Listbox(self, height=5)
        self.listbox.bind("<Double-Button-1>", lambda x: self.download_file())

        self.lb_files_avail.grid(row=0, column=0, columnspan=1)
        self.btn_test.grid(row=0, column=1, columnspan=1)
        self.listbox.grid(row=1, column=0, columnspan=2, pady=5)
        self.btn_download.grid(row=2, column=0, columnspan=2)
    # create_widgets

    def add_to_list(self, item):
        self.listbox.insert(tk.END, item)
    # add_to_list

    def download_file(self):
        if self.listbox.curselection() == ():
            return
        filename = self.listbox.get(self.listbox.curselection())
        print(filename)
    # download_file

# Download


class IPChooser(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        top = self.top = tk.Toplevel(master.master)
        self.ip = None

        # import center_window only if choosing IP
        from simpleshare import center_window
        center_window(self.top, 200, 200)

        self.ip_list = socket.gethostbyname_ex(socket.gethostname())[2]
        self.create_widgets()

        for ip in self.ip_list:
            self.listbox.insert(tk.END, ip)
    # init

    def cleanup(self):
        if not self.ip:
            raise Exception("IP not chosen")

        self.value = self.ip
        self.top.destroy()
        return self.value
    # cleanup

    def create_widgets(self):
        # print(self.ip_list)
        self.lb_ip = ttk.Label(self.top, text="Pick an IP address")
        self.listbox = tk.Listbox(self.top, height=len(self.ip_list))
        self.btn_choose_ip = ttk.Button(self.top, text="Choose",
                                        command=self.choose_ip)

        self.listbox.bind("<Double-Button-1>", lambda x: self.choose_ip())

        self.lb_ip.pack()
        self.listbox.pack(pady=5)
        self.btn_choose_ip.pack()

        # self.lb_ip.grid(row=0, column=0)
        # self.listbox.grid(row=1, column=0, pady=5)
        # self.btn_choose_ip.grid(row=2, column=0)
    # create_widgets

    def choose_ip(self):
        if self.listbox.curselection() == ():
            return
        self.ip = self.listbox.get(self.listbox.curselection())
        # print(self.ip)
        self.cleanup()
    # btn_choose_ip

# IPChooser


# # frame structure / wireframe
# page 1
"""
|------------------------------|
|       simmpleshare           |
|  -------------------------   |
|  | "Upload" | "Download" |   | # on click of upload/download, open respective
|  -------------------------   | #  "page" (frame)
|                              |
|------------------------------|
"""
# page 2 (Upload)
"""
|------------------------------|
|       simmpleshare           |
|    ------------------        |
|    | Choose File... |        | # on click on choose file, filepicker appears
|    ------------------        | #  and timeout starts
|                              |
|    Timeout: MM:SS            |
|                              |
|                              |
|------------------------------|
"""
# page 3 (Download)
"""
|------------------------------|
|       simmpleshare           |
|                              |
|      Files Available:        |
|                              |
|      ----------------        | # List filenames as the client can find them
|      |  <Filename1> |        | #  on click of one, open file picker to save
|      |  <Filename2> |        |
|      ----------------        |
|                              |
|       --------------         |
|       |  Download  |         |
|       --------------         |
|                              |
|------------------------------|
"""
# page 4 (IP picker)
"""
|------------------------------|
|      Pick your IP address    |
|                              |
|      ----------------        | # List IP addresses
|      |  <IPAddress> |        |
|      |  <IPAddress> |        |
|      ----------------        | # eventually add an Entry for the IP
|       --------------         |
|       |   Choose   |         |
|       --------------         |
|                              |
|------------------------------|
"""
