# 9/192022
class Inventory:
    def __init__(self, inventory_limit = 20):
        self.inventory = []
        self.inventory_limit = inventory_limit
        self.stored_items = []

#############################################################################################################################################################################################
########################################################################################### Items ###########################################################################################
#############################################################################################################################################################################################
class Item_base:
    def __init__(self, id, name, desc, type, sub, limit, quant, location,
        length = None, attack = None, defense = None, health = None, energy = None, speed = None, accuracy = None,
        effective = None, effects = None, p_class = None, element = None):
        # Information
        self.id = id
        self.name = name
        self.description = desc
        self.type = type
        self.subtype = sub
        self.limit = limit
        self.quantity = quant
        self.location = location 

        self.length = length
        self.attack = attack
        self.defense = defense
        self.health = health
        self.energy = energy
        self.speed = speed
        self.accuracy = accuracy

        self.effective = effective
        self.effects = effects
        self.p_class = p_class
        self.element = element

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

    @property
    def print_data(self):
        information = ( self.id, self.name, self.description, self.type, self.subtype, self.limit, self.quantity, self.location)
        statistics = (self.length, self.attack, self.defense, self.defense, self.health, self.energy, self.speed, self.accuracy)
        enhancements = (self.effective, self.effects, self.p_class, self.element)
        print(f"information {information}\nstatistics {statistics}\nenhancements{enhancements}")

class Medical_item(Item_base):
    def __init__(
        self, id, name, desc, sub, limit, quant, location, length = None, attack = None, defense = None, health = None, energy = None, speed = None, effective = None, effects = None, element = None):
        super().__init__(id, name, desc, "medical", sub, limit, quant, location, 
        length, 
        attack, 
        defense, 
        health, 
        energy, 
        speed, 

        effective= effective, 
        effects= effects, 
        element= element)

class Equipment_item(Item_base):
    def __init__(self, id,  name, desc, sub, location, attack=None, defense=None, health=None, energy=None, speed=None, accuracy=None, effects=None, p_class=None, element=None):
        super().__init__(id, name, desc, "equipment", sub, 1, 1, location,
        
        attack= attack,
        defense= defense,
        health= health,
        energy= energy,
        speed= speed,
        accuracy= accuracy,

        effects= effects,
        p_class= p_class,
        element= element)
###############################################################################################################################################################################################
############################################################################################ Items ############################################################################################
###############################################################################################################################################################################################

##############################################################################################################################################################################################
####################################################################################### Prebuilt items #######################################################################################
##############################################################################################################################################################################################


##############################################################################################################################################################################################
####################################################################################### Prebuilt items #######################################################################################
##############################################################################################################################################################################################