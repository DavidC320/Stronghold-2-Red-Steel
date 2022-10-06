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
        self.active_sql()

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

        # Get Storage items
        storage_dict = self.get_table_data("""
        Select * from Items
        where location = "storage"
        """)

        # get Inventory items
        inventory_dict = self.get_table_data("""
        Select * from Items
        where location = "inventory"
        """)

        # get equipped items
        equip_dict = self.get_table_data("""
        Select * from Items
        where location = "equipped"
        """)

        # converts items into object items
        # code snippet form finxter
        inventory = [self.item_converter(i) for i in inventory_dict] # creates a list of converted inventory items
        item_storage = [self.item_converter(i) for i in storage_dict]

        # Get's equipped items ready to be paired to allies
        equips = {}
        for i in equip_dict:
            item = self.item_converter(i)
            
            item.print_data
            equips.update({item.id : item})

        # finalize equipped items
        for ally in allies_dict:
            for slot in ("head", "body", "legs", "weapon"):
                item_id = ally.get(slot)
                if item_id != None:
                    if item_id in equips.keys():
                        ally.update({slot : equips.get(item_id)})

        # puts items that couldn't find a match into the storage
        for item in list(equips.values()):
            item_storage.append(item)

        # create the allies
        party = []
        ally_storage = []
        for a in allies_dict:
            ally = Base_Character(
                a.get("id"), a.get("name"), a.get("race"), a.get("in_party"), 
                a.get("health"), a.get("max_health"), a.get("speed"), a.get("energy"), a.get("defense"), a.get("attack"), 
                a.get("fighter_level"), a.get("fighter_xp"), a.get("hunter_level"), a.get("hunter_xp"), a.get("caster_level"), a.get("caster_xp"),
                a.get("head"), a.get("body"), a.get("legs"), a.get("weapon"))
            if ally.in_party:
                party.append(ally)
            else:
                ally_storage.append(ally)

            return item_storage, inventory, party, ally_storage


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
            self.active_sql()

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

    def active_sql(self):
        self.database = sqlite3.connect(f"{self.path}\\Player_Ally_Item.db")
        self.curser = self.database.cursor()

    def item_converter(self, i):
        # converts item dictionaries into items
        item_type = i.get("type")

        if item_type == "equipment":
            item = Equipment_item(
                # Information
                i.get("id"), i.get("name"), i.get("description"), i.get("subtype"), i.get("location"), i.get("attack"), 
                # Stats
                i.get("defense"), i.get("health"), i.get("energy"), i.get("speed"), i.get("accuracy"), 
                # enhancements
                i.get("effects"), i.get("player_class"), i.get("element"))

        elif item_type == "medical":
            item = Medical_item(
                # Information
                i.get("id"), i.get("name"), i.get("description"), i.get("subtype"), i.get("limit"), i.get("quantity"), i.get("location"), 
                # Stats
                i.get("length"), i.get("attack"), i.get("defense"), i.get("health"), i.get("energy"), i.get("speed"), 
                # enhancements
                i.get("effective"), i.get("effects"), i.get("element"))
        return item
        
Save_file_manager().create_save_folder("as")
Save_file_manager().load_save_folder("as")

        
