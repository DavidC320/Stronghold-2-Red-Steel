# 9/21/2022
from select import select
import sqlite3
import os
import _json

# imports from the game
from Game_info import ally_table_s, proficiencies_table_s, item_table_s
from Character_Info import Base_Character
from Inventory import Medical_item, Equipment_item

class Save_file_manager:
    def __init__(self):
        None

    def load_save_folder(self, file_name):
        self.path = f"Saves\\{file_name}"
        self.active_sql(file_name)

        # Grabs allies
        # SQL code from Rahul Tripathi for idea
        # Sql code from Michael Berkowski for fixes
        # This code creates a temporary table that gets the data for each stored ally in the database
        self.curser.execute("""
        create table temp as select * from Allies 
        inner join Skills on Allies.proficiencies = Skills.id
        """)

        # get ally information
        # Drops unnecessary columns // so far it's just ally_id
        self.curser.execute("Alter table temp drop column ally_id")
        allies_dict = self.get_table_data("select * from temp")
        self.curser.execute("drop table temp")
        print(allies_dict)

        # Get Storage items
        storage_dict = self.get_table_data("""
        Select * from Items
        where location = "storage"
        """)
        print(storage_dict)

        # get Inventory items
        storage_dict = self.get_table_data("""
        Select * from Items
        where location = "inventory"
        """)
        print(storage_dict)

        # get equipped items
        storage_dict = self.get_table_data("""
        Select * from Items
        where location = "equipped"
        """)
        print(storage_dict)

        


    def create_save_folder(self, file_name):
        # Creates the save data for the game
        # Code segment from Geeks for Geeks // This code allows the game to create a user folder to store data
        path = f"Saves\\{file_name}"
        try:  # Checks if a folder can be created
            os.mkdir(path)
            success = True
        except OSError as error:
            print(error)
            success = False

        if success:
            self.path = f"Saves\\{file_name}"
            self.active_sql(file_name)

            # Tables
            ally_table = f"CREATE TABLE IF NOT EXISTS Allies( {ally_table_s} )"
            proficiencies_table = f"CREATE TABLE IF NOT EXISTS Skills( {proficiencies_table_s})"
            item_table = f"CREATE TABLE IF NOT EXISTS Items( {item_table_s} )"
            print(ally_table, proficiencies_table, item_table)

            # Adds the tables
            for action in (ally_table, proficiencies_table, item_table):
                self.curser.execute(action)

            self.database.commit()
        else:
            print("Do to an error, this operation has been stopped")

    def get_table_data(self, command):
        # Gets the data from the table
        column_name = self.curser.execute(command)
        table_data = self.curser.fetchall()

        # Code from Alixaprodev // This code allows to get the table names. This will be used to dynamically get data.
        # this function will use allies as an example
        column_names = [description[0] for description in column_name.description]

        # creating a list of data
        ally_list = []
        for data in table_data:
            num = 0
            ally_section = {}

            for stat in data:  # Goes through the data to add into a dictionary using the column name
                ally_section.update({column_names[num] : stat})
                num += 1
            ally_list.append(ally_section)
        return ally_list

    def active_sql(self, file_name):
        self.database = sqlite3.connect(f"{self.path}\\Player_Ally_Item.db")
        self.curser = self.database.cursor()
        
Save_file_manager().create_save_folder("as")
Save_file_manager().load_save_folder("as")

        
