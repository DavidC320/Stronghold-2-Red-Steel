# 9/192022
import sys
sys.path.append("Game/scripts")
sys.path.append("Game/scripts/Game_scripts")
sys.path.append("Game/scripts/Stronghold2")

# game stuff
from scripts.Stronhold2 import debug

debug_menu = debug.Debug_menu()

while True:
    action = input("Action: ")
    if action == "debug":
        debug_menu.run_debug()