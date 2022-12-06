# 11/14/2022
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from UI_scripts.Main_menu import MainMenu

def openMainMenu():
    MainMenu(root)

def open_project():
    messagebox.showerror("Sorry", "This hasn't been implemented.")


root = MainMenu()

root.mainloop()
