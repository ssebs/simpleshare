# simpleshare
import sys
import os
import tkinter as tk

from simpleshare.gui import Simpleshare
from simpleshare.cli import cli_main


# defaults
PORT = 8139
MCASTGROUP = '239.0.0.68'


def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))
# center_window


def main():
    if len(sys.argv) > 1:
        try:
            cli_main(PORT, MCASTGROUP)
        except KeyboardInterrupt:
            exit(0)
    else:
        try:
            root = tk.Tk()
            center_window(root, 250, 150)
            root.minsize(200, 100)
            # icon doesn't work when built...
            # cwd = sys.path[0]
            # root.iconphoto(True, tk.PhotoImage(
            #     file=os.path.join(cwd,
            #                       "simpleshare/img/simpleshare_logo.png")))

            app = Simpleshare(master=root)
            app.mainloop()
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            print(e)
            exit(0)
# main
