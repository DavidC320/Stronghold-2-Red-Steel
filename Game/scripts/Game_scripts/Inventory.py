# 9/192022


def item_converter(self, i):
        # converts item dictionaries into items
        item_type = i.get("type")

        if item_type == "equipment":
            item = Equipment_item(
                # Information
                i.get("id"), i.get("name"), i.get("description"), i.get("subtype"), i.get("location"), i.get("attack"), 
                # Stats
                i.get("defense"), i.get("health"), i.get("energy"), i.get("speed"), i.get("accuracy"), 
                # enhancements
                i.get("effects"), i.get("player_class"), i.get("element"))

        elif item_type == "medical":
            item = Medical_item(
                # Information
                i.get("id"), i.get("name"), i.get("description"), i.get("subtype"), i.get("item_limit"), i.get("quantity"), i.get("location"), 
                # Stats
                i.get("length"), i.get("attack"), i.get("defense"), i.get("health"), i.get("energy"), i.get("speed"), 
                # enhancements
                i.get("effective"), i.get("effects"), i.get("element"))
        return item


class Inventory:
    def __init__(self, inventory_limit = 20):
        # Items
        self.stored_items = []
        self.inventory = []

        # information
        self.inventory_limit = inventory_limit
        self.used_ally_ids = []

    def generate_id(self):
        if len(self.used_ally_ids) == 0:
            self.used_ally_ids.append(0)
        ids = self.used_ally_ids
        ids.sort()

        id = ids[-1] + 1
        self.used_ally_ids.append(id)
        return id
    
    def organize_inventories(self, t_inventory_f_storage):
        # chooses what item collection to organise
        if t_inventory_f_storage:
            self.inventory = self.organizer(self.inventory)
        else:
            self.stored_items = self.organizer(self.stored_items)

    def organizer(self, inventory):
        # separates items based if their filled
        filled_items = []
        non_filled = []
        for item in inventory:
            if item.is_full:
                filled_items.append(item)
            else:
                non_filled.append(item)
        # Goes through all of the items that aren't filled
        move_to_filled = []  # this is where the index of filled items will go to for removal
        for item in non_filled:
            item_name = item.name
            matching = []

            if not index in move_to_filled:  # skips items that are already in the move list
                for same_items in non_filled:  # creates a list of matching items by name
                    # filters
                    name_check = same_items.name == item_name  # has the same name
                    not_same_check = not same_items == item  # not the same as the main item
                    index_not_check = not non_filled.index(same_items) in move_to_filled  # not in the move list
                    not_dead = same_items.quantity != 0  # isn't zero

                    if name_check and not_same_check and index_not_check and not_dead:
                        matching.append(same_items)

                if len(matching) != 0:

                    # goes through matched items
                    for sub_item in matching:
                        if item.quantity != 0:
                            amount_have = item.quantity
                            leftovers = sub_item.change_quantity(amount_have)
                            if sub_item.is_full:  # checks to see if an item is now full and place it into filled list
                                index = non_filled.index(sub_item)
                                filled_items.append(sub_item)
                                move_to_filled.append(index)
                            item.change_quantity(-amount_have + leftovers)
                if item.quantity != 0:
                    index = non_filled.index(item)
                    filled_items.append(item)
                    move_to_filled.append(index)
        
        # removes the items that have been placed in the move list
        move_to_filled.sort(reverse=True)
        for index in move_to_filled:
            non_filled.pop(index)

        return filled_items

############################################################################################################################################################################################
######################################################################################## Items Base ########################################################################################
############################################################################################################################################################################################

class Item_base:
    def __init__(self, id, name, desc, type, sub, limit, quant, location,
        length = None, attack = None, defense = None, health = None, energy = None, speed = None, accuracy = None,
        effective = None, effects = None, element = None):
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
        self.element = element

    @property
    def save_data(self):
        information = [self.id, self.name, self.description, self.type, self.subtype, self.limit, self.quantity, self.location,
        self.length, self.attack, self.defense, self.defense, self.health, self.energy, self.speed, self.accuracy,
        self.effective, self.effects, self.p_class, self.element]

        num = 0
        data = ""
        for stat in (information):
            if isinstance(stat, str):
                text = f"'{stat}'"
            elif isinstance(stat, Item_base):
                text = f"{stat.id}"
            elif isinstance(stat, bool):
                conversions = {
                    True : "True",
                    False : "False"
                }
                text = f"'{conversions.get(stat)}'"
            elif stat == None:
                text = "?"
            else:
                text = f"{stat}"
            if num!= len(information) -1:
                    text += ", "
            data += text
            num += 1
        return data

    @property
    def is_full(self):
        # Checks if the item is full
        return self.quantity >= self.limit

    @property
    def empty_space(self):
        # returns how many clones of this item needs to be full
        return self.limit - self.quantity

    def change_quantity(self, number):
        # changes the amount of items in an item stack
        quantity = self.quantity
        quantity += number

        if quantity > self.limit:  # if the new quantity is more than 
            left_over = quantity - self.limit  # something like 30 - 20 = 10 left overs
            quantity = self.limit
        elif quantity <= 0:  # if the new quantity is below quantity  
            left_over = quantity * -1  # something like -4 * -1
            quantity = 0
        else:
            left_over = 0
        self.quantity = quantity
        return left_over

    def use_item(self, number = 1):
        # uses an item getting rid of it
        if self.quantity > 0:
            self.quantity -= number
            if self.quantity <= 0:
                del self

############################################################################################################################################################################################
######################################################################################## Items Base ########################################################################################
############################################################################################################################################################################################

############################################################################################################################################################################################
####################################################################################### Item Classes #######################################################################################
############################################################################################################################################################################################

class Medical_item(Item_base):
    def __init__(
        self, id, name, desc, sub, limit, quant, location, length = None, attack = None, defense = None, health = None, energy = None, speed = None, effective = None, effects = None):
        super().__init__(id, name, desc, "medical", sub, limit, quant, location, 
        length, 
        attack, 
        defense, 
        health, 
        energy, 
        speed, 

        effective= effective, 
        effects= effects)

class Equipment_item(Item_base):
    def __init__(self, id,  name, desc, sub, location, attack=None, defense=None, health=None, energy=None, speed=None, accuracy=None, effective = None, effects=None, element=None):
        super().__init__(id, name, desc, "equipment", sub, 1, 1, location,
        
        attack= attack,
        defense= defense,
        health= health,
        energy= energy,
        speed= speed,
        accuracy= accuracy,

        effective= effective,
        effects= effects,
        element= element)

##########################################################################################################################################################################################
###################################################################################### Item Classes ######################################################################################
##########################################################################################################################################################################################
