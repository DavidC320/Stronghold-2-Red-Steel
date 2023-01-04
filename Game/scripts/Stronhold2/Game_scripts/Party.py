# 12/9/2022
from random import choice, randint

from Base_scripts.Game_info import character_life_forms
from Base_scripts.Item_info import Equipment_item, Item_base
from Pygame_character_class import Stronghold_character

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
    def current_ally(self):
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

            if isinstance(member, Stronghold_character):
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
            life_forms = list(character_life_forms.keys())
            #gets rid of none
            life_forms.pop(life_forms.index(None))
            life_form = choice(life_forms)
            name = choice(name_list)
            member = Stronghold_character(None, name, None, life_form, None, "party", 0, 0, randint(5, 20), 20, randint(1, 5), 20, randint(1, 5), randint(0, 4), 5, 2, 0, randint(0, 4), 0, randint(0, 4), 0, randint(0, 4), 0)
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
