# 9/29/2022


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
################################################################################################################################## Game Data #################################################################################################################################
##############################################################################################################################################################################################################################################################################

item_dictionary = {
    "medical" : ("med kit", "revive", "boost", "antidote"),
    "equipment" : ("head", "body", "legs", "weapon"),
    "throwable" : ("grenade", "bomb", "sentry"), 
    "misc" : ("quest", "key", "material")
}

character_races = {
    "Organic" : {
        "species" : ("human"),
        "weakness" : ("ice")
    },
    
    "Inorganic" : {
        "species" : ("cyborg", "walker"),
        "weakness" : ("fire")
    },

    "Spectral" : {
        "species" : ("golem", "ghost"),
        "weakness" : ("air")
    },
}

# What elements are in the game
elements = ("ice", "fire", "air")

# What effects are in the game
effects = ("over heal")

# What fighting style a weapon belongs to
player_classes = ("fighter", "hunter", "caster")

# Where an item is
item_location = ("equipped", "inventory", "storage")

##############################################################################################################################################################################################################################################################################
################################################################################################################################## Game Data #################################################################################################################################
##############################################################################################################################################################################################################################################################################


##############################################################################################################################################################################################################################################################################
################################################################################################################################## SQL Data ##################################################################################################################################
##############################################################################################################################################################################################################################################################################

ally_table_column = {
    "id" : "integer primary key AUTOINCREMENT",
    "name" : "text", 
    "race" : "text",
    "in_party" : "boolean",
    "health" : "integer", 
    "max_health" : "integer", 
    "speed" : "integer", 
    "energy" : "integer", 
    "defense" : "integer", 
    "attack" : "integer", 
    "proficiencies" : "integer", 
    "head" : "integer", 
    "body" : "integer", 
    "legs" : "integer",
    "weapon" : "integer"
    }
ally_table_s = table_builder(ally_table_column)

proficiencies_table_column = {
    "id" : "integer primary key AUTOINCREMENT",
    "ally_id" : "integer references Allies (id)",
    "fighter_level" : "integer",
    "fighter_xp" : "integer",
    "hunter_level" : "integer",
    "hunter_xp" : "integer",
    "caster_level" : "integer",
    "caster_xp" : "integer"
    }
proficiencies_table_s = table_builder(proficiencies_table_column)

item_table_column = {
    "id" : "integer primary key AUTOINCREMENT",
    "name" : "text",
    "description" : "text",
    "type" : "text",
    "subtype" : "text",
    "quantity" : "integer",
    "limit" : "integer",
    "effective" : "text",
    "effects" : "text",
    "length" : "integer",
    "attack" : "integer",
    "defense" : "integer",
    "health" : "integer",
    "energy" : "integer",
    "speed" : "integer",
    "player_class" : "text",
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
