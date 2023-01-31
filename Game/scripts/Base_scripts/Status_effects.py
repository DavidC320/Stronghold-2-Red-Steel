# 1/29/2023
from random import randint

class Status_manager:
    def __init__(self):
        self.status_effects = []
        self.temporary_effects = []

    @property
    def get_data(self):
        for status_list in (self.status_effects, self.temporary_effects):
            for effect in status_list:
                print(effect.__dict__)

    def chance_add_effect(self, int_chance, effect):
        chance = randint(0, 100)
        print( int_chance, effect)
        print(chance <= int_chance)
        if chance <= int_chance:
            self.cure_effect(effect.name)
            if effect.length_type == "round":
                self.status_effects.append(effect)
            else:
                self.temporary_effects.append(effect)

    def cure_effect(self, effect_name):
        for effect in self.status_effects:
            if effect.name == effect_name:
                index =  self.status_effects.index(effect)
                self.status_effects.pop(index)

    def grab_effect_name(self, effect_name):
        for effect in self.status_effects:
            if effect.name == effect_name:
                return effect

    def grab_effect_type(self, effect_type):
        print(self.get_data)
        for effect_lsit in (self.status_effects, self.temporary_effects):
            for effect in effect_lsit:
                print(effect.name, effect.effect_type)
                if effect.effect_type == effect_type:
                    return effect

    def loop_effects(self):
        for effect in self.status_effects:
            effect.length -= 1
            if effect.length < 0 and not effect.immortal:
                index =  self.status_effects.index(effect)
                self.status_effects.pop(index)
        self.temporary_effects.clear()
                
    def loop_temporary_effects(self):
        for effect in self.temporary_effects:
            effect.length -= 1
            if effect.length < 0 and not effect.immortal:
                index =  self.temporary_effects.index(effect)
                self.temporary_effects.pop(index)


class Status_effect:
    "A object that contains status data"
    def __init__(self, name, effect_type, effect_operation, number, length, immortal= False, length_type = "round"):
        self.name = name
        self.effect_type = effect_type
        self.effect_operation = effect_operation
        self.number = number
        self.immortal = immortal
        self.length_type = length_type
        self.length = length

"""
effect types
    redirect - changes the target to a different target
    resistance - changes how much damage is received
    stat % - uses the base stat to change the stat

"""