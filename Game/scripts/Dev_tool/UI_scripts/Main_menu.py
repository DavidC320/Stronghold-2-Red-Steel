# 11/27/2022
from tkinter import *
from tkinter import ttk

class MainMenu(Tk):
    def __init__(self):
        super().__init__()
        self.title("StrongHold 2 Dev Tool.")
        # menu
        menu_bar = Menu(self)
        self.config(menu= menu_bar)

        options = Menu(menu_bar)

        menu_bar.add_cascade(label="Options", menu=options)

        #
        ########################### controls ###########################

        # Control Notebook
        controller_book = ttk.Notebook(self)
        controller_book.pack(expand=1, fill='both')

        # Control Tabs
        controller_tab_welcome = Frame(controller_book)
        controller_tab_create = Frame(controller_book)
        controller_book.add(controller_tab_welcome, text="Welcome")
        controller_book.add(controller_tab_create, text="Create Mod")

        ########################### controls ###########################
        #

        #
        ############################ Create ############################

        # Create Notebook
        create_notebook = ttk.Notebook(controller_tab_create)
        create_notebook.pack(expand=1, fill='both')

        # Create Tabs
        create_ally_tab = Frame(create_notebook)
        create_enemy_tab = Frame(create_notebook)
        create_item_tab = Frame(create_notebook)

        create_notebook.add(create_ally_tab, text="Allies")
        create_notebook.add(create_enemy_tab, text="Enemies")
        create_notebook.add(create_item_tab, text="Items")

        ############################ Create ############################
        #

        
        