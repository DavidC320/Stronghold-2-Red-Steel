# 9/192022
import pygame

from Game_scripts.Teams import Enemy
from Game_scripts.Tool_box import create_text

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
            "Attack" : {
                "Left Weapon" : False,
                "Both Weapon" : False, 
                "Right Weapon" : False},
            "Defend" : "Select a party member to defend",
            "Item" : {
                "Use left pocket" : False, 
                "Use inventory" : False, 
                "Use right pocket" : False},
            "Run" : ("Don't Run Away", "Run AWay")
        }

        self.basic_actions = list(self.action_dict.keys())
        # actions
        self.attack_actions = list(self.action_dict.get("Attack").keys())  # problem
        self.use_item_actions = list(self.action_dict.get("Item").keys())  # problem
        self.run_away_actions = self.action_dict.get("Run")  # problem
        # current settings
        self.mode = None
        self.selected = 0

        # ui elements
        self.map = pygame.Rect(0, 0, self.screen_size[0], 160)  # map bar
        self.player_team = pygame.Rect(0, 160, 150, self.screen_size[1] - 160)  # player party
        self.arena_screen = pygame.Rect(150, 160, self.screen_size[0] - 300, 300)  # arena screen
        self.control_panel = pygame.Rect(150, 460, self.screen_size[0] - 300, 300)  # control panel
        self.enemy_team = pygame.Rect(self.screen_size[0] - 150, 160, 150, self.screen_size[1] - 160)  # Enemy party

        # sut up enemies
        self.area_limit = (self.arena_screen.x, self.arena_screen.x + self.arena_screen.width)

    def setup_combat_icons(self, team, display_rect):
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

    def display_members(self, team, show_playable = True):
        # Display the members
        num = 0
        for member in team:
            member.display_combat_icon(self.display, num, show_playable)

    def draw_action_buttons(self):
        if self.mode ==  None:
            self.draw_button(self.basic_actions, 2, 2)

        elif self.mode == "Attack":
            self.draw_button(self.action_dict.get("Attack"), column=3)

        elif self.mode == "Defend":
            create_text(self.display, "Select a party member to defend", "white", self.control_panel.center)

        elif self.mode == "Run":
            self.draw_button(self.action_dict.get("Run"), column= 2)

        elif self.mode == "Item":
            self.draw_button(self.action_dict.get("Item"), column= 3)


    def draw_button(self, options, row = 1, column = 1):
        # This draws the buttons for the game
        # Set up
        control_panel_size = self.control_panel.size
        control_panel_pos = self.control_panel.topleft
        x = control_panel_pos[0]
        y = control_panel_pos[1]
        if isinstance(options, dict):
            dict_ = options
            options = list(options.keys())
            is_dict = True
        else:
            is_dict =  False
        num = 0
        button_size = (control_panel_size[0]/ column, control_panel_size[1]/ row)
        for option in options:
            if x > control_panel_pos[0] + button_size[0] * column -1:
                x = control_panel_pos[0]
                y += button_size[1]
            button = pygame.Rect(x, y, button_size[0], button_size[1])
            if num == self.selected:
                if is_dict and dict_.get(option) == False:
                    color = "Red"
                else:
                    color = "Green"
            
            else:
                if is_dict and dict_.get(option) == False:
                    color = "Grey"
                else:
                    color = "Yellow"
            pygame.draw.rect(self.display, color, button, 5)
            create_text(self.display, option, "White", button.center)
            x += button_size[0]
            num += 1
                
    def change_selected(self, number, options):
        option_length = len(options)
        self.selected += number
        if self.selected > option_length - 1:
            self.selected -= option_length
        elif self.selected < 0:
            self.selected += option_length

    def event_controller(self, event):
        # What are the controls for the player using events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if self.mode == None: # selecting action
                    self.change_selected(-1, self.basic_actions)

                elif self.mode == "Attack": # attack action
                    self.change_selected(-1, self.attack_actions)

                elif self.mode == "Run": # running action
                    self.change_selected(-1, self.run_away_actions)

                elif self.mode == "Item": # item action
                    self.change_selected(-1, self.use_item_actions)
            
            elif event.key == pygame.K_RIGHT:
                if self.mode == None: # selecting action
                    self.change_selected(1, self.basic_actions)

                elif self.mode == "Attack": # attack action
                    self.change_selected(1, self.attack_actions)

                elif self.mode == "Run": # running action
                    self.change_selected(1, self.run_away_actions)

                elif self.mode == "Item": # item action
                    self.change_selected(1, self.use_item_actions)

            elif event.key == pygame.K_UP:
                if self.mode == None: # selecting action
                    self.change_selected(-2, self.basic_actions)

            elif event.key == pygame.K_DOWN:
                if self.mode == None: # selecting action
                    self.change_selected(2, self.basic_actions)

            elif event.key == pygame.K_RETURN:  # enter
                if self.mode == None:
                    self.mode = self.basic_actions[self.selected]  # changes the mode with the selected action
                    self.selected = 0 # reverts to 

            elif event.key == pygame.K_BACKSPACE:
                # Goes back
                if self.mode in self.basic_actions:  # Only avtive when the mode is in basic actions
                    self.selected =  self.basic_actions.index(self.mode)  # sets the selected number to the last number
                    self.mode = None

                # Only active when in specific actions
                elif self.mode in (self.attack_actions):
                    None

    def run_combat(self):
        running = True
        # setup icons
        self.setup_combat_icons(self.player_data.party.team, self.player_team)
        self.setup_combat_icons(self.enemy_data.party.team, self.enemy_team)
        self.enemy_data.combat_initialize_field_team(self.area_limit, self.arena_screen.midbottom[1] - 10)
        
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