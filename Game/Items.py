# 9/24/2022
# Item class imformation

item_types = {
    "medical" : ("medkit", "revive", "boost"),
    "equipment" : ("head", "body", "legs", "weapon"),
    "throwable" : ("gernade", "bomb", "sentry"), 
    "misc" : ("quest", "key", "material")
}

class Item_base:
    def __init__(self, name, desc, type, sub, limit, quant, custom, effective, effects, length, attack, defence, health, energy, element, accuracy):
        # Information
        self.name = name
        self.desciption = desc
        self.type = type
        self.subtype = sub
        self.limit = limit
        self.quantity = quant
        self.custom = custom

        self.effective
        self.effects
        self.length
        self.attack
        self.defence
        self.health
        self.energy
        self.element
        self.accuracy

    def add_to_quantity(self, number):
        # Adds a number into the item's limit
        if self.quantity < self.limit: # checks to make sure their is space left
            self.quantity += number

    def use_item(self, number = 1):
        self.quantity -= number
        if number <= 0:
            del self

    def add_item(self, number):
        self.quantity += number
        if self.quantity >= self.limit:
            self.quantity == self.limit




