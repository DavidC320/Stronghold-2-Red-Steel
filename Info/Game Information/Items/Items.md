# Items

  Items will be flag heavy for a lot of functions

## Structure

    ID - Used in creating save data
    Name
    Description
    Category
    Subcategory
    Flags - How the game will use the item internaly
    Properties - The effects that a weapon has
    Location - where is the item located

    Max_quantity
    Quantity
    Attack
    Defense
    Health
    Energy
    Speed

---

## Categories

These are the types of items in the game.
Subtypes are here to help distinguish items from one other and will auto automatically assign flags to items

---

### Medical

    Items that effect allies in the same party mostly buffing and healing members

Sub Categories

    Healing
    Revive
    Cure
    Injection


Auto Flags

    ONLY_ALLIES - This item can only be used by party members to other party members
    HEALTH_PERCENT_MAX_HEALTH - The health stat will be based off of the max health of the target

---

### Equipment

    Items that can be put on a character to change aspects.

Sub Categories

    Head
    Body
    Legs
    Feet
    Back
    Weapon

Auto Flags

    ONLY_ALLIES
    EQUIPPABLE_<slot> - This item can be equipped in a specified spot

---

### Deployable

    Items that can create other allies or stations to craft on in the overworld or in battle

Sub Categories

    Sentry
    Station

  Auto Flags

    ONLY_PARTY_SPACE - This will only work if there is a empty spot in the party in combat

---

### Other

    Items with no use or uses don't fall into the other categories.

Sub Categories

    Key
    Quest
    Material
    Ammo

---
