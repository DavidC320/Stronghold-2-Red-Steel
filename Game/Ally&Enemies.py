# 9/192022
from Items import Equipment_item
from random import randint

class Base_Chacter:
    def __init__(self, name, health, speed, energy, defense, attack, head, body, legs, weapon, pocket, fight, fight_lv, hunt, hunt_lv, cast, cast_lv):
        # Information
        self.name = name  # String

        # Statistics
        self.current_health = health  #Int
        self.hitpoints = health  # Int
        self.priorty = speed  # Int
        self.energy = energy   # Int
        self.armour = defense  # Int 
        self.attack = attack  # list / [Int, Int]

        self.fighter_pro = fight  # Int
        self.fighter_lv = fight_lv # Int

        self.hunter_pro = hunt # Int
        self.hunter_lv = hunt_lv # Int

        self.caster_pro = cast # Int
        self.caster_lv = cast_lv # Int

        # Equipment
        self.head = head  # object / None
        self.body = body # object / None
        self.legs = legs # object / None

        self.weapon = weapon # object
        # self.pocket = pocket # object

    @property
    def attack_roll(self): 
        # How much damage a chacter will do 
        attack_low = self.attack[0] + self.weapon.stat.get("attack")[0]
        attack_high = self.attack[1] + self.weapon.stat.get("attack")[1]
        print(attack_low, attack_high)

        # Getting the damage
        if attack_low >= attack_high:
            damage = randint(attack_low, attack_high)
        else:
            damage = attack_high
        print(damage)
        return damage

    @property
    def defense_calc(self):
        defense = self.armour
        for equipment in (self.head, self.body, self.legs):
             if equipment != None:
                defense += equipment.stat.get("defense")
        self.defense = defense
        return defense

    