# 10/16/2022 1.2.7
    Created the Tool_box file to store functions that will be used elsewhere.
    Character_info
        Reorganized variables for better legibility
        Added new variables
            left and right weapons
            left and right pockets
        The character will now verify it's data to clean the __init__ function
        The attack_roll function can now use left, right, and both weapons

    Combat
        Added the Enemy team
        created actions for combat within a dictionary
        changed the size of the control Panel
        Added the enemy team column
        display_members function can now be used by both teams
        Added draw_action_buttons to automatically add buttons to the control panel
        Greatly simplified the draw_button function
        event_controller will now use strings instead of numbers

    Created Enemies file to create enemy placeholders in the area in combat
    Player file has been deleted and replaced by Teams
    created Characters.md file to better understand how I want characters to work
    Created Goals to help prioritize

# 10/14/2022 1.2.0
    Added combat test into debug menu
    The player's team can have a max of 16 party members but can only control 4
    The  character classes health has been changed to HP for convenience
    Created the combat object to test combat
        created team member icons, includes name and health
        created buttons for actions

# 10/12/2022 Later in the day 1.1.2
    created the debug menu
    Character_info
        Characters can now get exhausted
        Characters can now lose energy
    Movement
        Running can now cause characters to lose energy
        More information on the current character 

# 10/12/2022 1.1.0 Movement test
    A lot of file moving
    created a Stronghold 2 document
    created debug file that will be used to test features
    Main file now can run the debug menu
    the Party Manager class in Character info can now grab the current selected member
    Game_info
        added colors for the different races
        added 4 new races abyss, red flesh, devoid, and None which is a fail load_save_folder
    created Movement file and it's features
    created a class test to see how getting data works
    created Movement test file to test how to make a rectangle to move

# 10/6-10/2022 1.0.0 Game tests
    Game
        started making a framework for the game

    Character_info
        updated add_members to allow auto ids
        created generate allies function
        created generate_id

    Game_info
        fixed the races to lower case
        added sql_versions
        fixed the item limit column to item_limit
        added json sql_versions
        created player_json_data dictionary
    
    Inventory
        Gave the Inventory the ability to convert item ids to numbers if none
        organize inventories has been added along with organizer
        gave items is_full and empty_space
        change_quantity has been added into base item
        gave base items save_data property

    Player
        imported sys to allow the modules within scripts to run
        changed the name of party to party manager
    
    Save_manager
        created load_save_folder
        created create_save_folder
        created functions for sql loading
        created json loading functions

    others
        created item count test

# 10/5/2022 0.5.0 json
    character_info file
        moved party into
        party_add_to_party has been changed to add_members and now can add to both party and storage
    Game_info file
        changed the names of the columns item_limit and item_max to quantity and item_limit
    Inventory file
        remodeled the inventory class to include inventory list and inventory_limit
        cleaned up all of Item classes to make it more legible
        in added the property print data in Item_base
    Player file
        added the manager and inventory into the player class
    Save_manager file
        finished creating the load_save_folder function
        created active_sql function to set file paths and database managing
        created item_converter to easily convert sql item data to item class objects

# 10/4/2022 0.4.1 Dynamic 2
    created a way to get data from a table and put it into a dictionary
    did optimized table data to dictionary conversion
    added in_party variable to the Base_Character object
    Started working on the Base_Character save data
    converted several item columns from integers into text
    added bool_conversion dictionary

# 10/2/2022 0.4.0 Dynamic
    Created dynamic tables in Game_info and save_manager
        Game_info now has ally, proficiencies, and item dictionaries
        Game_info has a table builder to easily create SQL tables
        Save_manager now has less code

# 9/28/2022
    File restructuring, forgot the changes
    added more items into the Game_info
    worked on save_manager
        Created allies
        created items

# 9/28/2022
    Character_classes has been changed to character_info
    did work in character_info
    did work in Player
    did work in saving

# 9/26/2022
    The Character_classes file has a new function to create basic characters to serve as party members.
    Created the party class in the Player file that will serve to organize and control the player's party.
        Created change party member to make changing party members easier.
        Created add party member to add more party members.
    added 1.0.0 because this is the second interaction of the game

# 9/25/2022 
    Started Changelog.
    Updated Plan.
    Started Credits.
    Updated character attack roll.
        Damage is based on proficiency, weapon attack, base attack, and accuracy. 
    added base attack to characters
    Change Allies and Enemies to Character_classes
    Finished basic character class
    made basic player class
    fixed up Items
