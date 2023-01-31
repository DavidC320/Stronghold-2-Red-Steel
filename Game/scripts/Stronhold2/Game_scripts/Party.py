# 12/9/2022
from random import choice, randint, choices

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
        self.playable_max = 4

    def regain_stamina(self, regain):
        "Regains the stamina in all living team members"
        for index in self.get_alive[0]:
            self.team[index].change_stamina(regain)
            self.team[index].build_icon_text()

    @property
    def true_index(self):
        return self.get_alive[0][self.current_member]
    
    @property
    def current_ally(self):
        return self.team[self.true_index]


    @property
    def get_alive(self):
        "Returns a two lists"
        "A list of indexes of living members"
        "A list of indexes of dead members"
        alive_list = []
        dead_list = []
        for member in self.team:
            if member.dead:
                dead_list.append(self.team.index(member))
            else:
                alive_list.append(self.team.index(member))
        return alive_list, dead_list

    @property
    def get_playable(self):
        "Return a list of index for playable characters"
        pass

        # keeping the end index equal to or lower than the max playble
        playable_length = self.playable_max
        alive = self.get_alive[0]
        if len(alive) < playable_length:
            playable_length = len(alive)
        return alive[:playable_length]

    def display_team_icons(self, display, show_playable):
        num = 0
        for member in self.team:
            is_selected = False
            is_playable = False

            if len(self.get_alive[0]) > 0:
                if self.team.index(member) == self.get_alive[0][self.current_member]:
                    is_selected = True

            if num in self.get_playable and show_playable:
                is_playable = True

            member.display_combat_icon(display, is_playable, is_selected, show_playable)
            num += 1

    def change_current(self, places = 1):
        ran_thru_full = False
        ran_thru_playable = False

        party_size = len(self.get_alive[0]) -1
        play_size = len(self.get_playable) -1

        self.current_member += places

        if self.current_member > party_size:
            self.current_member = 0
            ran_thru_full = True

        elif self.current_member > play_size:
            ran_thru_playable = True

        elif self.current_member < 0:
            self.current_member = party_size -1

        return ran_thru_full, ran_thru_playable

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
            "Axel", "John", "Emile", "Jane", "William", "Null", "?", "Isiah", "Centrion", "Ikos", "Betar-23", "Xoncx", "Skackat")
            life_forms = list(character_life_forms.keys())
            #gets rid of none
            life_forms.pop(life_forms.index(None))
            life_form = choice(life_forms)
            name = choice(name_list)
            member = Stronghold_character(None, name, None, life_form, None, "party", 0, 0, randint(5, 20), 20, randint(1, 10), 20, randint(1, 5), randint(0, 4), 5, 2, 0, randint(0, 4), 0, randint(0, 4), 0, randint(0, 4), 0)
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
