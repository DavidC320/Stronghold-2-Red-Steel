# Notes

## 1/5/2023

    I'm making better progress in the new combat loop and now I'm making the menu for it.
    Attack
    Items
    Actions
    End turn

---
    I just realized that the new way I'm making the combat menu means that I can't just use a string path but I would have to make a list of indexes.

## 1/4/2023

    I need to restart the combat test and make a better version

---
    I going to need to make a better action chunk so here is the idea
    {
        "title" : "Make an Action.",
        "settings":{
            "can use" : True,
            "action" : None,
            "button style": { 
                "button display": "grid",
                "column/row" : (2, 2),
                "show buttons" : True,
            },
        }
        "buttons": (
            {},
            {},
            {},
            {},
        )
    }

## 1/2/23

    Okay I ran into an issue with displaying items in the game. I need to create ways to display selectable which includes buttons and teams but I need a spin like button option where the buttons appear and will spin around showing more buttons. I also need a way to show selected targets from either the enemy or player team
---
    Since the buttons are in a list I just need to make special ways to display them
    None - The buttons will display at the bottom of the screen in a row column style
    <target> team - The buttons will be hidden and a special cursor will highlight the selected target in a team
    spin - The buttons will appear at the bottom of the screen but if the number of buttons is greater then what can be reasonable displayed then the rest of the buttons will be hidden until the player scrolls to them.
    I believe the best way to do this for now is to make several buttons that will change information after a certain number the information will shift to the opposite direction to show the other item.
    first I need to figure out how big the buttons should be and how many can fit in the box. So I need to figure out what is the best size for the button.

## 1/1/23

    This project is becoming a very disappointing project as I'm unable complete goals on time as I've gotten burnt out on this project but I still want to work on it. I need to remember what I need to do.

    first complete the player action sequence for them to make actions so far from what I can remeber I just need to create a action builder and a a button to end a turn
    next I need to build the enemy action sequence which will be tedious.
    lastly I need to make a funtion to go through all of the actions

---

    found a new problem items inside of the player will need to be accounted for. This sucks so lets break it down.

    "player" index "2" uses "pocket" index "0" on "Enemy" index "3"

    Now I'm worried about equiping items from pockets but I can make that a feature in the future
    so I need a way to store those values effectivly. I can jsut ignore the team and index of the user but the other for I need to store something like use_action and target that builds a move.

## 12/28/2022

    Now really working on the combat system creating actions and exicutions. Also I will call all actions moves to seperate some information.
    acctions are the options a player can take to make a move
    a move is teh actiual combat action

    current goals:
    Create move builder
    Add end turn action to the action menu

    I need to make an move builder but I need to know what a move is.
    A move in this game is a action that is taken by a character to another character to another or themselves.
    so far
    move is user -> target
    now sense the game will have no idea what team the user is on, we will need to specify that.
    move is team, user -> team, target
    a move say what kind of move it is
    move is team, user action-> team, target
    now for the last part, the move needs to know the index for weapons, pockets, and iventory so these need a index but defend and someothers don't need them

## 12/27/2022

    current_created_action = 

    Actions have a user, action I.E attack, object, value, and target

    action name : {
        "can use" : bool,
        "mode" : <operation>
        "action" : <action_type>
    }

    operations
    "show selected enemy"
    "show selected ally"

    action types
    "attack"
    "run"
    "item"
    "defend"
    "end" - this  ends the action creating an acton object

    Okay here is a new issue that I'm stuck at. This action menu to used to create a action that is put into a list and later will be gone through. I need a way to create and end an action and Im stuck at the ending an action it 

## 12/25/2022

    Back for a bit just going to plan out the combat menu.
    The combat commands are created in a dictionary with this structure
    {
        "text" : "Attack",
        "Can use" : object.can_use,
        "options" : ()
    }
    With is I'll be able to create more actions in the future but I need to solve the problem of how to create actions it would have to be an option like target_alies or something.

## 12/12/2022

    I have now gotten the item class updated with some new stats.
    I found a problem again. Items now have flags and properties so I think I need to create a new table for that data which I don't like doing. But I guess I'll do this. it will be pretty much the same as the traits and abilities thing in the character so just that. Though... no.

## 12/11/2022

    I'm starting to get frustrated about a problem with items. It has to do with how the base item mostly incorporates Equipment then other item categories but I need to not worry about it. Also Equipment. i need to rethink the items in this game

## 12/10/2022

    New problem I found while making the character save data.
    Problem
    The character has 2 list equipments weapons or hands and pockets
    so there is 
    The character
    a list of items
    the item list
    so I need to make two more tables
    hands table and pockets table
    nope now just one table called 
    so it will look like
        characrter id
        location text // "hands" or "pocket"
        item id

## 12/9/2022

    current problems I can see
    1. How will I save held weapons and held items.
       a. How will I update the character data to replace or remove rows that correspond to that item. 
    2. How will I list all of a characters traits and abilities

## 12/5/2022

    So it's been a while since I have worked on this project fully because of several things that I won't get into.
    While I was gone I decided that I want to work on the dev tool for the game so I can create a bunch of stuff easily.
    I also figure out how ot solve the actions problem.
        So the actions are basically a path to the current options
