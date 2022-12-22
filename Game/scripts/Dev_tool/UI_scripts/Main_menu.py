# 11/27/2022
from tkinter import *
from tkinter import ttk
from UI_scripts.Character_creator_frame import Character_creation

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
        create_character_tab = Character_creation(create_notebook)
        create_item_tab = Frame(create_notebook)
        create_map_tab = Frame(create_notebook)

        create_notebook.add(create_character_tab, text="Characters")
        create_notebook.add(create_item_tab, text="Items")
        create_notebook.add(create_map_tab, text="Maps")

        ############################ Create ############################
        #
        