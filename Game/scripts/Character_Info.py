# 9/192022
from random import choice, randint

from Game_info import character_races
from Inventory import Equipment_item, Item_base

class Party_manager:
    def __init__(self, team_limit = 4):
        # allies
        self.team = []
        self.storage = []

        # important information
        self.team_limit = team_limit  # How many allies can be in a party at once
        self.current_member = 0
        self.used_ally_ids = []
    
    @property
    def current_ally_class(self):
        print(len(self.team))
        print(self.team[self.current_member])
        return self.team[self.current_member]

    def change_current(self, places = 1):
        party_size = len(self.team) -1
        self.current_member += places
        if self.current_member > party_size:
            self.current_member = 0
        elif self.current_member < 0:
            self.current_member = party_size -1

    def add_members(self, party_list, add_to_party = True):
        # Function to add party members into the team. This only excepts Base_Character classes and will not except anything else
        if not isinstance(party_list, list):
            party_list = [party_list]
        for member in party_list:
            if isinstance(member, Base_Character):
                if member.id == None:
                    member.id = self.generate_id()
                if add_to_party and len(self.team) < 16:
                    self.team.append(member)
                else:
                    self.storage.append(member)
            else:
                print("ERROR: This is not a base character")
                break

    def remove_from_party(self, index):
        self.team.pop(index)

    def generate_allies(self, number = 4):
        party = []
        for _ in range(number):
            name_list = ("Atex", "Vito", "Tron", "Zekos", "phole", "Dikrak", "Zulnose", "Rinin", "Pineapple", "Eqix", "Drogos", "vilies", 
            "Teknozes", "Flemo", "Hi World", "Trogan", "Mockery", "Enix", "Gobo", "Tekneka", "Inplis", "Secsar", "Floob", "Trog", "Aris",
            "Axel", "John", "Emile", "Jane", "William", "Null", "?")
            races = list(character_races.keys())
            #gets rid of none
            races.pop(races.index(None))
            race = choice(races)
            name = choice(name_list)
            member = Base_Character(None, name, race, True, 20, 20, 5, 10, 4, 2, randint(0,4), 0, randint(0,4), 0, randint(0,4), 0,)
            party.append(member)
        self.add_members(party)

    def generate_id(self):
        if len(self.used_ally_ids) == 0:
            self.used_ally_ids.append(0)
        ids = self.used_ally_ids
        ids.sort()

        id = ids[-1] + 1
        self.used_ally_ids.append(id)
        return id
#############################################################################################################################################################################
############################################################################## Base characters ##############################################################################
#############################################################################################################################################################################
class Base_Character:
    def __init__(self, id, name, race, in_party, 
    current_health, health, speed, energy, defense, attack, 
    fight_lv, fight_xp, hunt_lv, hunt_xp, cast_lv, cast_xp, 
    head = None, body = None, legs = None, l_weapon = None, r_weapon = None, l_pocket = None, r_pocket = None
    ):
        # Information
        self.id = id  # what sql row they belong to
        self.name = name
        self.race = race  # gets what weaknesses a character has
        color = character_races.get(self.race)
        self.color = color.get("color")
        self.in_party = in_party  # Bool
        self.species = None  # Strings

        # Statistics
        self.current_hp = current_health  # How much health is left
        self.hp = health  # Maximum health
        self.current_energy = energy   # How much energy is left
        self.energy = energy   # Maximum energy
        self.boosted_hitpoints = health # How much maximum health has been boosted
        self.speed = speed  # how much their action is prioritized
        self.armour = defense  # defense
        self.attack = attack  # base character damage
        
        # Proficiencies
        self.fighter_lv = fight_lv # Melee class
        self.fighter_xp = fight_xp # Int
        self.hunter_lv = hunt_lv # Ranged class
        self.hunter_xp = hunt_xp # Int
        self.caster_lv = cast_lv # Magic class
        self.caster_xp = cast_xp # Int

        # Equipment
        self.head = head  # object / None
        self.body = body # object / None
        self.legs = legs # object / None
        self.r_weapon = r_weapon  # object
        self.r_weapon = r_weapon # object
        self.l_pocket = l_pocket # object / None
        self.r_pocket = r_pocket

        # Conditions
        self.exhausted = False

        # Verifies the character
        self.check_character()

    @property
    def character_save_data(self):
        if self.weapon.name == "Fist":
            weapon = None
        else:
            weapon = self.weapon

        ally_data = ""
        player_data = (self.id, self.name, self.race, self.in_party,
        self.current_health, self.hitpoints, self.speed, self.energy, self.armour, self.attack, 
        self.head, self.body, self.legs, weapon)

        prof_data = (self.fighter_lv, self.fighter_xp, self.hunter_lv, self.hunter_xp, self.caster_lv, self.caster_xp)
        items = (self.head, self.body, self.legs, weapon)
        data = []
        for data_set in (player_data, prof_data):
            text_data = ""
            num = 0
            for stat in data_set:
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
                if num!= len(data_set) -1:
                    text += ", "
                text_data += text
                num += 1
            data.append(text_data)

        # items
        item_list = []
        for item in items:
            if item != None:
                item_list.append(item.save_data)
        data.append(item_list)
        print(data)

    @property
    def defense_calc(self):
        defense = self.armour
        for equipment in (self.head, self.body, self.legs):
             if equipment != None:
                defense += equipment.stat.get("defense")
        return defense

    @property
    def base_attack(self):
        # what is the base amount of attack a character has
        base_attack = self.attack
        if self.body != None:
            base_attack += self.body.attack
        return base_attack

    def attack_roll(self, attack_style = "Left"): 
        # gets the damage that the ally will deal
        used_class = self.weapon.p_class
        proficiency_class = {
            "fighter" : self.fighter_lv,
            "hunter" : self.hunter_lv,
            "caster" : self.caster_lv
        }
        class_level = proficiency_class.get(used_class)
        proficiency = {
            0 : (.0, .20),
            1 : (.20, .40),
            2 : (.40, .60),
            3 : (.60, .80),
            4 : (.80, 1.00)
        }
        damage_threshold = proficiency.get(class_level)

        # get weapon
        weapons = {
            "left" : (self.l_weapon.attack, self.l_weapon.accuracy),
            "right" : (self.r_weapon.attack, self.r_weapon.accuracy),
            "both" : (self.l_weapon.attack + self.r_weapon.attack, self.l_weapon.accuracy + self.r_weapon.accuracy / 2)
        }

        # getting damage
        weapon = weapons.get()
        base_attack = self.base_attack + weapon[0]
        low_damage = (base_attack * damage_threshold[0])
        high_damage = (base_attack * damage_threshold[1])
        damage = randint(round(low_damage), round(high_damage))
        
        accuracy_pull = randint(1, 100)
        if accuracy_pull > weapon[1]:
            damage = 0
        return damage

    def check_character(self):
        # checks if the current character is dead
        if self.current_hp > self.boosted_hitpoints:
            self.current_hp = self.boosted_hitpoints

        if self.current_hp <= 0:
            self.dead = True
        else:
            self.dead = False

        # checks if the weapons are usable
        if self.r_weapon == None:
            self.l_weapon = Equipment_item(None, "Fist", "Better then nothing", "weapon", "equipped", 4, accuracy=50, p_class="fighter")
        if self.r_weapon == None:
            self.r_weapon = Equipment_item(None, "Fist", "Better then nothing", "weapon", "equipped", 4, accuracy=50, p_class="fighter")
        
        self.get_weakness()

    def take_damage(self, number):
        self.current_hp -= number
        self.check_character()

    def get_weakness(self):
        self.weakness = character_races.get(self.race).get("weakness")

    def change_energy(self, number):
        self.current_energy += number
        if self.current_energy <= 0:
            self.current_energy = 0
            self.exhausted = True

        elif self.current_energy > self.energy:
            self.current_energy = self.energy
            self.exhausted = False

    def can_use_weapon(self, hand):
        items = {
            "left" : self.l_weapon,
            "right" : self.r_weapon,
            "both" : (self.l_weapon, self.r_weapon)
        }
        item = items.get(hand)
        if hand != "both":
            if item == None:
                return False
            elif item.subtype == "weapon":
                return True
        else:
            if item[0] and item[1] == None:
                return False
            elif (item[0].subtype == "weapon") and (item[1].subtype == "weapon"):
                return True

    def can_use_pocket(self, hand):
        items = {
            "left" : self.l_pocket,
            "right" : self.r_pocket,
        }
        item = items.get(hand)
        if hand != "both":
            if item == None:
                return False
            elif issubclass(item, Item_base):
                return True
            

#############################################################################################################################################################################
############################################################################## Base characters ##############################################################################
#############################################################################################################################################################################