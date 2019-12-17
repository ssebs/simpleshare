# gui.py
import tkinter as tk


class Simpleshare(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("Simpleshare")
        self.pack()
        self.create_widgets()
    # init

    def create_widgets(self):
        self.lab = tk.Label(self, text="Simpleshare")
        self.lab.pack()
    # create_widgets


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
