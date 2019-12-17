# simpleshare
import sys
import tkinter as tk

from simpleshare.gui import Simpleshare
from simpleshare.cli import cli_main


# defaults
PORT = 8139
MCASTGROUP = '239.0.0.68'


def main():
    if len(sys.argv) > 1:
        try:
            cli_main(PORT, MCASTGROUP)
        except KeyboardInterrupt:
            exit(0)
    else:
        try:
            root = tk.Tk()
            app = Simpleshare(master=root)
            app.mainloop()
        except Exception as e:
            print(e)
            exit(0)
# main
