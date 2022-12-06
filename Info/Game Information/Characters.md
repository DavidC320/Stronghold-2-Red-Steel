
# Characters

Characters are the bases of enemies and allies used in this game

## Information

This is the more static data within each character

* Id - This is to add or update an SQL row
* Name - This is just the name of a character that will display at some points
* Identity - How the character is referred to when not using their name
* Composition - What they are made up of mostly affects weaknesses.
* species - What sprites will be used // set for deletion
* Mind
* Abilities
* Traits
* Weaknesses

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
* Expeierence
* Level

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

* Melee - How good they are with melee
  * Melee Level
  * Melee experience
* Ranged - How good they are with range
  * Ranged Level
  * Ranged experience
* Magic - How good they are with magic
  * Magic Level
  * Magic experience

## Equipment

This is what a character is wearing

* Head
* Body
* Legs
* Feet
* Back
* Hands
* Weapons
  * Left
  * Right
* Pocket - What item they have stored with them
  * Left
  * Right
