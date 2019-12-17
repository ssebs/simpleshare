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


# If running the file directly
if __name__ == "__main__":
    root = tk.Tk()
    app = Simpleshare(master=root)
    app.mainloop()
