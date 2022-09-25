# 9/24/2022
# Itex
from cgitb import text
from pydoc import describe
from tkinter import *
from tkinter import Entry, Label, ttk

class Intro_tab(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        Label(self, text="This is the Itex Item Creator.").pack()

class Base_tab(ttk.Frame):
    def __init__(self, parent, mode, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        # Instructions on how it works
        self.instructions = Frame(self)
        self.instructions.grid(column=0, row=0)
        #options
        self.options = Frame(self)
        self.options.grid(column=1, row=0)
        self.section_1 = Frame(self.options)
        self.section_1.grid(column=0, row=0)
        self.section_2 = Frame(self.options)
        self.section_2.grid(column=0, row=1)
        Button(self.options, text="test", command=self.get_info).grid(column=0, row=2)

        #options stuff
        # Name
        Label(self.section_1, text="Name").pack()
        self.name = StringVar()
        Entry(self.section_1, textvariable=self.name).pack()

        # Description
        Label(self.section_1, text="Description")
        self.description = StringVar()
        Entry(self.section_1, textvariable=self.description).pack()

        # Item types
        self.type = mode
        item_types = {
            "medical" : ("medkit", "revive", "injects"),
            "equipment" : ("head", "body", "legs", "weapon")
        }
        self.subtype = Listbox(self.section_1)
        self.subtype.pack()
        num = 0
        for subtype in item_types.get(mode):
            self.subtype.insert(num, subtype)
            num += 1
        
        # setting limits
        if self.type != "equipment":
            Label(self.section_1, text="limit").pack()
            self.limit = StringVar()
            limit = Spinbox(self.section_1, from_=1, to=50, textvariable=self.limit)
            limit.pack()
        else:
            self.limit = StringVar(value="1")
        
        # quantity
        self.quantity = 1

        # custom
        self.custom = False

    def get_info(self):
        data = (self.name.get(),
        self.description.get(),
        self.type, 
        self.subtype.get(ANCHOR),
        int(self.limit.get()),
        self.quantity,
        self.custom)
        print(data)
        return data

class Medical_tab(Base_tab):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent,"medical", *args, **kwargs)



class Equipment_tab(Base_tab):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent,"equipment", *args, **kwargs)

app = Tk()

note = ttk.Notebook(app)
note.pack()

tab1 = Intro_tab(note)
tab1.pack()

tab2 = Medical_tab(note)
tab2.pack()

tab3 = Equipment_tab(note)
tab3.pack()

note.add(tab1, text="Intro")
note.add(tab2, text="Medic")
note.add(tab3, text="Equipment")

app.mainloop()