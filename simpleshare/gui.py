# gui.py
import tkinter as tk


class Simpleshare(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("Simpleshare")
        self.master.geometry("150x200")
        self.pack()
        self.create_widgets()
    # init

    def create_widgets(self):
        self.lb_title = tk.Label(self, text="Simpleshare")
        self.lb_title.pack(side=tk.TOP)

        self.btn_upload = tk.Button(self, text="Upload a file",
                                    command=self.show_upload)
        self.btn_upload.pack(side=tk.LEFT)

        self.btn_download = tk.Button(self, text="Download a file")
        self.btn_download.pack(side=tk.RIGHT)

    # create_widgets

    def show_upload(self):
        self.frm_upload = Upload(self)
        self.frm_upload.pack(side=tk.BOTTOM)
        # self.frm_upload.tkraise()
        # self.pack()
    # show_upload

    def show_download(self):
        pass
    # show_download

# Simpleshare


class Upload(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.timeout_text = tk.StringVar(value="Timeout: 2 mins...")
        self.create_widgets()
    # init

    def create_widgets(self):
        self.btn_file = tk.Button(self, command=self.handle_btn_file,
                                  text="Select File...")
        self.btn_file.pack()
        self.lb_timout = tk.Label(self, textvariable=self.timeout_text)
        self.lb_timout.pack()
    # create_widgets

    def handle_btn_file(self):
        print("Select file?")
        self.timeout_text.set("foo")

# Upload


class Download(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
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
