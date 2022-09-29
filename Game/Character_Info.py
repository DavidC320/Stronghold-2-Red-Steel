# 9/192022
from Items import Equipment_item
from random import choice, choices, randint, random

class Base_Character:
    def __init__(self, id, name, race, current_health, health, speed, energy, defense, attack, fight_lv, fight_xp, hunt_lv, hunt_xp, cast_lv, cast_xp, head = None, body = None, legs = None, weapon = None, pocket = None):
        # Information
        self.name = name  # String
        self.id = id
        self.race = race
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
            weapon = Equipment_item("Fist", "Should get a weapon", "weapon", False, attack=6, p_class="fighter", accuracy=70)
        self.weapon = weapon # object
        # self.pocket = pocket # object

    @property
    def attack_roll(self): 
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

    @property
    def proficiency(self):
        return f"Name: {self.name}\nFighter: {self.fighter_lv}\nHunter: {self.hunter_lv}\nCaster: {self.caster_lv}"

    def check_character(self):
        # checks if the current character is dead
        if self.current_health > self.boosted_hitpoints:
            self.current_health = self.boosted_hitpoints

        if self.current_health <= 0:
            self.dead = True
        else:
            self.dead = False

    def damage(self, number):
        self.current_health -= number
        self.check_character()

    def get_weakness(self):
        self.weakness = weakness.get(self.race)


def generate_allies(number = 4):
    party = []
    for _ in range(number):
        name_list = ("Atex", "Vito", "Tron", "Zekos", "phole", "Dikrak", "Zulnose", "Rinin")
        race = choice(races)
        name = choice(name_list)
        member = Base_Character(None, name, race, 20, 20, 5, 10, 4, 2, randint(0,4), 0, randint(0,4), 0, randint(0,4), 0)
        party.append(member)
    return party

races = ("organic", "inorganic", "spectral")
elements = ("ice", "fire", "air")
weakness = {}
for race in races:
    num = races.index(race)
    weakness.update({race : elements[num]})
