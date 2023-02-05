# 9/192022
from Status_effects import Status_effect, effects


def item_converter(self, i):
        # converts item dictionaries into items
        item_category = i.get("category")

        if item_category == "equipment":
            item = Equipment_item(
                # Information
                i.get("id")
            )

        elif item_category == "medical":
            item = Medical_item(
                # Information
                i.get("id"), i.get("name"), i.get("description"), i.get("subcategory"), i.get("item_max_quantity"), i.get("quantity"), i.get("location"), 
                # Stats
                i.get("length"), i.get("attack"), i.get("defense"), i.get("health"), i.get("stamina"), i.get("speed"), 
                # enhancements
                i.get("effective"), i.get("effects"), i.get("element"))
        return item

############################################################################################################################################################################################
######################################################################################## Items Base ########################################################################################
############################################################################################################################################################################################

class Item_base:
    def __init__(self,
        id, name, desc, category, sub, flags, properties, location, skills_used,
        max_quantity, quant, inventory_slots= None, pocket_slots= None, attack = None, defense = None, health = None, stamina = None, speed = None, energy_spend= 2):

        # Information
        self.id = id
        self.name = name
        self.description = desc
        self.category = category
        self.subcategory = sub
        self.flags = flags
        self.properties = properties
        self.location = location
        self.skills = skills_used

        # Statistics
        self.max_quantity = max_quantity
        self.quantity = quant
        self.inventory_slots = inventory_slots
        self.pocket_slots = pocket_slots
        self.attack = attack
        self.defense = defense
        self.health = health
        self.stamina = stamina
        self.speed = speed
        self.energy_spend = energy_spend
        self.setup_item

        # special varablies
        self.phantom_uses = 0  # used for checkin if an item can be used without completely spending from the current amount

    def can_use(self, stamina):
        "Character stamina"
        enough_stamina = stamina >= self.energy_spend
        is_avalivble = self.quantity - self.phantom_uses > 0

        if enough_stamina and is_avalivble:
            return True
        return False

    #########
    # Setup #
    #########

    @property
    def setup_item(self):
        # sets up character

        # makes sure these are lists
        if self.properties == None:
            self.properties = []
        if self.flags == None:
            self.flags = []

        # grabs all of the flags for the item
        
        cf = category_flags.get(self.category)
        sf = subcategory_flags.get(self.subcategory)
        print(cf, sf)
        self.flags.extend(cf)
        self.flags.extend(sf)


    ###############################################################################################################################################################################
    ################################################################################## Save data ##################################################################################
    ###############################################################################################################################################################################

    @property
    def save_data(self):
        # Creates the save data for the item
        data = self.convert_stats
        item_effector_data = self.convert_effectors
        
        return data, item_effector_data

    @property
    def convert_stats(self):
        information = (self.id, self.name, self.description, self.category, self.subcategory, self.location)
        stats = (self.max_quantity, self.quantity, self.inventory_slots, self.pocket_slots, self.attack, self.defense, self.defense, self.health,
                self.stamina, self.speed)

        item_data= []
        for stat_list in information, stats:
            item_data.extend(stat_list)

        num = 0
        data = ""
        for stat in (item_data):
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
            if num!= len(item_data) -1:
                    text += ", "
            data += text
            num += 1

        return data

    @property
    def convert_effectors(self):
        other_information = (self.flags, self.skills_used)

        current_location = {
            0 : "flags",
            1 : "skills used"
        }

        item_effector_data = []
        for item_list in other_information:
            location = current_location.get(other_information.index(item_list))
            for effector in item_list:
                # Example (1, "hands", 30)
                item_effector_data.append(f"{self.id}, '{location}', {effector}")

        return item_effector_data

    @property
    def item_data(self):
        quantity = f"Qt: {self.quantity - self.phantom_uses} / {self.max_quantity}"
        spend = f"-{self.energy_spend} St"
        return quantity, spend

    ###############################################################################################################################################################################
    ################################################################################## Save data ##################################################################################
    ###############################################################################################################################################################################

    @property
    def is_full(self):
        # Checks if the item is full
        return self.quantity >= self.max_quantity

    @property
    def empty_space(self):
        # returns how many clones of this item needs to be full
        return self.max_quantity - self.quantity

    def change_quantity(self, number):
        # changes the amount of items in an item stack
        quantity = self.quantity
        quantity += number

        if quantity > self.max_quantity:  # if the new quantity is more than 
            left_over = quantity - self.max_quantity  # something like 30 - 20 = 10 left overs
            quantity = self.max_quantity
        elif quantity <= 0:  # if the new quantity is below quantity  
            left_over = quantity * -1  # something like -4 * -1
            quantity = 0
        else:
            left_over = 0
        self.quantity = quantity
        return left_over

    def use_item(self, number = 1):
        # uses an item getting rid of it
        yield self.properties
        if self.quantity > 0:
            self.quantity -= number
            self.phantom_uses -= number
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
        self, id, name, desc, sub, flags, properties, location, skills_used, 
        max_quantity, quant, health=None, energy_spend= 1):
        super().__init__(id, name, desc, "medical", sub, flags, properties, location, skills_used, 
        max_quantity, quant, health, energy_spend)

class Equipment_item(Item_base):
    def __init__(
        self, id, name, desc, sub, flags, properties, location, skills_used, 
        max_quantity, quant, inventory_slots=None, pocket_slots=None, attack=None, defense=None, health=None, stamina=None, speed=None, energy_spend= 2):
        super().__init__(
            id, name, desc, "equipment", sub, flags, properties, location, 
            skills_used, max_quantity, quant, inventory_slots, pocket_slots, attack, defense, health, stamina, speed, energy_spend)

##########################################################################################################################################################################################
###################################################################################### Item Classes ######################################################################################
##########################################################################################################################################################################################

##############
# Item flags #
##############

category_flags = {
    None : (),
    "medical" : ["target_ally"],
    "equipment": ["target_ally"],
    "deployable": ["target_self", "open_party"],
    "other": []
}
subcategory_flags = {
    None : (),
    # Medical
    "heal" : ["percent_hp"],
    "revive" : ["target_dead", "percent_hp"],
    # Equipment
    "head" : ["equip_head"],
    "body" : ["equip_body"],
    "legs" : ["equip_legs"],
    "feet" : ["equip_feet"],
    "back" : ["equip_back"],
    "weapon" : ["equip_weapon"]
}

#########
# Items #
#########

basis_items = (
    Medical_item("B-1", "Half pot", "A Small potion", "heal", None, [effects[0]], None, None, 5, 1, energy_spend= 1),
    # Medical_item("B-5", "Revive potion", "A Small potion", "revive", None, [effects[1]], None, None, 20, 1, energy_spend= 1),
    Medical_item("B-2", "Full pot", "A pretty big potion", "heal", None, [effects[2]], None, None, 5, 1, energy_spend= 1)
    )

basis_weapons = (
    Equipment_item("B-0", "fist", "Bare hands, you feel naked.", "weapon", None, None, "equipped", ["fighter"], 1, 1, attack=3),
    Equipment_item("B-3", "slingshot", "Makeshift isn't it.", "weapon", None, None, "equipped", ["hunter"], 1, 1, attack=3),
    Equipment_item("B-4", "wand", "few magic comes out ow.", "weapon", None, None, "equipped", ["caster"], 1, 1, attack=3)
)