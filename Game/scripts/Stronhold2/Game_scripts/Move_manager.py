# 1/30/2023
from Base_scripts.Status_effects import Status_effect
from random import choices, choice, randrange
from Game_scripts.Tool_box import quick_display_text

class Character_move:
    def __init__(self, user_team, user_index, action, action_index, target_team, target_index, speed= 0):
        self.user_team = user_team
        self.user_index = user_index
        self.action = action
        self.action_index = action_index
        self.target_team = target_team
        self.target_index = target_index
        self.speed = speed

class Move_manager:
    "A class built to hand with character moves"
    def __init__(self, combat_data):
        self.music_manager = combat_data.music_manager

        self.combat_data = combat_data
        self.player = self.combat_data.player_data
        self.enemy = self.combat_data.enemy_data
        
        self.move_index = 0
        self.global_moves = []
        self.created_moves = []
        self.current_move = [None, None, None, None]
        self.starting_move = True

        self.current_display_move = (None, None)

    @property
    def move_display_time(self):
        default_time = 3000
        move_max = default_time * 10
        global_move_length = len(self.global_moves) * default_time
        if global_move_length > move_max:
            default_time = 1500
        return default_time

    ########################################################################################################################################################
    ######################################################################## set up ########################################################################
    ########################################################################################################################################################

    def reset_move_data(self):
        self.starting_move = True
        self.move_index = 0
        self.global_moves.clear()
        self.created_moves.clear()
        self.current_move = [None, None, None, None]


    @property
    def set_up_moves(self):
        "organizes the moves so by speed"
        self.starting_move = True
        self.global_moves.sort(key= self.grab_move_speed)

    ########################################################################################################################################################
    ######################################################################## set up ########################################################################
    ########################################################################################################################################################

    ########################################################################################################################################################
    #################################################################### Grab functions ####################################################################
    ########################################################################################################################################################

    def grab_action_object_lists(self, member, state):
        "Used to get item lists that the member is apart of"

        inventories = {
            "enemy" : self.enemy.inventory.inventory,
            "player" : self.player.inventory.inventory
        }

        action_list = {
            "attack" : member.grab_weapons_in_hands,
            "pocket" : member.hands,
            "inventory" : inventories.get(state)
        }
        return action_list

    
    @property
    def team_data(self):
        player = self.player
        enemy = self.enemy
        return {
            "player" : [
                player.party.team,
                player.party.get_alive,
                player.party.current_member,
                player.inventory.can_use_inventory(),
                enemy.inventory.inventory
            ],
            "enemy" : [
                enemy.party.team,
                enemy.party.get_alive,
                enemy.party.current_member,
                enemy.inventory.can_use_inventory(),
                enemy.inventory.inventory
            ]
        }

    
    def grab_move_speed(self, move):
        "Used in sorting moves"
        return move.speed


    @property
    def get_current_global_move(self):
        "Grabs the current move for displaying and interpreting"
        return self.global_moves[self.move_index]


    ########################################################################################################################################################
    #################################################################### Grab functions ####################################################################
    ########################################################################################################################################################

    #######################################################################################################################################################
    ###################################################################### Auto move ######################################################################
    #######################################################################################################################################################

    def auto_member(self):
        "Creates moves for unplayable characters"
        state = self.combat_data.state

        teams = self.team_data
        team_data = teams.get(state)
        team = team_data[0]
        living_indexes = team_data[1][0]
        start_index = team_data[2]
        can_use_inventory = team_data[3]

        for member_index in living_indexes[start_index:]:

            member = team[member_index]
            self.auto_move_maker(member, can_use_inventory, state)
            self.global_moves.extend(self.created_moves)

            self.created_moves.clear()
            if state == "player":
                next_turn = self.player.party.change_current()[0]
                if next_turn:
                    self.combat_data.state = "enemy"
                    self.auto_move = False

            elif state == "enemy":
                next_turn = self.enemy.party.change_current()[0]
                if next_turn:
                    self.combat_data.state = "moves"


    def auto_move_maker(self, member, can_use_inventory, state):
        "Creates moves for a character"
        # action
        action, index = self.auto_move_action(member, can_use_inventory, state)

        if action != "end turn":
            # target
            target_team, target_index = self.auto_move_target(member, action, index, state)

            self.current_move = [action, index, target_team, target_index]
            self.build_move(self.combat_data.state)


    def auto_move_action(self, member, can_use_inventory, state):
        "The first portion of the auto move that creates the action and the index"
        action = None
        index = None

        # gets the action
        possible_actions = member.available_actions
        if can_use_inventory:
            possible_actions.append("inventory")

        action = choices(possible_actions)[0]

        # gets the action index
        action_lists = self.grab_action_object_lists(member, state)

        if action in list(action_lists.keys()):
            index = randrange(0, len(action_lists.get(action)))

        return action, index


    def auto_move_target(self, member, action, item_index, state):
        "The last portion of the auto move that sets a target for the move"
        target_team = None
        target_index = None

        action_list = self.grab_action_object_lists(member, state)

        # creates the target
        if action == "attack":
            target_team, target_index = self.get_target("target_enemy", False, state)

        elif action == "defend":
            target_team, target_index = self.get_target("target_ally", False, state)

        elif action in list(action_list.keys()):  # if the action need items
            item = action_list.get(action)[item_index]
            target_team, target_index = self.item_get_target(item, state)

        return target_team, target_index


    def get_target(self, target_team, get_dead, state):
        "returns the string of team target and index of target"
        grab_dead = {
            True : 1,
            False : 0
        }
        targets = {
            "player" : {
                "target_ally" : "player",
                "target_enemy" : "enemy"
            },
            "enemy" : {
                "target_ally" : "enemy",
                "target_enemy" : "player"
            }
        }

        team_targets = targets.get(state)
        teams = self.team_data

        target_team = team_targets.get(target_team)
        segmented_teams = teams.get(target_team)[1]
        target_dead = grab_dead[get_dead]

        target_index = choices(segmented_teams[target_dead])[0]
        return target_team, target_index


    def item_get_target(self, item, state):
        "interprets items into moves"
        target_team = None
        target_index = None

        flags = item.flags
        target_dead = "target_dead" in flags

        if "target_ally" in flags:
            target_team, target_index = self.get_target("target_ally", target_dead, state)

        elif "target_enemy" in flags:
            target_team, target_index = self.get_target("target_enemy", target_dead, state)
        
        return target_team, target_index

    #######################################################################################################################################################
    ###################################################################### Auto move ######################################################################
    #######################################################################################################################################################

    def build_move(self, state):
        "Creates a character move that will be placed in the created move list"

        if state in ("player", "enemy"):
            character_index = {
                "player" : self.player.party.true_index,
                "enemy" : self.enemy.party.true_index
            }

            user_team = state
            user_index = character_index.get(user_team)
            user = self.team_data.get(user_team)[0][character_index.get(user_team)]

            action, action_index, target_team, target_index = self.current_move
            
            print(action)
            move = Character_move(user_team, user_index, action, action_index, target_team, target_index, user.base_speed)
            self.created_moves.append(move)
            self.spend_character_stamina(move)

    def spend_character_stamina(self, move):
        "spends the characters stamina"
        user_team = move.user_team
        user_index = move.user_index
        action = move.action
        action_index = move.action_index
        # getting member
        team = self.team_data.get(user_team)[0]
        member = team[user_index]

        # getting action
        if action == "defend":
            member.change_stamina(-4)
        else:
            ivens = self.grab_action_object_lists(member, user_team)
            used_inventory = ivens.get(action)
            item =  used_inventory[action_index]
            member.change_stamina(-item.energy_spend)
        member.build_icon_text()

    def move_player(self):
        "Plays though all of the moves"
        if not self.starting_move:
            self.move_index += 1
        self.starting_move = False

        if self.move_index > len(self.global_moves) - 1:
            self.combat_data.state = "result"
            self.starting_move = True
            self.move_index = 0
            self.global_moves.clear()

        else:
            current_move = self.get_current_global_move
            self.interpret_move(current_move)

##################################################################### Going through moves ##################################################################### 

    def interpret_move(self, move):
        "Interprets the current move"
        parties = self.team_data

        user_party = parties.get(move.user_team)[0]
        user = user_party[move.user_index]

        target_party = parties.get(move.target_team)[0]
        target_lving_party = parties.get(move.target_team)[1][0]
        print(target_lving_party)
        target = target_party[move.target_index]

        number = None
        killed = False
        target_team = move.user_team
        target_index = move.target_index
        extra = None

        action = move.action
        if not user.dead and target_lving_party:
            if target.dead:
                target = target_party[choice(target_lving_party)]

            if action == "defend":
                does_target_already_have_defend = target.status_effects.grab_effect_name("defended")

                defended_effect = Status_effect("defended", "redirect", move.user_team, move.user_index, 0)
                user.status_effects.chance_add_effect(100, defended_effect)
                self.music_manager.play_sound(0)
            
            elif action == "attack":
                does_target_already_have_defend = target.status_effects.grab_effect_name("defended")
                if does_target_already_have_defend:
                    effect = does_target_already_have_defend
                    target_team = effect.effect_operation
                    us_party = parties.get(effect.effect_operation)[0]
                    us_target = us_party[effect.number]
                    if not us_target.dead:
                        target = us_party[effect.number]
                        defender_effect = Status_effect("defender", "resistance", "damage", .5, 0, length_type="temporary")
                        target.status_effects.chance_add_effect(100, defender_effect)
                        self.music_manager.play_sound(5)
                
                number = user.attack_roll([move.action_index])
                number = target.take_damage(number)
                target.status_effects.loop_temporary_effects()
                killed = target.dead

                if killed:
                    self.music_manager.play_sound(2)
                else:
                    self.music_manager.play_sound(1)

            else:
                inventories = self.grab_action_object_lists(user, move.user_team)
                item = inventories.get(action)[move.action_index]
                extra = item.name
                for list_ef in item.use_item():
                    for effect in list_ef:
                        print(effect)
                        target.status_effects.chance_add_effect(100, effect)

                target.heal_damage()
                target.status_effects.loop_temporary_effects()


            user.build_icon_text()
            target.build_icon_text()

            self.create_display_move(user, move.user_team, target, action, extra, number, killed)

            if killed:
                self.remove_dead_actions(target_team, target_index)
            self.combat_data.next_move_start_time = self.combat_data.current_time


    def create_display_move(self, user, user_team,  target, action, extra, number = None, killing_blow = False):
        "Creates a text box to tell what is happening"
        pass
        user_name = user.name
        target_name = target.name
        action_dict = {
            "attack" : f"attacked {target_name} Dealing {number} damage!",
            "defend" : f"defended {target_name}",
            "inventory" : f"used {extra} on {target_name}"
        }

        text = f"{user_name} {action_dict.get(action)}"
        if killing_blow:
            text += " Killing them"
        self.current_display_move = (text, user_team)

    def remove_dead_actions(self, team, character_index):
        "Removes actions containing a user and user_index matching the dead character"
        for move in self.global_moves:
            if (move.user_team, move.user_index) == (team, character_index):
                self.global_moves.pop(self.global_moves.index(move))

    def display_move(self, display, rect):
        "Takes the current move grabbed form get_current_global_move to display on screen along with highlighting the user and target"
        

        color = {
            "enemy" : "#510000",
            "player" : "#035200",
            None : "White"
        }
        quick_display_text(display, self.current_display_move[0], color.get(self.current_display_move[1]), rect.center)

##################################################################### Going through moves ##################################################################### 
