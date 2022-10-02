# 9/192022
class Inventory:
    def __init__(self):
        self.items = []
        self.stored_items = []

#############################################################################################################################################################################################
########################################################################################### Items ###########################################################################################
#############################################################################################################################################################################################
class Item_base:
    def __init__(self, id, name, desc, type, sub, limit, quant, custom,
     effective = None, effects = None, length = None, attack = None, defense = None, health = None, energy = None, speed = None,
      p_class = None, element = None, accuracy = None):
        # Information
        self.id = id
        self.name = name
        self.description = desc
        self.type = type
        self.subtype = sub
        self.limit = limit
        self.quantity = quant
        self.custom = custom

        self.effective = effective
        self.effects = effects
        self.length = length
        self.attack = attack
        self.defense = defense
        self.health = health
        self.energy = energy
        self.speed = speed

        self.p_class = p_class
        self.element = element
        self.accuracy = accuracy

    def add_item(self, number):
        # Adds a number into the item's limit
        if self.quantity < self.limit: # checks to make sure their is space left
            self.quantity += number

    def use_item(self, number = 1):
        # uses an item getting rid of it
        if self.quantity > 0:
            self.quantity -= number
            if self.quantity <= 0:
                del self

class Medical_item(Item_base):
    def __init__(
        self, id, name, desc, sub, limit, quant, custom, effective = None, effects = None, length = None, attack = None, defense = None, health = None, energy = None, speed = None, element = None):
        super().__init__(id, name, desc, "medical", sub = sub, limit = limit, quant = quant, custom = custom,
        # What Character race will get a bonus
        effective = effective,
        # What effects an item have. Currently only affects med kit items
        effects = effects, 
        # How long a boost will last
        length = length, 
        # These stats will be boosted by a percent
        attack = attack, 
        defense = defense,
        energy = energy,
        speed = speed,
        # if the item is a medic then it's a percent heal by max health or a health boost by a percent
        health = health,
        # What status an antidote will heal
        element= element
        )

class Equipment_item(Item_base):
    def __init__(self,id,  name, desc, quant, custom, effects=None, attack=None, defense=None, health=None, energy=None, speed=None, p_class=None, element=None, accuracy=None):
        super().__init__(id, name, desc, "equipment", 1, 1, quant = quant, custom = custom,
        # What special attribute an item has
        effects=effects, 
        # stat boost
        attack=attack, 
        defense=defense, 
        health=health, 
        energy=energy, 
        speed=speed, 
        # What class an equipment belongs to
        p_class=p_class, 
        # what attribute an equipment has
        element=element, 
        # how likely a weapon is to hit
        accuracy=accuracy)
###############################################################################################################################################################################################
############################################################################################ Items ############################################################################################
###############################################################################################################################################################################################
