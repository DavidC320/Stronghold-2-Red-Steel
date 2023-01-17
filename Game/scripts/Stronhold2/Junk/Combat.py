# 9/192022
import pygame

from Game_scripts.Teams import Enemy
from Game_scripts.Tool_box import create_text

class character_move:
    def __init__(self, user_team, user_index, action, action_index, target_team, target_index):
        self.user_team = user_team
        self.user_index = user_index
        self.action = action
        self.action_index = action_index
        self.target_team = target_team
        self.target_index = target_index

class Combat:
    def __init__(self, display, clock, player):
        self.display = display
        self.clock = clock
        self.screen_size = self.display.get_size()

        self.player_data = player
        self.current_ally = self.player_data.party.current_ally_class

        # Enemy 
        self.enemy_data = Enemy()
        if len(self.enemy_data.party.team) <= 0:
            self.enemy_data.party.generate_allies()

        # battle states
        self.state_list = ("Intro", "Player", "Enemy", "Win", "Lose", "Escape")
        self.state = "Intro"

        # options
        self.action_dict = {
            "can use" : True,
            "operation" : "button",
            "column and row" : [2, 2],
            "up and down jump" : [-2, 2],
            "move" : None,
            "options" : {
                "Attack" : {
                    "can use" : True,
                    "operation" : "slide",
                    "column and row" : None,
                    "up and down jump" : [0, 0],
                    "move" : "attack",
                    "options" : {}
                },
                "Item" : {
                    "can use" : True,
                    "operation" : "button",
                    "column and row" : [2, 1],
                    "up and down jump" : [0, 0],
                    "move" : None,
                    "options" : {
                        "Pockets" : {
                            "can use" : True,
                            "operation" : "slide",
                            "column and row" : None,
                            "up and down jump" : [0, 0],
                            "move" : "item",
                            "options" : {

                            }
                        },
                        "Inventory" : {
                            "can use" : True,
                            "operation" : "slide",
                            "column and row" : None,
                            "up and down jump" : [0, 0],
                            "move" : "item",
                            "options" : {
                                
                            }
                        }
                    }

                },
                "Defend" : {
                    "can use" : True,
                    "operation" : "allies",
                    "column and row" : None,
                    "up and down jump" : [0, 0],
                    "move" : "defend",
                    "options" : {

                    }
                },
                "Other Actions" : {
                    "can use" : True,
                    "operation" : "button",
                    "column and row" : [2, 1],
                    "move" : None,
                    "options" : {
                        "Run" : {
                            "can use" : True,
                            "operation" : "button",
                            "column and row" : [2, 1],
                            "up and down jump" : [0, 0],
                            "move" : "run",
                            "options" : {
                                "Don't run" : {
                                    "can use" : True,
                                    "operation" : None,
                                    "column and row" : None,
                                    "up and down jump" : [0, 0],
                                    "move" : "back",
                                    "options" : {}
                                },
                                "Run" : {
                                    "can use" : True,
                                    "operation" : None,
                                    "column and row" : None,
                                    "up and down jump" : [0, 0],
                                    "move" : "end",
                                    "options" : {}
                                    }
                                }
                            },
                        "End turn" : {
                            "can use" : True,
                            "operation" : None,
                            "column and row" : None,
                            "up and down jump" : [0, 0],
                            "move" : "end turn",
                            "options" : {}
                        }
                    }
                }
            }
        }

        
        self.move_list = []
        self.player_action_path = []  # this is the path to the current option in the action menu
        self.selected = 0
        self.current_move = {
            "action" : None,
            "action_index" : 0,
            "target team" : None,
            "target index" : 0
        }

        # ui elements
        self.map = pygame.Rect(0, 0, self.screen_size[0], 160)  # map bar
        self.player_team = pygame.Rect(0, 160, 150, self.screen_size[1] - 160)  # player party
        self.arena_screen = pygame.Rect(150, 160, self.screen_size[0] - 300, 300)  # arena screen
        self.control_panel = pygame.Rect(150, 460, self.screen_size[0] - 300, 300)  # control panel
        self.enemy_team = pygame.Rect(self.screen_size[0] - 150, 160, 150, self.screen_size[1] - 160)  # Enemy party
        self.current_display_buttons = []

        # set up enemies
        self.area_limit = (self.arena_screen.x, self.arena_screen.x + self.arena_screen.width)

    @property
    def current_option(self):
        # gets the current nested dictionary using the action path
        current_option = self.action_dict
        if self.player_action_path:
            for path in self.player_action_path:
                current_option = current_option.get("options").get(path)###################################################################
                
    def change_selected(self, number):
        # increases or decreases the selected variable
        option_length = len(self.current_option.get("options"))
        self.selected += number
        if self.selected > option_length - 1:
            self.selected -= option_length
        elif self.selected < 0:
            self.selected += option_length
    
    def change_path(self, mode):
        # changes the action path
        options = self.current_option.get("options")
        option_keys = options.keys()
        if mode == "back":
            self.remove_last_path()

        elif mode == "forward":
            next_path = option_keys[self.selected]
            option_info = options.get(next_path)
            if option_info.get("can use"):
                #   checks if the last option was an action
                if self.current_move.get("action") != None:
                    self.current_move["action index"] = self.selected
                self.move_enter(option_info, next_path)

    def move_enter(self, selected_option, next_path):
        action =  selected_option.get("move")
        if action == "back":
            self.remove_last_path()
        elif action == "end":
            None
        elif action == "end turn":
            self.player_data.party.current_member += 1
            if len(self.player_data.party.team) == self.player_data.party.current_member:
                self.player_data.party.current_member = 0
                self.mode = "enemy"
            self.player_action_path = []
        else:
            self.current_move["action"] = action
            self.player_action_path.append(next_path)

    def build_move(self):
        None

    def remove_last_path(self):
        if len(self.player_action_path) > 0:
                self.player_action_path.pop(-1)

    def controller(self, event):
        # this is the new controls for the game
        if self.state == "player":
            up_down_change = self.current_option.get("up and down jump")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.change_selected(-1)
                elif event.key == pygame.K_RIGHT:
                    self.change_selected(1)
                elif event.key == pygame.K_UP:
                    self.change_selected(up_down_change[0])
                elif event.key == pygame.K_UP:
                    self.change_selected(up_down_change[1])

                elif event.key == pygame.K_RETURN:  # enter
                    self.change_path("forward")
                elif event.key == pygame.K_BACKSPACE:
                    self.change_path("back")

    ####################################################################################################################################################
    #################################################################### showing UI ####################################################################
    ####################################################################################################################################################

    def display_members(self, team, show_playable = True):
        # Display the members
        num = 0
        for member in team:
            member.display_combat_icon(self.display, num, show_playable)

    def build_action_buttons(self):
        # Creates the action buttons to show on screen
        current_option = self.current_option
        options = current_option.get("options") # gets the dictonary of options
        row_column = current_option.get("column and row")
        if row_column == None:
            row_column = [1, 4]

        # gets teh initial position of the buttons
        control_panel_pos = self.control_panel.topleft
        x = control_panel_pos[0]
        y = control_panel_pos[1]
        # gets the size of the buttons
        control_panel_size = self.control_panel.size
        button_size = (control_panel_size[0]/ row_column[1], control_panel_size[1]/ row_column[0])

        # goes through all of the options inside of the current selected option and creates buttons form them
        buttons = []
        for option in options:
            # creates the position
            if x > control_panel_pos[0] + button_size[0] * row_column[1] -1:
                x = control_panel_pos[0]
                y += button_size[1]

            button = pygame.Rect(x, y, button_size[0], button_size[1])
            text = option
            can_use = options.get(option).get("can use")
            buttons.append((button, text, can_use))
        
        # end product
        self.current_display_buttons= buttons

    def draw_buttons(self): 
        # draws the buttons
        # dictionaries for color
        can_select_selected_colors = {
            True : "Green",
            False : "Red"
        }
        can_select_unselected_colors = {
            True : "Yellow",
            False : "Grey"
        }
        for button in self.current_display_buttons:
            index_number = self.current_display_buttons.index(button)
            color = "white"  # false safe
            if index_number == self.selected:
                color = can_select_selected_colors.get(button[2])
            else:
                color =  can_select_unselected_colors.get(button[2])

            pygame.draw.rect(self.display, color, button[0], 5)
            create_text(self.display, button[1], "White", button.center)

    ####################################################################################################################################################
    #################################################################### showing UI ####################################################################
    ####################################################################################################################################################

    ##################################################################################################################################################
    #####################################################################  Setup #####################################################################
    ##################################################################################################################################################

    def setup_combat(self):
        # sets up the the enemy and player ui for the game
        # team icons
        self.setup_combat_icons(self.player_data.party.team, self.player_team)
        self.setup_combat_icons(self.enemy_data.party.team, self.enemy_team)

        # sets the enemies on the field
        self.enemy_data.combat_initialize_field_team(self.area_limit, self.arena_screen.midbottom[1] - 10)

    def setup_combat_icons(self, team, display_rect):
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

    

    def setup_player_actions(self):
        None
        # creating weapon actions
        weapon_actions ={}
        current_member = self.player_data.current_member
        for weapon in current_member.hands:
            if "equip_weapon" in weapon.flags:
                None
                weapon_action = {weapon.name : {
                    "can use" : current_member.stamina > weapon.energy_spend
                }}

        # creating pocket actions

        # creating inventory actions
    ##################################################################################################################################################
    #####################################################################  Setup #####################################################################
    ##################################################################################################################################################

    def run_combat(self):
        running = True
        self.setup_combat()
        
        while running:
            self.clock.tick(60)  # This sets up framerate

            # events that control the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Debug is now closed")
                    running = False

                self.event_controller(event)

            # display settings
            self.display.fill((0, 0, 0))  # play screen

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

            # control panel
            pygame.draw.rect(self.display, "Orange", self.control_panel, 2)
            self.draw_action_buttons()

            pygame.display.update()