# 9/21/2022
from random import randint

from Game_scripts.Character_Info import Party_manager
from Game_scripts.Inventory import Inventory
from Game_scripts.Save_manager import Save_file_manager
from Game_scripts.Enemies import Enemy_rectangel

class Team_base:
    def __init__(self):
        self.party = Party_manager()
        self.inventory = Inventory()

class Player(Team_base):
    def __init__(self):
        super().__init__()
        # Information
        self.manager = Save_file_manager()

class Enemy(Team_base):
    def __init__(self):
        super().__init__()
        self.display_team = []

    def display_enemy_team(self, display):
        for member in self.display_team:
            member.display_character(display)
    
    def initialize_enemies(self, x_m_M, y):
        if len(self.display_team) <= 0:
            print(x_m_M)
            x_min = x_m_M[0]
            x_max = x_m_M[1]
            for member in self.party.team:
                char_rect = Enemy_rectangel(member)
                char_size = char_rect.rect.size[0] / 2  # makes sure the enemies can't get behind ui elements
                x_pos = randint(x_min + char_size, x_max - char_size)
                char_rect.rect.midbottom = (x_pos, y)
                self.display_team.append(char_rect)





