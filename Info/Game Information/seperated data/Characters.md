**Characters**
# General Information
Characters are the bases of enemies and allies used in this game

## Information
This is the more static data within each character
* Id - This is to add or update an SQL row
* Name - This is just the name of a character that will display at some points
* Race - This decides the weaknesses of a character
* species - What sprites will be used // set for deletion

## Statistics
This is the numbers of a character
* Health - How much damage a character can take before being knocked down
    * Current Hp
    * Hp 
* Energy - How long a character can run and what moves a character can make in combat
    * Current Energy 
    * Energy 
* Speed - How much a character's action is prioritized
* Defense - How much damage is absorbed
* Attack - The base amount of damage a character can deal

## Proficiencies
This is how good a character is with a class of weapons. These affect damage
___
Damage table
|Level|Threshold|
|-----|---------|
|0    |(0, .2)  |
|1    |(.2, .4) |
|2    |(.4, .6) |
|3    |(.6, .8) |
|4    |(.8, 1)  |
___
* Fighter - How good they are with melee
    * Fighter Level
    * Fighter experience
* Hunter - How good they are with range
    * Hunter Level
    * Hunter experience
* Caster - How good they are with magic
    * Caster Level
    * Caster experience

## Equipment
This is what a character is wearing
* Head
* Body
* Legs
* Weapons
    * Left
    * Right
* Pocket - What item they have stored with them
    * Left
    * Right

# Planned Features
Features I want to add to characters

## Information
* Nature - Affects what the character will do on auto pilot
* Abilities - What special features a character has

## Statistics

## Proficiencies

## Equipment
* Back - Affects the inventory capacity of the whole team
* Boots - Affects speed