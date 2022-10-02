# 9/21/2022
import sqlite3
from Game_info import ally_table_s, proficiencies_table_s, item_table_s

class Save_file_manager:
    def __init__(self):
        None

    def create_save_file(self, name):
        database = sqlite3.connect("Saves\\" + name + ".db")
        curser = database.cursor()

        ally_table = f"""CREATE TABLE IF NOT EXISTS
        Allies( {ally_table_s} )"""

        proficiencies_table = f"""CREATE TABLE IF NOT EXISTS
        Skills( {proficiencies_table_s} )"""

        item_table = f"""CREATE TABLE IF NOT EXISTS
        Items( {item_table_s} )"""

        for action in (ally_table, proficiencies_table, item_table):
            curser.execute(action)

        database.commit()
        database.close()

    def getting_column_names(self, name):
        database = sqlite3.connect("Saves\\" + name + ".db")
        curser = database.cursor()
        # Code from Alixaprodev // This code allows to get the table names. This will be used to dynamicly update existing tables.
        data = curser.execute("select * from Allies")

        names = [description[0] for description in data.description]
        print(names)

Save_file_manager().create_save_file("as")

        
