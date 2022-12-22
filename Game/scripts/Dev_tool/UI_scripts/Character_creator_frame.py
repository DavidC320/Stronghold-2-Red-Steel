# 12/8/2022
from tkinter import *
from tkinter import ttk

class Character_creation(Frame):
    def __init__(self, master):
        super().__init__(master)

        # Note book
        character_notebook = ttk.Notebook(self)
        character_notebook.pack(fill= "both", expand=1)

        # Tabs
        create_character = Frame(character_notebook)
        """create_forms = Frame(character_notebook)
        create_species = Frame(character_notebook)
        create_traits = Frame(character_notebook)
        create_abilities = Frame(character_notebook)"""

        character_notebook.add(create_character, text="Create")
        """character_notebook.add(create_forms, text="Forms")
        character_notebook.add(create_species, text="Species")
        character_notebook.add(create_traits, text="Traits")
        character_notebook.add(create_abilities, text="Abilities")"""

        # character creator
        # Information
        Information_frame = Frame(create_character, border=2, relief=RAISED)
        Information_frame.grid(row=0, column=0)

        Label(Information_frame, text="Information").grid(row=0, column=0, columnspan=3)

        Label(Information_frame, text="Name:").grid(row=1, column=0)
        Entry(Information_frame).grid(row=1, column=1)

        Label(Information_frame, text="Description:").grid(row=2, column=0)
        Entry(Information_frame).grid(row=2, column=1)

        Label(Information_frame, text="From").grid(row=3, column=0)
        ttk.Combobox(Information_frame).grid(row=3, column=1)

        Label(Information_frame, text="Species").grid(row=4, column=0)
        ttk.Combobox(Information_frame).grid(row=4, column=1)

        Label(Information_frame, text="Brain").grid(row=5, column=0)
        ttk.Combobox(Information_frame).grid(row=5, column=1)

        Label(Information_frame, text="Abilities").grid(row=6, column=0)
        Listbox(Information_frame, height=3).grid(row=6, column=1)

        Label(Information_frame, text="Traits").grid(row=7, column=0)
        Listbox(Information_frame, height=3).grid(row=7, column=1)

        # user can't change weaknesses

        # Statistics
        statistics_frame = Frame(create_character, border=2, relief=RAISED)
        statistics_frame.grid(row=1, column=0)

        Label(statistics_frame, text="Statistics").grid(row=0, column=0, columnspan=3)

        Label(statistics_frame, text="Max health:").grid(row=1, column=0)
        Spinbox(statistics_frame, from_=1, to=50).grid(row=1, column=1)

        Label(statistics_frame, text="Max stamina:").grid(row=2, column=0)
        Spinbox(statistics_frame, from_=1, to=50).grid(row=2, column=1)

        Label(statistics_frame, text="Attack:").grid(row=3, column=0)
        Spinbox(statistics_frame, from_=1, to=50).grid(row=3, column=1)

        Label(statistics_frame, text="Defense:").grid(row=4, column=0)
        Spinbox(statistics_frame, from_=1, to=50).grid(row=4, column=1)

        Label(statistics_frame, text="Speed:").grid(row=5, column=0)
        Spinbox(statistics_frame, from_=1, to=50).grid(row=5, column=1)

        Label(statistics_frame, text="level:").grid(row=6, column=0)
        Spinbox(statistics_frame, from_=1, to=50).grid(row=6, column=1)

        Label(statistics_frame, text="Arm slots:").grid(row=7, column=0)
        Spinbox(statistics_frame, from_=1, to=6).grid(row=7, column=1)

