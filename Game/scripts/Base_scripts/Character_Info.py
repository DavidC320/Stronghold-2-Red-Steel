# 9/192022
from random import randint

from Game_info import character_life_forms
from Item_info import Equipment_item, Item_base

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
        self.current_hp = current_health  # How much health is left
        self.base_hp = health  # Maximum health
        self.current_stamina = base_stamina   # How much base_stamina is left
        self.base_stamina = base_stamina   # Maximum base_stamina
        self.boosted_hitpoints = health # How much maximum health has been boosted
        self.base_speed = base_speed  # how much their action is prioritized
        self.base_defense = defense  # defense
        self.base_attack = base_attack  # base character damage
        self.inventory_slots = inventory_slots
        self.arm_slots = arm_slots
        self.pocket_slots = pocket_slots
        
        # Proficiencies
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
            self.hands.append(Equipment_item(None, "fist", "Bare hands, you feel naked.", "weapon", None, None, "equipped", ["fighter"], 1, 1, attack=5))
        
        self.weakness = character_life_forms.get(self.life_form).get("weakness")

    @property
    def check_if_dead(self):
        if self.current_hp <= 0:
            self.dead = True
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
        if self.current_stamina >= 1:
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
    @property
    def grab_weapons_in_hands(self):
        weapons = []
        for item in self.hands:
            if "equip_weapon" in item.flags:
                weapons.append(item)
        return weapons

    def grab_weapon_info(self, weapon):
        skills_used = weapon.skills

        proficiency_class = {
            "fighter" : self.fighter_lv,
            "hunter" : self.hunter_lv,
            "caster" : self.caster_lv
        }
        proficiency = {
            0 : (.0, .20),
            1 : (.20, .40),
            2 : (.40, .60),
            3 : (.60, .80),
            4 : (.80, 1.00)
        }
        low_damage = 0
        high_damage = 0
        number_of_skills_used = 0
        for skill in skills_used:
            prof = proficiency.get(proficiency_class.get(skill))
            if prof != None:
                low_damage += prof[0]
                high_damage += prof[1]
                number_of_skills_used += 1

        low_damage %= number_of_skills_used * 100
        high_damage %= number_of_skills_used * 100
        
        return weapon.attack, [low_damage, high_damage]

    def attack_roll(self, weapon_index = [0]): 
        # gets the damage that the ally will deal
        
        damage = 0
        proficiency = [0, 0]
        number_of_used = 0
        weapons = self.grab_weapons_in_hands
        for selected_weapon in weapon_index:
            weapon = weapons[selected_weapon]
            used_weapons = self.grab_weapon_info(weapon)
            damage += used_weapons[0]
            proficiency = used_weapons[1]
            number_of_used += 1

        if number_of_used != 0:
            # correcting the proficiencies
            proficiency[0] %= number_of_used * 100
            proficiency[1] %= number_of_used * 100
            damage /= number_of_used  # Average of all used weapon's damage
            
            print(proficiency, damage)

            damage = self.get_damage(damage, proficiency)
            return damage
        else:
            return 0

    def get_damage(self, weapon_damage, damage_threshold):
        # Returns a random number using the damage threshold * damage
        damage = self.attack + weapon_damage
        low_damage = round(damage * damage_threshold[0])
        high_damage = round(damage * damage_threshold[1])
        damage = randint(low_damage, high_damage)

        return damage

    def take_damage(self, number):
        # takes away jit points from the character
        # This also returns remaining damage.
        over_damage = 0
        self.current_hp -= number
        self.check_if_dead
        if self.dead:
            over_damage = self.current_hp * -1
            self.current_hp = 0
        return over_damage

    def change_stamina(self, number):
        self.current_stamina += number
        if self.current_stamina <= 0:
            self.current_stamina = 0
            self.exhausted = True

        elif self.current_stamina > self.base_stamina:
            self.current_stamina = self.base_stamina
            self.exhausted = False
            

#############################################################################################################################################################################
############################################################################## Base characters ##############################################################################
#############################################################################################################################################################################


class Status_manager:
    def __init__(self):
        self.status_effects = []

    def chance_add_effect(self, int_chance, effect):
        chance = randint(0, 100)
        print(chance, chance >= int_chance)
        if chance >= int_chance:
            self.cure_effect(effect.name)
            self.status_effects.append(effect)

    def cure_effect(self, effect_name):
        for effect in self.status_effects:
            if effect.name == effect_name:
                index =  self.status_effects.index(effect)
                self.status_effects.pop(index)

    def grab_effect_name(self, effect_name):
        for effect in self.status_effects:
            print(effect)
            if effect.name == effect_name:
                return effect
        else:
            return None

    def grab_effect_type(self, effect_type):
        effects = []
        for effect in self.status_effects:
            if effect.effect_type == effect_type:
                effects.append(effect)

    def loop_effects(self):
        for effect in self.status_effects:
            effect.length -= 1
            if effect.length < 0 and not effect.immortal:
                index =  self.status_effects.index(effect)
                self.status_effects.pop(index)


class Status_effect:
    "A object that contains status data"
    def __init__(self, name, effect_type, effect_operation, number, length, immortal= False):
        self.name = name
        self.effect_type = effect_type
        self.effect_operation = effect_operation
        self.number = number
        self.immortal = immortal
        self.length = length

"""
effect types
    redirect - changes the target to a different target
    resistance - changes how much damage is received


"""