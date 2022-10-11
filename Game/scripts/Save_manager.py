# 9/21/2022
import sqlite3
import os
import json

# imports from the game
from Game_info import ally_table_s, proficiencies_table_s, item_table_s, player_jason_data, character_ids, item_ids
from Character_Info import Base_Character
from Inventory import Medical_item, Equipment_item

class Save_file_manager:
    def __init__(self):
        None

    def load_save_folder(self, file_name):
        if not os.path.isdir("Saves"):
            os.mkdir("Save")
            print("Due to the save folder not existing, loading has stopped")
        else:
            self.path = f"Saves\\{file_name}"
            if os.path.isdir(self.path):

                red_flag = self.active_sql()
                if red_flag:
                    print("Player_Ally_Item.db doesn't exist so a new sql has been created")
                    self.create_sql_table()

                # SQL Data
                sql_data = self.load_sql_data()

                # Json data
                if not os.path.exists(f"{self.path}\\player_data.json"):
                    print("The player data file was missing, a new file has been created.")
                    
                json_data = self.load_json_file()

                print(sql_data, json_data)

                return  sql_data, json_data
            else:
                print("This player folder doesn't exist")


    def create_save_folder(self, file_name):
        # Creates the save data for the game
        # code form techiedelight //  checks if the save folder exists
        if not os.path.isdir("Saves"):
            os.mkdir("Save")

        path = f"Saves\\{file_name}"
        player_folder =os.path.isdir(path)

        if not player_folder:
            self.path = f"Saves\\{file_name}"
            self.active_sql()

            # SQL data
            self.create_sql_table()

            # Json data
            self.create_json_file()
            
        else:
            print("This player folder exists")

    #############################################################################################################################################################################
    ############################################################################# SQL data funtions #############################################################################
    
    def active_sql(self):
        # actives the sql database
        sql_data_path = f"{self.path}\\Player_Ally_Item.db"
        if not os.path.exists(sql_data_path):
            red_flag = True
        else:
            red_flag = False

        self.database = sqlite3.connect(sql_data_path)
        self.curser = self.database.cursor()

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
                i.get("id"), i.get("name"), i.get("description"), i.get("subtype"), i.get("item_limit"), i.get("quantity"), i.get("location"), 
                # Stats
                i.get("length"), i.get("attack"), i.get("defense"), i.get("health"), i.get("energy"), i.get("speed"), 
                # enhancements
                i.get("effective"), i.get("effects"), i.get("element"))
        return item
    
    def create_sql_table(self):
        ally_table = f"CREATE TABLE IF NOT EXISTS Allies( {ally_table_s} )"
        proficiencies_table = f"CREATE TABLE IF NOT EXISTS Skills( {proficiencies_table_s})"
        item_table = f"CREATE TABLE IF NOT EXISTS Items( {item_table_s} )"
        print(ally_table, proficiencies_table, item_table)

        # Adds the tables
        for action in (ally_table, proficiencies_table, item_table):
            self.curser.execute(action)

        self.database.commit()

    def load_sql_data(self):
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

        self.curser.execute("select id from Items order by id desc")
        item_ids = self.curser.fetchall()
        
        self.curser.execute("select id from Allies order by id desc")
        character_ids = self.curser.fetchall()

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
        return inventory, item_storage, party, ally_storage

    def save_sql_data(self):
        None

    ############################################################################# SQL data funtions #############################################################################
    #############################################################################################################################################################################

    ##############################################################################################################################################################################
    ############################################################################# JSON data funtions #############################################################################
    
    def create_json_file(self):
        with open(f"{self.path}\\player_data.json", "w") as file:
            json.dump(player_jason_data, file, indent=2, sort_keys=True)

    def load_json_file(self):
        with open(f"{self.path}\\player_data.json", "r") as data:
            player = json.load(data)
            money = player["player info"].get("money")
            difficulty = player["player info"].get("difficulty")
        return money, difficulty

    ############################################################################# JSON data funtions #############################################################################
    ##############################################################################################################################################################################
