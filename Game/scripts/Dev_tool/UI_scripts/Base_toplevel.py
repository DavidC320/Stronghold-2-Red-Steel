# 11/27/2022
from tkinter import *
from tkinter import ttk

class BaseMenu(Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.protocol("WM_DELETE_WINDOW", self.close_stuff)
        self.grab_set()

    def close_stuff(self):
        self.grab_release()
        self.destroy()