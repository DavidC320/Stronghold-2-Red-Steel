# Notes

## 2/5/2023

    Okay this will be a completely big overhaul that will have to do in order to make sure that items work all because of revives.

### Goal

Create an item selection system that allows the use of items dynamic.

---

The first issue that needs to be solved is item checks since each item needs to know if it can be used. I think the best way to do this is in combat in a function that takes the current team and member uh fuck. This needs to be rewritten.

## 2/4/2023

    This sucks... the invnetory is broken and it needs to be fxed.

## 2/3/2023

    More feedback mostly balance changes which i'm not looking at for the moment but their is a bug in the game

### Bugs

Items in the inventory always say that there is only one in a stack.

## 2/2/2023

    New style of notes so that I can use more of mark down

### Goals

1. Fix the bug where actions don't update after a round properly
2. Make fundamental changes
3. Make sure that enemies are using items correctly

## 2/1/2023

    Today I got feedback for the game that I need to organize.

    bugs
        the action menu doesn't update after a round
            I just need to add an action

    quality of life
        Lower the game volume //
        Make the move text brighter
            Really easy to implement
        Clear false selection in the menu
            This will be pretty difficult for items but this can somewhat be achivable with the living and non living system
        moves need to be visible on the arena
        battle timer
        Visualize moves
        Mouse selection
        Team commands

    balancing
        Auto end round when a team wipes
        Lower how many items are generated
        Lower stamina for test

    fundamental changes
        Add the evade stat
        Change the threshold to affect accuracy and not damage

## 1/31/2023

    Yesterday I got to show off the game so far and everyone thought it was pretty good. Got some feedback mostly on buttons. Today I need to fix the inventory because it's broken.
---
Issues

The inventory organizer is broken deleting item groups. To fix this I need to completely redo it.

## 1/29/2023

    Here are the current problems with this game.
    1. Dead characters moves where playing. Fixed
    2. Characters keep attacking dead characters
    3. Items still need to be added
        Defenders need to be able to get the .5 damage resistance
    New problems
    4. When a charter that was defending dies, the character is still targeted

---
   Dead moves
   I fixed this problem by making the move interpreter ignore dead users which wouldn't set off the move start time.

---
    Characters keep attacking dead
    This will be very difficult to fix or tedious. What is needed to fix this problem is a check for dead targets and a check for living targets.
    The first part is easy if the target is dead then select a new target using a choice function on the target living list but the check for living targets would need to do an emideate stop to the moves. so that's a clear for global moves
    Fixed I did by doing two checks. if the target is dead and if their are available targets which made the game skip those moves in the move interpreter

---
    Items need to be added
    This is the hardest part which will require a new status system. This new way of doing this will involve temporary statuses that only last a single turn not round. This will help with all other items mostly just medical as medical items like healing and reviving need to do stat changes to the target but needs to be imedfiate since all other items like boosters, deployables and weapons can have status effects attached to them making things more confusing. To do this I'll create a sperete list for tempory statuses that will be played everytime the character is used which will get rid of the temporary effect

    New problem
    The Inventory doesn't have an add item funtion in it. This is pretty odd so I need to look at that.

## 1/28/2023

    After yesterday I've given myself a break again but whatever. Now is time to interpret what I need to do before Monday. First feedback.

---
    FeedBack
    I had 5 people play the game with 3 people who gave feedback
    Mostly add Music and sfx which is fine
    but I got a balance feed back that defending should be more expensive like costing 4 stamina 
    One of them was giving me ideas that are beyond the scope of combat so I can't retain that information nor do anything with it till a long time.

---
    general
    I want to add items into the game properly. So far I have only equipment items that are already equipped. The problem is that items are built for equipment and that's about it but I need medical items usable which can't use many of the stats that the item base class has. So I'll need to rely on the status effect system that is half broken.

## 1/27/2023

    Add background music
    sfx 

## 1/26/2023

    Yesterday was an absolute fluke but I need to work on this game test.

---
    Bugs
    Sometimes when going through effects the game will say that the object that is in the effects list is not a status effect. I need to figure out what is causing this problem and fix it.
    I think it's caused by the list being empty and its grabbing a None object.
    Problem was probably fixed. It was potently caused when curing buffs so I took that out.

    When a character that was once in the available team dies, they are still playable.
    What ever is in charge of getting the current player character and  what shows as selected need to be fixed.
    I don't know if I fixed it until I can recreate the bug

---
    I've added better text to the game now it has more structured sentences

    I now need to add the ability for the menu buttons to have extra text.
    To do this need to change how the menu data is displayed.
    I'll add a new variable that can contain a list of extra text to display
    But doing this will cause overlapping problems so I need to pre-create the text locations.
    The title of the button will move to the top and the extras will fill up the empty space
    To get the extra locations I just need to take the bottom y coordinate of the title position and the bottom coordinate of the button itself.

    Now I need to see if it works with characters

## 1/25/2023

    Combat now somewhat functional where each team can now kill each other but I need to make it look better and I got to get somethings working

---
    Improvements
    Have more data in the action menu to show.
        weapons will say what skill is used and damage threshold
        Characters will have their show their health and defense

    Better move display
        More legible move interpreting I.E. "{user} attacks {target} with {weapon} dealing {damage}"

    Add a score board for fun
    show team wins and kills

    Implement
    Add Items to the game to allow characters to heal, revive, boost, or equip items which will open the inventory and pockets to the player

## 1/23/2023

    I'm running out of time and I need to get a lot of things done

    1. get move interpreter working
    2. get the moves of a character to take stamina from them
    3. get the result function working
    4. get a win and lose function

## 1/19/2023

    In the auto move function I realized that I need a way to increment who is currently selected which makes all of the auto characters moves be made by the last index for making moves.

    Also realized that when player character dies that character will still be in the playable characters area which 

## 1/18/2023

    Today I need to create the auto move system for the enemies so that they can make moves.
    Legend: // ignore, V work
    move categories
        Attack V
        Defend V
        Item //
            Pocket //
            Iventory //
        End turn V
    
    So I just need to get Attack, Defend, and End Turn for this game to be functional
    Since I have a way to make moves I should base it off of that.
    move consist of

    user_team <- static
    User_index <- static
    <These need to be randomized>
    action
    action_index
    target_team
    target_index

## 1/16/2023

    Back after a 4 day break doing modeling.

---
    Goals
    Remake the menu
    Make a end turn function for the move creator

## 1/12/2023

    Currently got the create move function done so I just need to clean out the code.
    First I need to redo how the menu works. I will change it to a object instead of a dictionary to make cleaner code and quick changes.

## 1/8/2023

    I got into an issue. I need to make an action thing

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
