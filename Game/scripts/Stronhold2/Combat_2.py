# 1/2/2023
import pygame
from random import choices, randrange

from Game_scripts.Teams import Enemy
from Game_scripts.Tool_box import quick_display_text, create_timer, create_text
from Base_scripts.Character_Info import Status_effect

class Character_move:
    def __init__(self, user_team, user_index, action, action_index, target_team, target_index, speed= 0):
        self.user_team = user_team
        self.user_index = user_index
        self.action = action
        self.action_index = action_index
        self.target_team = target_team
        self.target_index = target_index
        self.speed = speed

class Menu_action:
    "Creates a section of the action menu to display in the game"
    def __init__(self,
    title,
    extra_text = [],
    can_use= True, 
    move= None, target= None, end_type= None, 
    button_display= "grid", column_row= (2, 1), show_buttons= True, 
    options = []):
        self.title = title
        self.extra_text = extra_text
        
        # settings
        self.can_use = can_use

        # action
        # When this button is pressed, anything that is not None will replace what ever it says.
        self.move = move
        self.target = target
        self.end_type = end_type

        # button style
        self.button_display = button_display
        self.column_row = column_row
        self.show_buttons = show_buttons

        self.options = options 

class Move_manager:
    "A class built to hand with character moves"
    def __init__(self, combat_data):

        self.combat_data = combat_data
        self.player = self.combat_data.player_data
        self.enemy = self.combat_data.enemy_data
        
        self.move_index = 0
        self.global_moves = []
        self.created_moves = []
        self.current_move = [None, None, None, None]
        self.starting_move = True

        self.current_display_move = (None, None)

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
            action, action_index, target_team, target_index = self.current_move
            move = Character_move(user_team, user_index, action, action_index, target_team, target_index)
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
            member.change_stamina(-1)
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
        self.combat_data.next_move_start_time = self.combat_data.current_time

##################################################################### Going through moves ##################################################################### 

    def interpret_move(self, move):
        "Interprets teh current move"
        parties = self.team_data

        user_party = parties.get(move.user_team)[0]
        user = user_party[move.user_index]

        target_party = parties.get(move.target_team)[0]
        target = target_party[move.target_index]

        number = None
        killed = False
        target_team = move.user_team
        target_index = move.target_index

        action = move.action
        if action == "defend":
            does_target_already_have_defend = target.status_effects.grab_effect_name("defended")
            if does_target_already_have_defend:
                effect = does_target_already_have_defend
                us_party = parties.get(effect.effect_operation)
                us_user = us_party[effect.number]
                us_user.status_effects.cure_effect("defender")

            defended_effect = Status_effect("defended", "redirect", move.user_team, move.user_index, 0)
            defender_effect = Status_effect("defender", "resistance", "damage", .5, 0)
            user.status_effects.chance_add_effect(100, defender_effect)
            target.status_effects.chance_add_effect(100, defended_effect)
        
        elif action == "attack":
            does_target_already_have_defend = target.status_effects.grab_effect_name("defended")
            if does_target_already_have_defend:
                effect = does_target_already_have_defend
                target_team = effect.effect_operation
                us_party = parties.get(effect.effect_operation)
                target = us_party[effect.number]
            
            number = user.attack_roll()
            target.take_damage(number)
            killed = target.dead
        else:
            "Not now"
        user.build_icon_text()
        target.build_icon_text()

        self.create_display_move(user, move.user_team, target, action, number, killed)
        if killed:
            self.remove_dead_actions(target_team, target_index)


    def create_display_move(self, user, user_team,  target, action, number = None, killing_blow = False):
        "Creates a text box to tell what is happening"
        pass
        user_name = user.name
        target_name = target.name
        action_dict = {
            "attack" : f"attacked Dealing {number} damage!",
            "defend" : f"defended {target_name}"
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
        print("ooh")

    def display_move(self, display, rect):
        "Takes the current move grabbed form get_current_global_move to display on screen along with highlighting the user and target"
        

        color = {
            "enemy" : "#510000",
            "player" : "#035200",
            None : "White"
        }
        quick_display_text(display, self.current_display_move[0], color.get(self.current_display_move[1]), rect.center)

##################################################################### Going through moves ##################################################################### 


################################################################################################################################################################
############################################################################ Combat ############################################################################
################################################################################################################################################################


class Combat:
    def __init__(self, display, clock, player):
        # screen
        
        self.display = display
        # clock I have no idea what this does
        self.clock = clock
        self.clock.tick(60)
        self.display_size = self.display.get_size()

        # teams
        self.player_data = player
        self.enemy_data = Enemy()
        if len(self.enemy_data.party.team) <= 0:
            self.enemy_data.party.generate_allies()

        # UI
        self.control_panel = pygame.Rect(150, 460, self.display_size[0] - 300, 300)  # control panel
        self.action_buttons = []
        self.action_text_list = []
        self.map = pygame.Rect(0, 0, self.display_size[0], 160)  # map bar
        self.player_team = pygame.Rect(0, 160, 150, self.display_size[1] - 160)  # player party
        self.arena_screen = pygame.Rect(150, 160, self.display_size[0] - 300, 300)  # arena screen
        self.control_panel = pygame.Rect(150, 460, self.display_size[0] - 300, 300)  # control panel
        self.enemy_team = pygame.Rect(self.display_size[0] - 150, 160, 150, self.display_size[1] - 160)  # Enemy party

        # current options
        self.move_menu = {}
        self.move_path = []
        self.info_list= []
        self.button_grid = [3, 2] # column / row
        self.current_selection = 0
        self.button_style = "spin"
        self.true_spin = False
        self.info_len = 0

        # battle states
        self.state_list = ("Intro", "Player", "Enemy", "moves", "result")
        self.state = "Intro"
        self.run_combat = True
        self.auto_move = False

        # moves
        self.move_manager = Move_manager(self)

        # set up enemies
        self.area_limit = (self.arena_screen.x, self.arena_screen.x + self.arena_screen.width)

        # time
        self.current_time = 0
        self.next_move_start_time = 0

        # configure
        self.one_move = False
        self.debug = True
        self.scores = [0, 0]

    ########################################################################################################################################################################################################
    ################################################################################################# Menu #################################################################################################
    ########################################################################################################################################################################################################

    # ////////////////////// Build functions
    # UI --
    def build_buttons(self):
        if self.button_style == "grid":
            self.build_grid_buttons()
        elif self.button_style == "spin":
            self.build_spin_buttons()
        
        self.build_info()

    def build_grid_buttons(self):
        # creates the grid buttons
        # getting button size
        self.true_spin = False
        control_size = self.control_panel.size
        button_width = control_size[0] /self.button_grid[0]
        button_height = control_size[1] /self.button_grid[1]
        button_size = (button_width, button_height)

        # creates the buttons
        button_list = []
        starting_x_pos = self.control_panel.topleft[0]
        pos = list(self.control_panel.topleft)
        start_index = 0
        for num in range(len(self.info_list)):
            # changes the row when the the buttons reach the end of the control panel
            if pos[0] >= self.control_panel.topright[0]:
                pos[0] = starting_x_pos 
                pos[1] += button_size[1]

            button = pygame.Rect(pos[0], pos[1], button_size[0], button_size[1])
            pos[0] += button_size[0]
            start_index += 1
            button_list.append((button, num))

        self.action_buttons = button_list
  
    def build_spin_buttons(self):
        # Creates the spin buttons

        # checks if the number is greater than ir less than 5
        number = len(self.info_list)
        number_of_buttons = number
        index_offset = 0
        if number > 5:
            self.true_spin = True
            number_of_buttons = 5
            index_offset = self.current_selection -2 
        else:
            self.true_spin = False

        # getting the position offset for the buttons to make sure the buttons are centered.
        total_button_width = 120 * number_of_buttons
        pos_offset = (self.control_panel.size[0] - total_button_width)/2

        # creates the buttons
        button_list = []
        pos = list(self.control_panel.topleft)
        pos[0] += pos_offset
        button_size= [120, 300]
        start_index = index_offset
        for _ in range(number_of_buttons):

            if start_index < 0:
                start_index = number + start_index
            elif start_index > number:
                start_index = 0 

            button = pygame.Rect(pos[0], pos[1], button_size[0], button_size[1])
            pos[0] += button_size[0]
            if start_index + 1 > len(self.info_list):
                start_index = 0
            num = start_index
            start_index += 1
            button_a = [button, num]
            button_list.append(button_a)

        self.action_buttons = button_list
    
    def build_info(self):
        # shows the info inside fo the buttons
        # creates the text info
        info_list = []
        if self.true_spin:
            info_index = self.current_selection -2 
        else:
            info_index = 0

        for button in self.action_buttons:

            # makes sure that the index doesn't go over to nonextant info
            if info_index > len(self.info_list) - 1:
                info_index = 0
            # getting the location of 
            texts = []
            if self.info_list[info_index].extra_text:
                print(button)
                print(button[0].midtop)
                x, y = button[0].midtop
                title_info = [self.info_list[info_index].title, (x, y+ 10)]
                texts.append(title_info)

                # getting the range of availbe space
                text_rect = create_text(self.info_list[info_index].title, "white", (x, y+ 10))[1]
                text_bottom_pos = text_rect.bottom
                button_bottom_pos = button[0].bottom
                size_range = (button_bottom_pos - text_bottom_pos)/2
                print(size_range, text_bottom_pos, button_bottom_pos)
                offset = int(size_range / len(self.info_list[info_index].extra_text))

                num = 0
                for data in self.info_list[info_index].extra_text:
                    true_offset = (y+10) + offset + (num) * offset


                    pos = (x, true_offset)
                    texts.append((data, pos))
                    num += 1


            else:
                title_info = [self.info_list[info_index].title, button[0].center]
                texts.append(title_info)

            info_list.extend(texts)
            info_index += 1

        self.action_text_list = info_list
    
    # UI --

    #########################################################################################################################################################################
    ############################################################################## Action Menu ##############################################################################
    def build_team_menu_action(self, team= "player", dead= False):
        teams = {
            "player" : self.player_data.party.team,
            "enemy" : self.enemy_data.party.team
        }
        team_menu = []
        for member in teams.get(team):
            can_use_dict = {
                False : not member.dead,
                None : True,
                True : member.dead
            }
            can_use = can_use_dict.get(dead)
            health = f"Hp {member.current_hp} / {member.base_hp}"
            team_menu.append(Menu_action(member.name, extra_text=[health], can_use=can_use, target= team, end_type= "move"))
        return team_menu

    def build_move_action(self, items):

        weapon_menu = []
        for item in items:
            weapon_menu.append(Menu_action(item.name, can_use=True, move="attack", button_display="spin", show_buttons= False, options= self.build_team_menu_action("enemy")))
        return weapon_menu

    def build_move_menu(self):
        # creates the action menu for the the character
        member = self.player_data.party.current_ally

        weapons_menu = self.build_move_action(member.grab_weapons_in_hands)

        end_move_menu = Menu_action("End Turn?", options=(
            Menu_action("No Don't End Turn.", can_use= False, move= "back", show_buttons=False),
            Menu_action("Yes End Turn!", end_type="turn", show_buttons=False)
        ))


        action_menu = Menu_action("Do an Action", options=(
            Menu_action("Defend!", button_display= "spin", can_use= member.can_use_defend, move="defend", show_buttons=False, options= self.build_team_menu_action()),
            Menu_action("Run?", can_use= False, options=(
                Menu_action("No, Don't Run.",can_use= False , move= "back", show_buttons= False),
                Menu_action("Yes, Run!", can_use= False, end_type= "turn", show_buttons= False)
            ))
        ))

        item_menu = Menu_action("Use an Item",can_use= False , options=(
            Menu_action("Use Inventory!", can_use= False, button_display= "spin"),
            Menu_action("Use Pockets!", can_use= False, button_display= "spin")
        ))
        
        combat_menu = Menu_action("Fight!", can_use= member.can_use_weapon, button_display= "spin", options= weapons_menu)


        start_menu = Menu_action("Make a Move.", column_row=(2, 2), options=(combat_menu, item_menu, action_menu, end_move_menu))

        self.move_menu = start_menu

    ############################################################################## Action Menu ##############################################################################

    # /////////////////////// Display functions
    # Button --
    def covert_button_index_color(self, num):
        # gets the info from the list to get what colors to use
        selected_colors= {
            True : ("Green", "#1a4d27"),
            False : ("red", "#4d1a1c")
        }

        unselected_colors = {
            True : ("Blue", "#1a1d4d"),
            False : ("dark Grey", "#4f4f4f")
        }
        
        button_info = self.info_list[num]
        can_use = button_info.can_use
        if num == self.current_selection:
            color = selected_colors.get(can_use)
            return color
        else:
            color = unselected_colors.get(can_use)
            return color

    def display_action_info(self):
        # displays the information inside of the buttons
        for info in self.action_text_list:
            text, position = info
            quick_display_text(
                self.display, text, "white", position)

    def display_buttons(self):
        # displays the action buttons
        for button in self.action_buttons:
            pygame.draw.rect(self.display, self.covert_button_index_color(button[1])[1], button[0])
            pygame.draw.rect(self.display, self.covert_button_index_color(button[1])[0], button[0], 5)
    
    # Button --

    # /////////////////////// Change functions
    # Button --
    def change_current(self, number):
        option_length = len(self.info_list)
        if self.current_selection + number > option_length-1:
            self.current_selection += number - option_length
        elif self.current_selection + number < 0:
            self.current_selection = option_length + self.current_selection + number
        else:
            self.current_selection += number

        # do to how spin works, buttons have to be recreated every time it's moved
        if self.true_spin:
            self.build_buttons()

    def change_path(self, forward=True):
        if forward:
            next_option = self.info_list[self.current_selection]
            if next_option.can_use:
                if next_option.move != "back":
                    self.change_action()
                else: 
                    if len(self.move_path) > 0:
                        self.current_selection = self.move_path[-1]
                        self.move_path.pop(-1)
        else:
            if len(self.move_path) > 0:
                self.current_selection = self.move_path[-1]
                self.move_path.pop(-1)

        self.get_current_move_menu()
        self.build_buttons()

    def change_action(self):
        next_option = self.info_list[self.current_selection]
        # current action [action, action_index, target, target_index]
        # actions: attack

        # changes the move 
        move = next_option.move
        if move != None:
            self.move_manager.current_move[0] = move
            self.move_manager.current_move[1] = self.current_selection

        # changes the move index
        target = next_option.target
        if target != None:
            self.move_manager.current_move[2] = target
            self.move_manager.current_move[3] = self.current_selection

        # exits
        exit_type = next_option.end_type
        if exit_type == None:
            self.move_path.append(self.current_selection)

        elif exit_type == "move":
            self.move_manager.build_move(self.state)
            self.move_manager.current_move= [None, None, None, None]
            self.move_path.clear()

        elif exit_type == "turn":
            self.move_manager.global_moves.extend(self.move_manager.created_moves)
            self.move_manager.created_moves.clear()
            change_data = self.player_data.party.change_current()
            next_team = change_data[0]
            self.auto_move = change_data[1]
            if next_team:
                self.state= "enemy"
            self.move_path.clear()
        self.current_selection = 0
    # Button --

    ########################################################################################################################################################################################################
    ################################################################################################# Menu #################################################################################################
    ########################################################################################################################################################################################################

     
    #########################################################################################################################################################################################################
    ############################################################################################# build methods #############################################################################################
    #########################################################################################################################################################################################################
    def build_combat_icons(self, team, display_rect):
        # creates the combat icons in the game
        party_4 = len(team) <= 4
        pos = display_rect.topleft
        x = pos[0]
        y = pos[1]
        for member in team:
            if party_4:
                member.combat_icon_pos = (x, y)
                member.build_combat_icon(party_4)
                y += 150
            else:
                if x > pos[0] + 75:
                    x = pos[0]
                    y += 75 
                member.combat_icon_pos = (x, y)
                member.build_combat_icon(party_4)
                x += 75

    
    #########################################################################################################################################################################################################
    ############################################################################################# build methods #############################################################################################
    #########################################################################################################################################################################################################

    #########################################################################################################################################################################################################
    ############################################################################################ display methods ############################################################################################
    #########################################################################################################################################################################################################
    def display_ui(self):
        # displays UI
        self.display.fill((0, 0, 0))

        # displays how many entries are in the info list
        # quick_display_text(self.display, f"Items in info_list: {len(self.info_list)}", "White", [self.display_size[0]/2, self.display_size[1]/2])

        # Debug 
        """quick_display_text(self.display, f"currents: {self.player_data.party.current_member}, {self.enemy_data.party.current_member}", "White", [self.display_size[0]/2, self.display_size[1]/2 - 60])
        quick_display_text(self.display, f"state: {self.state}", "White", [self.display_size[0]/2, self.display_size[1]/2 - 40])
        btn_nums = []
        for button in self.action_buttons:
            btn_nums.append(button[1])
        quick_display_text(self.display, f"button numbers: {btn_nums}", "White", [self.display_size[0]/2, self.display_size[1]/2 - 20])
        quick_display_text(self.display, f"button config: {self.button_style}, {self.button_grid}, {self.true_spin}", "White", [self.display_size[0]/2, self.display_size[1]/2- 80])
        quick_display_text(self.display, f"auto: {self.auto_move}", "White", [self.display_size[0]/2, self.display_size[1]/2- 100])"""

        # map rectangle
        pygame.draw.rect(self.display, "Blue", self.map, 2)
        player_score_pos = list(self.map.midleft)
        player_score_pos[0] += 20
        quick_display_text(self.display, f"{self.scores[0]}", "white", player_score_pos, "midleft")

        enemy_score_pos = list(self.map.midright)
        enemy_score_pos[0] -= 20
        quick_display_text(self.display, f"{self.scores[1]}", "white", enemy_score_pos, "midright")

        # Player data
        pygame.draw.rect(self.display, (0, 255, 0), self.player_team, 2)
        self.player_data.party.display_team_icons(self.display, self.state == "player")

        # Enemy Data
        pygame.draw.rect(self.display, "Red", self.enemy_team, 2)
        self.enemy_data.party.display_team_icons(self.display, False)

        # Arena screen
        pygame.draw.rect(self.display, "#bcd2eb", self.arena_screen)
        pygame.draw.rect(self.display, (255, 0, 0), self.arena_screen, 2)
        self.enemy_data.display_field_team(self.display)

        # draws the control panel
        pygame.draw.rect(self.display, "Orange", self.control_panel, 2)

        if self.state == "player" and not self.auto_move:
            self.display_buttons()
            self.display_action_info()
            if self.move_path:
                x, y = self.control_panel.midtop
                quick_display_text(self.display, "Back", "White", (x, y - 20))


        if self.state == "moves":
            self.move_manager.display_move(self.display, self.control_panel)

        elif self.auto_move:
            quick_display_text(self.display, f"Your allies are making their move.", "White", self.control_panel.center)

        elif self.state == "enemy":
            quick_display_text(self.display, f"Your enemies are making their move.", "White", self.control_panel.center)

        pygame.display.update()
    
    #########################################################################################################################################################################################################
    ############################################################################################ display methods ############################################################################################
    #########################################################################################################################################################################################################

    #########################################################################################################################################################################################################
    ################################################################################################# Setup #################################################################################################
    #########################################################################################################################################################################################################
    def results(self):
        "Gets result of round"
        if not self.enemy_data.party.get_alive[0]:
            if self.debug:
                self.init_combat()
                print("player win")
            else:
                self.run_combat = False
        elif not self.player_data.party.get_alive[0]:
            if self.debug:
                self.init_combat()
                print("enemy lose")
            else:
                self.run_combat = False
        else:
            for team in (self.enemy_data, self.player_data):
                team.party.current_member = 0
                team.party.regain_stamina(2)
            self.auto_move = False
            self.state = "player"
    
    def setup_combat_icons(self):
        self.build_combat_icons(self.player_data.party.team, self.player_team)
        self.build_combat_icons(self.enemy_data.party.team, self.enemy_team)

        # sets the enemies on the field
        self.enemy_data.combat_initialize_field_team(self.area_limit, self.arena_screen.midbottom[1] - 10)

    def debbuging(self):
        "resets the battle with a fresh batch of players and enemies"
        for team in (self.enemy_data, self.player_data):
            team.party.team.clear()
            team.party.generate_allies(randrange(1, 17))

    def reset_combat(self):
        if self.debug:
            self.debbuging()
        self.move_manager.reset_move_data()
        self.auto_move = False
        self.state = "player"
        self.enemy_data.party.current_member = 0
        self.player_data.party.current_member = 0

    def init_combat(self):
        self.run_combat = True
        self.reset_combat()
        self.get_current_move_menu()
        self.build_buttons()
        self.setup_combat_icons()

    def get_current_move_menu(self):
        self.build_move_menu()
        move_menu = self.move_menu
        if len(self.move_path) != 0:
            for index in self.move_path:
                move_menu = move_menu.options[index]
        
        self.info_list= move_menu.options
        self.button_style = move_menu.button_display
        self.button_grid = move_menu.column_row

    #########################################################################################################################################################################################################
    ################################################################################################# Setup #################################################################################################
    #########################################################################################################################################################################################################

    def state_control(self):
        "Operates the functions that are tied to a state or mode"

        if self.state == "player" and self.auto_move:
            self.move_manager.auto_member()
            self.scores[0] += 1
        elif self.state == "enemy":
            self.move_manager.auto_member()
            self.scores[1] += 1
        elif self.state == "moves":
            if create_timer(self.current_time,3000, self.next_move_start_time) or self.move_manager.starting_move:
                self.move_manager.move_player()
        elif self.state == "result":
            self.results()

    def controller(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_combat = False

                if self.state == "player" and not self.auto_move:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.change_current(-1)
                        elif event.key == pygame.K_RIGHT:
                            self.change_current(1)
                        elif event.key == pygame.K_UP:
                            self.change_current(self.button_grid[0] * -1)
                        elif event.key == pygame.K_DOWN:
                            self.change_current(self.button_grid[0] * 1)

                        elif event.key == pygame.K_RETURN:  # enter
                            self.change_path()
                        elif event.key == pygame.K_BACKSPACE:
                            self.change_path(False)

    def play_combat(self):
        self.init_combat()
        while self.run_combat:
            self.current_time = pygame.time.get_ticks()
            self.state_control()
            self.controller()
            self.display_ui()
