# 9/21/2022
from Character_Info import Party
from Inventory import Inventory
from Save_manager import Save_file_manager

class Player:
    def __init__(self):
        # Information
        self.manager = Save_file_manager()
        self.party = Party()
        self.inventory = Inventory()

