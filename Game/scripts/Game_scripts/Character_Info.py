# 9/192022
from random import choice, randint

from Game_info import character_races
from Inventory import Equipment_item, Item_base

def build_character(dictionary):
    a = dictionary
    if isinstance(a, dict):
        character = Base_Character(
            a.get("id"), a.get("name"), a.get("race"), a.get("location"), 
            a.get("level"), a.get("xp"), a.get("health"), a.get("max_health"), a.get("speed"), a.get("energy"), a.get("defense"), a.get("attack"), 
            a.get("fighter_level"), a.get("fighter_xp"), a.get("hunter_level"), a.get("hunter_xp"), a.get("caster_level"), a.get("caster_xp"),
            a.get("head"), a.get("body"), a.get("legs"), a.get("l_weapon"), a.get("r_weapon"), a.get("l_pocket"), a.get("r_pocket")
            )
    else:
        return
    return character

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
            member = Base_Character(None, name, race, "party", None, 0, 0, randint(5, 20), 20, randint(1, 5), 20, 5, randint(1, 5), randint(0, 4), 0, randint(0, 4), 0, randint(0, 4), 0)
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
    def __init__(
    # Information
    self, id, name, race, location, species,
    # Stats
    level, xp, current_health, health, speed, energy, defense, attack, 
    # Proficiencies
    fight_lv, fight_xp, hunt_lv, hunt_xp, cast_lv, cast_xp,
    # Equipment 
    head = None, body = None, legs = None, l_weapon = None, r_weapon = None, l_pocket = None, r_pocket = None
    ):
        # Information
        self.id = id  # what sql row they belong to
        self.name = name
        self.race = race  # gets what weaknesses a character has
        self.location = location  # Bool
        self.species = species  # Strings
        color = character_races.get(self.race)
        self.color = color.get("color")

        # Statistics
        self.level = level
        self.xp = xp
        self.current_hp = current_health  # How much health is left
        self.hp = health  # Maximum health
        self.current_energy = energy   # How much energy is left
        self.energy = energy   # Maximum energy
        self.boosted_hitpoints = health # How much maximum health has been boosted
        self.speed = speed  # how much their action is prioritized
        self.armour = defense  # defense
        self.attack = attack  # base character damage
        
        # Proficiencies
        # Classes
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
        self.l_weapon = l_weapon  
        self.r_weapon = r_weapon 
        self.l_pocket = l_pocket 
        self.r_pocket = r_pocket

        # Conditions
        self.exhausted = False
        self.status_effects = []

        # Verifies the character
        self.check_character()

    @property
    def character_save_data(self):
        # This creates a SQL record
        if self.l_weapon.name == "Fist":
            l_weapon = None
        else:
            l_weapon = self.l_weapon
        if self.r_weapon.name == "Fist":
            r_weapon = None
        else:
            r_weapon = self.r_weapon
            
        player_data = (
            # Information
            self.id, self.name, self.race, self.location,
            # Statistics
            self.level, self.xp, self.current_hp, self.hp, self.speed, self.energy, self.armour, self.attack, 
            # class
            self.fighter_lv, self.fighter_xp, self.hunter_lv, self.hunter_xp, self.caster_lv, self.caster_xp,
            # Equipment
            self.head, self.body, self.legs, l_weapon, r_weapon, self.l_pocket, self.r_pocket
            )

        data = []
        for data_set in (player_data):
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

        
        items = (self.head, self.body, self.legs, l_weapon, r_weapon, self.l_pocket, self.r_pocket)

        # items
        item_list = []
        for item in items:
            if item != None:
                item_list.append(item.save_data)
        data.append(item_list)
        print(data)

    @property
    def defense_calc(self):
        # This counts how many defense points a character has
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

    def attack_roll(self, attack_style = "left"): 
        # gets the damage that the ally will deal
        weapons = {
            "left" : (self.l_weapon),
            "right" : (self.r_weapon),
            "both" : (self.l_weapon, self.r_weapon)
        }
        used_weapons = weapons.get(attack_style)
        damage = 0
        for weapon in used_weapons:
            damage += self.get_damage(weapon)
        
        return damage

    def get_damage(self, weapon):
        # gets the damage from a weapon
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
        damage_threshold = proficiency.get(proficiency_class.get(weapon.effective))

        base_damage = self.base_attack + weapon.attack
        low_damage = round(base_damage * damage_threshold[0])
        high_damage = round(base_damage * damage_threshold[1])
        damage = randint(low_damage, high_damage)

        accuracy_pull = randint(1, 100)
        if accuracy_pull > weapon.accuracy:
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
            self.l_weapon = Equipment_item(None, "Fist", "Better then nothing", "weapon", "equipped", 4, accuracy=50, effective="fighter")

        if self.r_weapon == None:
            self.r_weapon = Equipment_item(None, "Fist", "Better then nothing", "weapon", "equipped", 4, accuracy=50, effective="fighter")
        
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