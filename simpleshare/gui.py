# gui.py
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
import ttk

import sys
import socket
import time
from os import path
from threading import Thread

from simpleshare.util import is_port_open, MCASTGROUP, PORT
from simpleshare.server import broadcast_info, wait_for_replies, send_file
from simpleshare.client import get_filename, recv_file, reply


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
        ip = None
        try:
            with socket.socket() as s:
                s.connect(("google.com", 80))
                ip = s.getsockname()[0]
                print(ip)
                self.master.frm_upload.set_ip(ip)
        except Exception:
            # IP chooser if you can't get to google
            frm_ip = IPChooser(self.master)
            self.master.wait_window(frm_ip.top)
            ip = frm_ip.value
            print(ip)
            self.master.frm_upload.set_ip(ip)

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
        self.timeout = 10
        t_text = f"Timeout: {self.timeout} seconds..."
        self.timeout_text = tk.StringVar(value=t_text)
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

        print(f"Sharing {self.filename_text.get()} for {self.timeout} seconds")

        def broadcast():
            broadcast_info(self.my_ip, MCASTGROUP, self.filename_text.get(),
                           PORT, PORT+1, self.timeout)
        # broadcast

        def reply_n_send():
            reply = wait_for_replies(self.my_ip, self.filename_text.get(),
                                     PORT+1)
            req_fn = reply.split(":")[1]
            send_file(self.my_ip, self.filename, PORT+2)
        # reply_n_send

        b_t = Thread(target=broadcast)
        b_t.start()

        r_t = Thread(target=reply_n_send)
        r_t.start()

        self.update_timeout_text(self.timeout)
    # handle_btn_share

    def set_ip(self, ip):
        self.my_ip = ip
    # set_ip

    def update_timeout_text(self, count):
        self.timeout_text.set(f"Timeout: {count} seconds...")
        if count > 0:
            self.master.master.after(1000, self.update_timeout_text, count-1)
    # update_timeout_text

# Upload


class Download(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.create_widgets()

        self.server_ip = None

        def listen():
            server_ip, filename = get_filename(MCASTGROUP, PORT)
            self.listbox.insert(tk.END, filename)
            self.server_ip = server_ip
        # listen

        l_t = Thread(target=listen)
        l_t.start()

    # init

    def create_widgets(self):
        self.lb_files_avail = ttk.Label(self, text="Files available:")
        self.btn_download = ttk.Button(self, text="Download",
                                       command=self.download_file)
        self.listbox = tk.Listbox(self, height=5)
        self.listbox.bind("<Double-Button-1>", lambda x: self.download_file())

        self.lb_files_avail.grid(row=0, column=0, columnspan=1)
        self.listbox.grid(row=1, column=0, columnspan=2, pady=5)
        self.btn_download.grid(row=2, column=0, columnspan=2)
    # create_widgets

    def download_file(self):
        if self.listbox.curselection() == ():
            return
        filename = self.listbox.get(self.listbox.curselection())
        print(f"Downloading {filename}")

        reply(self.server_ip, PORT+1, filename)
        time.sleep(0.5)
        newpath = asksaveasfilename()
        if not newpath:
            return
        recv_file(self.server_ip, PORT+2, newpath)
        messagebox.showinfo("Done", f"Downloaded {filename}!")
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
