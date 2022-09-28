# 9/21/2022
from Character_classes import Base_Character, generate_allies

class Player:
    def __init__(self):
        None
        # Information
        self.file_name = None
        self.party = Party()

class Party:
    def __init__(self):
        self.team = []
        self.current_member = 0

    def change_current(self, places = 1):
        party_size = len(self.team)
        self.current_member += places
        if self.current_member > party_size:
            self.current_member = 0
        elif self.current_member < 0:
            self.current_member = party_size -1

    def add_to_party(self, party_list):
        # Function to add party members into the team. This only excepts Base_Character classes and will not except anything else
        if not isinstance(party_list, list):
            party_list = [party_list]
        for member in party_list:
            if isinstance(member, Base_Character):
                print("yeah")
            else:
                print("ERROR: This is not a base character")
                break



a = Player()
for _ in range(4):
    a.party.add_to_party(generate_allies(1)[0])
