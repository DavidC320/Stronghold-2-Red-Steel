# 1/2/2023
import pygame

from Game_scripts.Teams import Enemy
from Game_scripts.Tool_box import create_text

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
        self.current_selection = 0
        self.info_list= []
        self.button_style = "spin"
        self.true_spin = False
        self.button_grid = [3, 2] # column / row

        # battle states
        self.state_list = ("Intro", "Player", "Enemy", "Win", "Lose", "Escape")
        self.state = "Intro"
        self.run_combat = True

        # set up enemies
        self.area_limit = (self.arena_screen.x, self.arena_screen.x + self.arena_screen.width)

    #########################################################################################################################################################################################################
    ############################################################################################# build methods #############################################################################################
    #########################################################################################################################################################################################################
    #################
    # build buttons #
    #################
    def build_buttons(self):
        if self.button_style == "grid":
            self.build_grid_buttons()
        elif self.button_style == "spin":
            self.build_spin_buttons()
        
        self.build_info()


    def build_grid_buttons(self):
        # creates the grid buttons
        # getting button size
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
        index_offset = 0
        if number > 5:
            self.true_spin = True
            number = 5
            index_offset = self.current_selection -2 
        else:
            self.true_spin = False

        # getting the position offset for the buttons to make sure the buttons are centered.
        total_button_width = 120 * number
        pos_offset = (self.control_panel.size[0] - total_button_width)/2

        # creates the buttons
        button_list = []
        pos = list(self.control_panel.topleft)
        pos[0] += pos_offset
        button_size= [120, 300]
        start_index = index_offset
        for _ in range(number):
            button = pygame.Rect(pos[0], pos[1], button_size[0], button_size[1])
            pos[0] += button_size[0]
            if start_index + 1 > len(self.info_list):
                start_index = 0
            num = self.info_list.index(self.info_list[start_index])
            start_index += 1
            button_list.append((button, num))

        self.action_buttons = button_list
    #################
    # build buttons #
    #################
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

            text_info = [self.info_list[info_index]["title"], button[0].center]
            info_list.append(text_info)
            info_index += 1

        self.action_text_list = info_list

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

    def build_move_menu(self):
        # creates the action menu for the the character
        end_move_menu = {
            "title" : "End Turn?",
            "settings":{
                "can use" : True,
                "action" : {
                    "move" : None,
                    "target" : None,
                    "end type" : None
                    },
                "button style": { 
                    "button display": "grid",
                    "column/row" : (2, 1),
                    "show buttons" : True,
                    },
            },
            "buttons": (
                {
                    "title" : "No Don't End Turn.",
                    "settings":{
                        "can use" : False,
                        "action" : {
                            "move" : "back",
                            "target" : None,
                            "end type" : None
                            },
                        "button style": { 
                            "button display": "grid",
                            "column/row" : (2, 2),
                            "show buttons" : False,
                            },
                    },
                    "buttons": ()
                },
                {
                    "title" : "Yes End Turn!",
                    "settings":{
                        "can use" : False,
                        "action" : {
                            "move" : None,
                            "target" : None,
                            "end type" : "turn"
                            },
                        "button style": { 
                            "button display": "grid",
                            "column/row" : (2, 2),
                            "show buttons" : False,
                            },
                    },
                    "buttons": ()
                }
            )
        }

        action_menu = {
            "title" : "Do an Action.",
            "settings":{
                "can use" : True,
                "action" : {
                    "move" : None,
                    "target" : None,
                    "end type" : None
                    },
                "button style": { 
                    "button display": "grid",
                    "column/row" : (2, 1),
                    "show buttons" : True,
                    },
            },
            "buttons": (
                {
                    "title" : "Defend!",
                    "settings":{
                        "can use" : False,
                        "action" : {
                            "move" : None,
                            "target" : None,
                            "end type" : None
                            },
                        "button style": { 
                            "button display": "allies",
                            "column/row" : (2, 2),
                            "show buttons" : False,
                            },
                    },
                    "buttons": ()
                    },
                {
                    "title" : "Run?",
                    "settings":{
                        "can use" : True,
                        "action" : {
                            "move" : None,
                            "target" : None,
                            "end type" : None
                            },
                        "button style": { 
                            "button display": "grid",
                            "column/row" : (2, 1),
                            "show buttons" : True,
                            },
                    },
                    "buttons": (
                        {
                            "title" : "No Don't Run.",
                            "settings":{
                                "can use" : False,
                                "action" : {
                                    "move" : "back",
                                    "target" : None,
                                    "end type" : None
                                    },
                                "button style": { 
                                    "button display": "grid",
                                    "column/row" : (2, 2),
                                    "show buttons" : False,
                                    },
                            },
                            "buttons": ()
                            },
                        {
                            "title" : "Yes run Run!",
                            "settings":{
                                "can use" : False,
                                "action" : {
                                    "move" : "run",
                                    "target" : None,
                                    "end type" : "turn"
                                    },
                                "button style": { 
                                    "button display": "grid",
                                    "column/row" : (2, 2),
                                    "show buttons" : False,
                                    },
                                },
                            "buttons": ()
                            }
                        )
                }
            )
        }

        item_menu = {
            "title" : "Use an Item.",
            "settings":{
                "can use" : True,
                "action" :  {
                    "move" : None,
                    "target" : None,
                    "end type" : None
                    },
                "button style": { 
                    "button display": "grid",
                    "column/row" : (2, 1),
                    "show buttons" : True,
                    },
                },
            "buttons": (
                {
                    "title" : "Use inventory!",
                    "settings":{
                        "can use" : False,
                        "action" : {
                            "move" : None,
                            "target" : None,
                            "end type" : None
                            },
                        "button style": { 
                            "button display": "spin",
                            "column/row" : (2, 2),
                            "show buttons" : True,
                        },
                    },
                    "buttons": ()
                },
                {
                    "title" : "Use Pockets!",
                    "settings":{
                        "can use" : False,
                        "action" :  {
                            "move" : None,
                            "target" : None,
                            "end type" : None
                            },
                        "button style": { 
                            "button display": "spin",
                            "column/row" : (2, 2),
                            "show buttons" : True,
                        },
                    },
                    "buttons": ()
                },
            )
        }

        combat_menu = {
            "title" : "Fight!",
            "settings":{
                "can use" : False,
                "action" :  {
                    "move" : None,
                    "target" : None,
                    "end type" : None
                    },
                "button style": { 
                    "button display": "spin",
                    "column/row" : (2, 2),
                    "show buttons" : True,
                    },
                },
            "buttons": ()
            }

        start_menu = {
            "title" : "Make an Move.",
            "settings":{
                "can use" : True, 
                "action" : {
                    "move" : None,
                    "target" : None,
                    "end type" : None
                    },
                "button style": { 
                    "button display": "grid",
                    "column/row" : (2, 2),
                    "show buttons" : True,
                },
            },
            "buttons": (
                combat_menu,
                item_menu,
                action_menu,
                end_move_menu,
            )
        }
        self.move_menu = start_menu
    #########################################################################################################################################################################################################
    ############################################################################################# build methods #############################################################################################
    #########################################################################################################################################################################################################


    #########################################################################################################################################################################################################
    ############################################################################################ display methods ############################################################################################
    #########################################################################################################################################################################################################
    def covert_button_index_color(self, num):
        # gets the info from the list to get what colors to use
        selected_colors= {
            True : "Green",
            False : "red"
        }

        unselected_colors = {
            True : "Blue",
            False : "dark Grey"
        }
        
        button_info = self.info_list[num]
        can_use = button_info["settings"]["can use"]
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
            create_text(
                self.display, text, "white", position)

    def display_buttons(self):
        # displays the action buttons
        for button in self.action_buttons:
            pygame.draw.rect(self.display, self.covert_button_index_color(button[1]), button[0], 5)

    def display_members(self, team, show_playable = True):
        num = 0
        for member in team:
            member.display_combat_icon(self.display, num, show_playable)

    def display_ui(self):
        # displays UI
        self.display.fill((0, 0, 0))

        # displays how many entries are in the info list
        create_text(self.display, f"Items in info_list: {len(self.info_list)}", "White", [self.display_size[0]/2, self.display_size[1]/2])
        create_text(self.display, f"current index: {self.current_selection}", "White", [self.display_size[0]/2, self.display_size[1]/2 + 20])
        self.display_action_info()
        self.display_buttons()

        # map rectangle
        pygame.draw.rect(self.display, "Blue", self.map, 2)

        # Player data
        pygame.draw.rect(self.display, (0, 255, 0), self.player_team, 2)
        self.display_members(self.player_data.party.team)

        # Enemy Data
        pygame.draw.rect(self.display, "Red", self.enemy_team, 2)
        self.display_members(self.enemy_data.party.team, False)

        # Arena screen
        pygame.draw.rect(self.display, (255, 0, 0), self.arena_screen, 2)
        self.enemy_data.display_field_team(self.display)

        # draws the control panel
        pygame.draw.rect(self.display, "Orange", self.control_panel, 2)

        pygame.display.update()
    #########################################################################################################################################################################################################
    ############################################################################################ display methods ############################################################################################
    #########################################################################################################################################################################################################
    def get_current_move_menu(self):
        self.build_move_menu()
        move_menu = self.move_menu
        if len(self.move_path) != 0:
            for index in self.move_path:
                move_menu = move_menu.get("buttons")[index]
        
        self.info_list= move_menu["buttons"]
        self.button_style = move_menu["settings"]["button style"]["button display"]
        self.button_grid = move_menu["settings"]["button style"]["column/row"]
        
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
            if next_option["settings"]["can use"]:
                self.move_path.append(self.current_selection)
                self.current_selection = 0
        else:
            if len(self.move_path) > 0:
                self.current_selection = self.move_path[-1]
                self.move_path.pop(-1)

        self.get_current_move_menu()
        self.build_buttons()

    def controller(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_combat = False

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

    def setup_combat_icons(self):
        self.build_combat_icons(self.player_data.party.team, self.player_team)
        self.build_combat_icons(self.enemy_data.party.team, self.enemy_team)

        # sets the enemies on the field
        self.enemy_data.combat_initialize_field_team(self.area_limit, self.arena_screen.midbottom[1] - 10)

    def init_combat(self):
        self.run_combat = True
        self.get_current_move_menu()
        self.build_move_menu()
        self.build_buttons()
        self.setup_combat_icons()

    def play_combat(self):
        self.init_combat()
        while self.run_combat:
            self.controller()
            self.display_ui()
