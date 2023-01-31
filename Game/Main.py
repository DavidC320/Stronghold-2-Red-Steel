# 9/19/2022
import sys
sys.path.append("Game/scripts")
sys.path.append("Game/scripts/Base_scripts")
sys.path.append("Game/scripts/Stronhold2")
sys.path.append("Game/scripts/Stronhold2/Game_scripts")

# game stuff
from scripts.Stronhold2 import debug

debug_menu = debug.Debug_menu()


while True:
    debug_menu.run_debug()
    break