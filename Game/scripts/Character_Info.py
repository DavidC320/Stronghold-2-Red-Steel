# 9/192022
from Game_info import character_races
from Inventory import Equipment_item, Item_base
from random import choice, randint

class Party_manager:
    def __init__(self, team_limit = 4):
        # allies
        self.team = []
        self.storage = []

        # important information
        self.team_limit = team_limit  # How many allies can be in a party at once
        self.current_member = 0

        self.used_ally_ids = []

    def change_current(self, places = 1):
        party_size = len(self.team)
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
                if add_to_party:
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
            name_list = ("Atex", "Vito", "Tron", "Zekos", "phole", "Dikrak", "Zulnose", "Rinin")
            races = list(character_races.keys())
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
    head = None, body = None, legs = None, weapon = None, pocket = None
    ):
        # Information
        self.id = id
        self.name = name  # String
        self.race = race  # String
        self.in_party = in_party  # Bool
        #self.species = species

        # Statistics
        self.current_health = current_health  #Int
        self.hitpoints = health  # Int
        self.boosted_hitpoints = health # Int

        self.speed = speed  # Int
        self.energy = energy   # Int
        self.armour = defense  # Int 
        self.attack = attack  # list / [Int, Int]
        
        self.get_weakness()
        self.check_character() #checks if dead

        self.fighter_lv = fight_lv # Int
        self.fighter_xp = fight_xp # Int

        self.hunter_lv = hunt_lv # Int
        self.hunter_xp = hunt_xp # Int

        self.caster_lv = cast_lv # Int
        self.caster_xp = cast_xp # Int

        # Equipment
        self.head = head  # object / None
        self.body = body # object / None
        self.legs = legs # object / None

        if weapon == None:
            weapon = Equipment_item(None, "Fist", "Better then nothing", "weapon", "equipped", 4, accuracy=50, p_class="fighter")
        self.weapon = weapon # object
        # self.pocket = pocket # object

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
    def attack_roll(self): 
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

        # getting damage
        base_attack = self.base_attack + self.weapon.attack
        low_damage = (base_attack * damage_threshold[0])
        high_damage = (base_attack * damage_threshold[1])
        damage = randint(round(low_damage), round(high_damage))
        
        accuracy_pull = randint(1, 100)
        if accuracy_pull > self.weapon.accuracy:
            damage = 0
        return damage

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

    def check_character(self):
        # checks if the current character is dead
        if self.current_health > self.boosted_hitpoints:
            self.current_health = self.boosted_hitpoints

        if self.current_health <= 0:
            self.dead = True
        else:
            self.dead = False

    def take_damage(self, number):
        self.current_health -= number
        self.check_character()

    def get_weakness(self):
        self.weakness = character_races.get(self.race).get("weakness")

#############################################################################################################################################################################
############################################################################## Base characters ##############################################################################
#############################################################################################################################################################################