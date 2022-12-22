# Notes

## 12/12/2022

    I have now gotten the item class updated with some new stats.
    I found a problem again. Items now have flags and properties so I think I need to create a new table for that data which I don't like doing. But I guess I'll do this. it will be pretty much the same as the traits and abilites thing in the character so just that. Though... no.

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
