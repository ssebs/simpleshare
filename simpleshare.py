# simpleshare.py
import sys
import tkinter as tk

from simpleshare import cli
from simpleshare.gui import Simpleshare

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            cli()
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
