# 1/2/2023
import pygame
from random import randrange

from Game_scripts.Teams import Enemy
from Game_scripts.Music_player import Music_manager
from Game_scripts.Tool_box import quick_display_text, create_timer, create_text
from Game_scripts.Move_manager import Move_manager

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

################################################################################################################################################################
############################################################################ Combat ############################################################################
################################################################################################################################################################


class Combat:
    def __init__(self, display, clock, player):
        # screen
        self.music_manager = Music_manager()
        
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
                x, y = button[0].midtop
                title_info = [self.info_list[info_index].title, (x, y+ 10)]
                texts.append(title_info)

                # getting the range of availbe space
                text_rect = create_text(self.info_list[info_index].title, "white", (x, y+ 10))[1]
                text_bottom_pos = text_rect.bottom
                y = text_bottom_pos
                button_bottom_pos = button[0].bottom
                size_range = (button_bottom_pos - text_bottom_pos )
                offset = int(size_range / len(self.info_list[info_index].extra_text))

                num = 0
                for data in self.info_list[info_index].extra_text:
                    true_offset = (y+ 10)+ (num) * offset


                    pos = (x, true_offset)
                    texts.append((str(data), pos))
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
    def build_team_menu_action(self, team= "target_ally", dead= False):
        print(dead)
        teams = {
            "target_ally" : self.player_data.party.team,
            "target_enemy" : self.enemy_data.party.team
        }
        team_conversion = {
            "target_ally" : "player",
            "target_enemy" : "enemy"
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
            team_menu.append(Menu_action(member.name, extra_text=[health], can_use=can_use, target= team_conversion.get(team), end_type= "move"))
        return team_menu

    def build_move_action(self, items, move= "attack"):
        weapon_menu = []
        member = self.player_data.party.current_ally
        stamina = member.current_stamina
        for item in items:
            if move == "attack":
                weapon_menu.append(Menu_action(item.name, extra_text=member.weapon_data(item), can_use=item.can_use(stamina), move="attack", button_display="spin", show_buttons= False, options= self.build_team_menu_action("target_enemy")))
            else:
                flags = item.flags
                allow_dead = "target_dead" in flags
                print(flags, allow_dead)
                print(item.item_data)

                if "target_ally" in flags:
                    weapon_menu.append(Menu_action(item.name, extra_text= item.item_data, can_use= item.can_use(stamina), move=move, button_display="spin", show_buttons= False, options= self.build_team_menu_action("target_ally", allow_dead)))
                elif "target_enemy" in flags:
                    weapon_menu.append(Menu_action(item.name, extra_text= item.item_data, can_use= item.can_use(stamina), move=move, button_display="spin", show_buttons= False, options= self.build_team_menu_action("target_enemy", allow_dead)))
                else:
                    weapon_menu.append(Menu_action(item.name, extra_text= item.item_data, can_use= item.can_use(stamina), move=move, button_display="spin", show_buttons= False))
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

        inventory_menu = self.build_move_action(self.player_data.inventory.inventory, "inventory")

        item_menu = Menu_action("Use an Item" , options=(
            Menu_action("Use Inventory!", can_use= self.player_data.inventory.can_use_inventory() ,button_display= "spin", options= inventory_menu),
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
            self.music_manager.play_sound(3)

        elif exit_type == "move":
            self.move_manager.build_move(self.state)
            self.move_manager.current_move= [None, None, None, None]
            self.move_path.clear()
            self.music_manager.play_sound(4)

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
            quick_display_text(self.display, "Control with arrows.", "White", self.map.center)
            x, y = self.control_panel.midtop
            if self.move_path:
                quick_display_text(self.display, "<-- Back Button or Esc to go back.", "Black", (x, y - 20))
            else:
                quick_display_text(self.display, "Press Enter to make your moves.", "Black", (x, y - 20))


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
                self.scores[0] += 1
            else:
                self.run_combat = False
        elif not self.player_data.party.get_alive[0]:
            if self.debug:
                self.init_combat()
                self.scores[1] += 1
            else:
                self.run_combat = False
        else:
            for team in (self.enemy_data, self.player_data):
                team.party.current_member = 0
                team.party.regain_stamina(2)
                team.inventory.organize_inventories(True)
            self.build_move_menu()
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
            team.inventory.generate_items()

    def reset_combat(self):
        if self.debug:
            self.debbuging()
        self.move_manager.reset_move_data()
        self.auto_move = False
        self.state = "player"
        self.enemy_data.party.current_member = 0
        self.player_data.party.current_member = 0

    def init_combat(self):
        self.music_manager.play_music()
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
        elif self.state == "enemy":
            self.move_manager.auto_member()
        elif self.state == "moves":
            if create_timer(self.current_time, self.move_manager.move_display_time, self.next_move_start_time) or self.move_manager.starting_move:
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
                        elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                            self.change_path(False)

    def play_combat(self):
        self.init_combat()
        while self.run_combat:
            self.current_time = pygame.time.get_ticks()
            self.state_control()
            self.controller()
            self.display_ui()