# 9/21/2022
from random import randint

from Game_scripts.Party import Party_manager
from Base_scripts.Inventory import Inventory
#from Base_scripts.Save_manager import Save_file_manager

class Team_base:
    def __init__(self):
        self.party = Party_manager()
        self.inventory = Inventory()

class Player(Team_base):
    def __init__(self):
        super().__init__()
        # Information
        #self.manager = Save_file_manager()

class Enemy(Team_base):
    def __init__(self):
        super().__init__()

    def display_field_team(self, display):
        for member in self.party.team:
            member.display_character(display)
    
    def combat_initialize_field_team(self, x_m_M, y):
        print(self.party.team)
        if len(self.party.team) > 0:
            print("more than zero")
            x_min = x_m_M[0]
            x_max = x_m_M[1]
            for member in self.party.team:
                char_size = member.rect.size[0] / 2  # makes sure the enemies can't get behind ui elements
                x_pos = randint(x_min + char_size, x_max - char_size)
                member.rect.midbottom = (x_pos, y)
                print(member.rect.midbottom)





