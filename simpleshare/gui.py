# gui.py
import tkinter as tk
from tkinter.filedialog import askopenfilename
import ttk


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
        self.btn_upload.grid(row=1, column=0, padx=5)
        self.btn_download.grid(row=1, column=1, padx=5)
        ttk.Separator(self, orient=tk.HORIZONTAL).grid(row=4,
                                                       sticky="ew",
                                                       pady=10,
                                                       columnspan=2)
    # create_widgets

    def show_upload(self):
        print("Switch to upload page")
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
    # handle_btn_file

    def handle_btn_share(self):
        print(f"Sharing {self.filename_text.get()} for 2 mins")
    # handle_btn_share

# Upload


class Download(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.test_text = ttk.Label(self, text="Test")
        self.test_text.pack()
    # init
# Download


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
|                              |
|------------------------------|
"""
