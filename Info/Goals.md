# Goals

## Major problem

    Do to rushing development for the combat system, the code has gotten bloated and needs to be trimmed down and more legible.

## initial problem

    revive items don't work properly because the game need to some how check if there are available targets for the item. in this case it would be if their are dead characters on the same team

##  Plan

1. Clean up the bloat in combat_2 and move_manager
   1. Reorganize everything
   2. disassemble code into functions

2. Fix how items work in the game when selecting them
