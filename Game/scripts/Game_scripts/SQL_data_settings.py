# 11/8/2022


def table_builder(table_dict):
    # Creates the string for building tables in sql
    keys = list(table_dict.keys())  # Grabs the keys in a dictionary then turns the keys into a list
    text = ""

    # Creates the sql table
    for key in keys:
        string = f"{key} {table_dict.get(key)}"
        
        if keys.index(key) != len(keys) - 1:
            string += ", "

        text += string
    return text


##############################################################################################################################################################################################################################################################################
################################################################################################################################## SQL Data ##################################################################################################################################
##############################################################################################################################################################################################################################################################################
sql_version = 2.1

ally_table_column = {
    "id" : "integer primary key AUTOINCREMENT",

    # Info
    "name" : "text", 
    "race" : "text",
    "location" : "text",

    #Stats
    "level" : "integer",
    "xp" : "integer",
    "health" : "integer", 
    "max_health" : "integer", 
    "speed" : "integer", 
    "energy" : "integer", 
    "defense" : "integer", 
    "attack" : "integer",

    # Equip
    "head" : "integer", 
    "body" : "integer", 
    "legs" : "integer",
    "weapon_l" : "integer",
    "weapon_r" : "integer",
    "pocket_l" : "integer",
    "pocket_r" : "integer",

    # Class
    "fighter_level" : "integer",
    "fighter_xp" : "integer",
    "hunter_level" : "integer",
    "hunter_xp" : "integer",
    "caster_level" : "integer",
    "caster_xp" : "integer"
    }
ally_table_s = table_builder(ally_table_column)


item_table_column = {
    "id" : "integer primary key AUTOINCREMENT",
    "name" : "text",
    "description" : "text",
    "type" : "text",
    "subtype" : "text",
    "quantity" : "integer",
    "item_limit" : "integer",
    "effective" : "text",
    "effects" : "text",
    "length" : "integer",
    "attack" : "integer",
    "defense" : "integer",
    "health" : "integer",
    "energy" : "integer",
    "speed" : "integer",
    "element" : "text",
    "accuracy" : "integer",
    "location" : "text"
    }
item_table_s = table_builder(item_table_column)

bool_conversion = {
    "true" : True,
    "false" : False
}

##############################################################################################################################################################################################################################################################################
################################################################################################################################## SQL Data ##################################################################################################################################
##############################################################################################################################################################################################################################################################################
