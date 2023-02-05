# 9/19/2022
from random import randint, choice, random, randrange

from Game_info import character_life_forms
from Status_effects import Status_manager
from Item_info import Equipment_item, Item_base, basis_weapons

def build_character(dictionary):
    a = dictionary
    if isinstance(a, dict):
        character = Base_Character(
            # information
            a.get("id"), a.get("name"), a.get("description"), a.get("life form"), a.get("species"), a.get("location"),
            # Statistics
            a.get("level"), a.get("xp"), a.get("current_hp"), a.get("hp"), a.get("current_stamina"), a.get("stamina"), a.get("speed"), a.get("defense"), a.get("attack"),
            a.get("arm_slots"), a.get("pocket_slots"),
            # Skills
            a.get("fighter_level"), a.get("fighter_xp"), a.get("hunter_level"), a.get("hunter_xp"), a.get("caster_level"), a.get("caster_xp"),
            # Equipment
            a.get("head"), a.get("body"), a.get("legs"), a.get("feet"), a.get("back"), a.get("hands"), a.get("pockets"))
    else:
        return
    return character

#############################################################################################################################################################################
############################################################################## Base characters ##############################################################################
#############################################################################################################################################################################

class Base_Character:
    def __init__(
    # Information
    self, id, name, description, life_form, species, location,
    # Stats
    level, xp, current_health, health, base_speed, base_stamina, defense, base_attack, inventory_slots, arm_slots, pocket_slots,
    # Proficiencies
    fight_lv, fight_xp, hunt_lv, hunt_xp, cast_lv, cast_xp,
    # Equipment 
    head= None, body= None, legs= None, feet= None, back= None, hands= None, pockets= None
    ):
        # Information
        self.id = id  # what sql row they belong to
        self.name = name
        self.description = description
        self.life_form = life_form  # gets what weaknesses a character has
        self.species = species  # Strings
        self.location = location

        # Statistics
        self.level = level
        self.xp = xp

        self.current_hp = current_health
        self.base_hp = health

        self.current_stamina = base_stamina
        self.base_stamina = base_stamina

        self.base_speed = base_speed
        self.base_defense = defense
        self.base_attack = base_attack

        self.inventory_slots = inventory_slots
        self.arm_slots = arm_slots
        self.pocket_slots = pocket_slots
        
        # Skills
        # Melee
        self.fighter_lv = fight_lv
        self.fighter_xp = fight_xp
        # Ranged
        self.hunter_lv = hunt_lv
        self.hunter_xp = hunt_xp
        # Magic
        self.caster_lv = cast_lv
        self.caster_xp = cast_xp

        # Equipment
        self.head = head 
        self.body = body 
        self.legs = legs 
        self.feet = feet
        self.back = back

        # lists
        self.hands = hands
        self.pockets = pockets

        # Conditions
        self.dead = False
        self.exhausted = False
        self.status_effects = Status_manager()

        # Verifies the character
        self.check_character()


    ###############################################################################################################################################
    #################################################################### Setup ####################################################################
    ###############################################################################################################################################

    def check_character(self):
        # Sets the current hp to hp
        if self.current_hp > self.base_hp:
            self.current_hp = self.base_hp

        self.check_if_dead

        if not isinstance(self.hands, list):
            self.hands = []
            
        if not isinstance(self.pockets, list):
            self.pockets = []

        unused_slots = self.arm_slots + len(self.hands)
        # Adds default items into unused slots in the character
        for _ in range(unused_slots):
            self.hands.append(choice(basis_weapons))
        
        self.weakness = character_life_forms.get(self.life_form).get("weakness")

    @property
    def check_if_dead(self):
        if self.current_hp <= 0:
            self.dead = True
            self.current_hp = 0
        else:
            self.dead = False

    ###############################################################################################################################################
    #################################################################### Setup ####################################################################
    ###############################################################################################################################################

    ###############################################################################################################################################
    ################################################################## Save Data ##################################################################
    ###############################################################################################################################################
    @property
    def character_save_data(self):
        character_data = self.convert_stats
        slot_items_data = self.convert_slot_items
        items_data = self.convert_items

        
        return character_data, slot_items_data, items_data[0], items_data[1]
    
    @property
    def convert_stats(self):
        # This coverts all of the characters stats into sql conpatible data.
        # Warning! This does not convert items in hands or pocket slots

        # information
        information_data = (self.id, self.name, self.description, self.life_form, self.species, self.location)
        # Statistics
        statistics_data = (self.level, self.xp, self.current_hp, self.base_hp, self.current_stamina, self.base_stamina, self.base_speed, self.base_defense, 
                        self.base_attack, self.inventory_slots, self.arm_slots, self.pocket_slots)
        # Proficiencies
        proficiencies_data = (self.fighter_lv, self.fighter_xp, self.hunter_lv, self.hunter_xp, self.caster_lv, self.caster_xp)
        # body Equipment
        body_equipment = (self.head, self.body, self.legs, self.feet, self.back)

        information = []
        for stat_list in (information_data, statistics_data, proficiencies_data, body_equipment):
            information.extend(stat_list)

        num = 0
        character_data = ""
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
            character_data += text
            num += 1
        return character_data

    @property
    def convert_items(self):
        # Creates sql conpatible data for all items including hands and pocket slots
        body_equipment = (self.head, self.body, self.legs, self.feet, self.back)
        hands = self.hands
        pockets = self.pockets
        items_data = []
        item_effector_data = []
        for item_list in (body_equipment, hands, pockets):
            for item in item_list:
                if item != None:
                    item.location = "equipped"
                    data = item.save_data
                    items_data.append(data[0])
                    item_effector_data.extend(data[1])

        return items_data, item_effector_data

    @property
    def convert_slot_items(self):
        hands = self.hands
        pockets = self.pockets

        current_location = {
            0 : "hands",
            1 : "pockets"
        }

        slot_items = (hands, pockets)
        slot_item_data = []
        for item_list in slot_items:
            location = slot_items.index(item_list)
            for item in item_list:
                # Example (1, "hands", 30)
                slot_item_data.append(f"{self.id}, '{current_location.get(location)}', {item.id}")
        
        return slot_item_data
    
    ###############################################################################################################################################
    ################################################################## Save Data ##################################################################
    ###############################################################################################################################################

    ################################################################################################################################################
    ############################################################### calculated stats ###############################################################
    ################################################################################################################################################

    @property
    def defense(self):
        # This counts how many defense points a character has
        defense = self.base_defense
        for equipment in (self.head, self.body, self.legs, self.feet, self.back):
             if equipment != None:
                defense += equipment.defense

        return defense

    @property
    def attack(self):
        # what is the base amount of base_attack a character has
        base_attack = self.base_attack
        for item in (self.head, self.body, self.legs, self.feet, self.back):
            if item != None:
                base_attack += self.body.base_attack

        return base_attack

    ################################################################################################################################################
    ############################################################### calculated stats ###############################################################
    ################################################################################################################################################

    ################################################################################################################################################
    #################################################################### Checks ####################################################################
    ################################################################################################################################################

    @property
    def can_use_weapon(self):
        # sees if this character can use weapons
        if len(self.grab_weapons_in_hands) != 0:
            stamina_use = self.grab_weapons_in_hands[0].energy_spend
            for weapon in self.grab_weapons_in_hands:
                if stamina_use > weapon.energy_spend:
                    stamina_use = weapon.energy_spend
            return self.current_stamina >= stamina_use
        return False

    @property
    def can_use_pocket(self):
        # sees if there are items in the characters pockets
        if len(self.pockets) != 0:
            return True
        return False

    @property
    def can_use_defend(self):
        if self.current_stamina >= 4:
            return True
        return False

    @property
    def available_actions(self):
        action_list = ["end turn"]
        if self.can_use_weapon:
            action_list.append("attack")
        if self.can_use_pocket:
            action_list.append("pocket")
        if self.can_use_defend:
            action_list.append("defend")
        return action_list

    ################################################################################################################################################
    #################################################################### Checks ####################################################################
    ################################################################################################################################################

    ################################################################################################################################################
    ############################################################## Damage Calculation ##############################################################
    ################################################################################################################################################

    def grab_weapon_info(self, weapon : Equipment_item):
        "Grabs the data from the weapon and interprests the skills used"
        "returns damage and skill power"
        skills_used = weapon.skills

        skills = {
            "fighter" : self.fighter_lv,
            "hunter" : self.hunter_lv,
            "caster" : self.caster_lv
        }
        proficiency = {
            None : 0,
            0 : 2,
            1 : 4,
            2 : 6,
            3 : 8,
            4 : 10
        }
        skill_power = 0
        number_of_skills_used = 0

        for skill in skills_used:
            prof = proficiency.get(skills.get(skill))
            skill_power = prof
            number_of_skills_used += 1

        skill_power /= number_of_skills_used
        
        return weapon.attack, round(skill_power)

    def get_damage(self, weapon_damage, accuracy):
        # Returns a random number using the damage threshold * damage
        damage = self.attack + weapon_damage

        chance_land =  randint(0, 10)
        if chance_land <= accuracy:
            return damage
        else:
            return 0 

    def attack_roll(self, weapon_index : list = [0]) -> int: 
        "Grabs the the skills and damage from weapons in a list to return a damage number"
        weapon_damage = 0
        proficiency = 0
        number_of_used = 0
        weapons = self.grab_weapons_in_hands

        for selected_weapon_index in weapon_index:
            weapon = weapons[selected_weapon_index]

            used_weapons_info = self.grab_weapon_info(weapon)
            weapon_damage += used_weapons_info[0]

            proficiency += used_weapons_info[1]

            number_of_used += 1

        if number_of_used != 0:
            # correcting the proficiencies
            proficiency /= number_of_used  
            weapon_damage /= number_of_used  # Average of all used weapon's damage

            damage = self.get_damage(weapon_damage, proficiency)

        return damage

    ################################################################################################################################################
    ############################################################## Damage Calculation ##############################################################
    ################################################################################################################################################


    def weapon_data(self, weapon):
        damage, pro = self.grab_weapon_info(weapon)
        quantity = f"{weapon.quantity} / {weapon.max_quantity}"
        text = (
            weapon.skills, 
            f"Dm: {damage} + {self.attack}", 
            f"Ac: {pro}", 
            f"qt: {quantity}", 
            f"-{weapon.energy_spend} st"
        )
        return text

    @property
    def grab_weapons_in_hands(self):
        weapons = []
        for item in self.hands:
            if "equip_weapon" in item.flags:
                weapons.append(item)
        return weapons

    def heal_damage(self):
        "Place holder for applying effects to characters"
        stat_effect = self.status_effects.grab_effect_type("stat %")
        if stat_effect:
            if stat_effect.effect_operation == "health":
                self.current_hp += round(self.base_hp * stat_effect.number)
                if self.current_hp > self.base_hp:
                    self.current_hp = self.base_hp

    def take_damage(self, damage):
        "Takes the number and subtracts it from the character"
        "If the Character has a resistance it will multiply it to the damage"

        resistance_effect = self.status_effects.grab_effect_type("resistance")
        if resistance_effect:
            damage * resistance_effect.number

        self.current_hp -= damage
        self.check_if_dead
        return damage

    def change_stamina(self, number):
        self.current_stamina += number
        if self.current_stamina <= 0:
            self.current_stamina = 0
            self.exhausted = True
#im a marsh man moo mmo meow you know its me okay by jeff......my names jeffthe cide will start in 300 years yep easter egg
        elif self.current_stamina > self.base_stamina:
            self.current_stamina = self.base_stamina
            self.exhausted = False
            

#############################################################################################################################################################################
############################################################################## Base characters ##############################################################################
#############################################################################################################################################################################
