# 9/21/2022
import sys
sys.path.append("/Game/scripts")

from Character_Info import Party_manager
from Inventory import Inventory
from Save_manager import Save_file_manager

class Player:
    def __init__(self):
        # Information
        self.manager = Save_file_manager()
        self.party = Party_manager()
        self.inventory = Inventory()


