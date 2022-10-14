# 9/192022
from re import X
import pygame

class Combat:
    def __init__(self, display, clock, player):
        self.display = display
        self.clock = clock
        self.screen_size = self.display.get_size()
        self.player_data = player
        if len(self.player_data.party.team) <= 0:
            self.player_data.party.generate_allies(30)

        # states
        self.state_list = ("Intro", "Player", "Enemy", "Win", "Lose", "Escape")
        self.state = "Intro"

        # options
        self.basic_actions = ("Attack", "Defend", "Run", "Item")
        self.attack_actions = ("left Weapon", "Both Weapons", "Right Weapon")
        self.use_Item_actions = ("Use Left Pocket", "Use Inventory", "Use Right Pocket")
        self.run_away_actions = ("Don't Run Away", "Run Away")
        self.mode = 0

        self.selected = 0


        # ui elements
        # map bar
        self.map = pygame.Rect(0, 0, self.screen_size[0], 160)
        # player party
        self.player_team = pygame.Rect(0, 160, 150, self.screen_size[1] - 160)
        # arena screen
        self.arena_screen = pygame.Rect(150, 160, self.screen_size[0] - 150, 300)
        # control panel
        self.control_panel = pygame.Rect(150, 460, self.screen_size[0] - 150, 300)

    def create_text(self, text, color, position, mode = "center", size = 22):
        font = pygame.font.SysFont("Britannic", size)
        text = font.render(text, False, color)
        if mode == "center":
            text_rect = text.get_rect(center=position)
        elif mode == "midleft":
            text_rect = text.get_rect(midleft=position)
        self.display.blit(text, text_rect)

    def display_members(self, team):
        party_4 = len(team) <= 4
        x = 0
        y = 160
        num = 0
        for member in team:
            if party_4:
                name_size = 22
                hp_size = name_size
                icon = pygame.Rect(x, y, 150, 150)
                pygame.draw.rect(self.display, "Cyan", icon, 6)
                pygame.draw.rect(self.display, member.color, icon, 4)
                y += 150
            else:
                name_size = 14
                hp_size = 11
                if x > 75:
                    x = 0
                    y += 75 
                icon = pygame.Rect(x, y, 75, 75)
                if num < 4:
                    pygame.draw.rect(self.display, "Cyan", icon, 6)
                pygame.draw.rect(self.display, member.color, icon, 4)
                x += 75
                num += 1
            text_defualt = icon.midtop
            name_offset = icon.size[0] * .3
            self.create_text(member.name, "white", (text_defualt[0], text_defualt[1] + name_offset ), size = name_size)
            hp_offset = icon.size[0] * .8
            self.create_text(f"Hp: {member.current_hp} / {member.hp}", "white", (text_defualt[0], text_defualt[1] + hp_offset), size = hp_size)

    def draw_buttons(self):
        control_panel_size = self.control_panel.size
        control_panel_pos = self.control_panel.topleft
        x = control_panel_pos[0]
        y = control_panel_pos[1]
        num = 0
        if self.mode ==  0:
            button_size = (control_panel_size[0]/ 2, control_panel_size[1]/ 2)
            for option in self.basic_actions:
                if x > control_panel_pos[0] + button_size[0]:
                    x = control_panel_pos[0]
                    y += button_size[1]
                button = pygame.Rect(x, y, button_size[0], button_size[1])
                if num == self.selected:
                    color = "Green"
                else:
                    color = "Yellow"
                pygame.draw.rect(self.display, color, button, 5)
                self.create_text(option, "White", button.center)
                x += button_size[0]
                num += 1

        elif self.mode == 1:
            button_size = (control_panel_size[0]/ 3, control_panel_size[1])
            for option in self.basic_actions:
                button = pygame.Rect(x, y, button_size[0], button_size[1])
                if num == self.selected:
                    color = "Green"
                else:
                    color = "Yellow"
                pygame.draw.rect(self.display, color, button, 5)
                self.create_text(option, "White", button.center)
                x += button_size[0]
                num += 1

        elif self.mode == 2:
            self.create_text("Select a party member to defend", "white", self.control_panel.center)

        elif self.mode == 3:
            button_size = (control_panel_size[0]/ 2, control_panel_size[1])
            for option in self.run_away_actions:
                button = pygame.Rect(x, y, button_size[0], button_size[1])
                if num == self.selected:
                    color = "Green"
                else:
                    color = "Yellow"
                pygame.draw.rect(self.display, color, button, 5)
                self.create_text(option, "White", button.center)
                x += button_size[0]
                num += 1

        elif self.mode == 4:
            button_size = (control_panel_size[0]/ 3, control_panel_size[1])
            for option in self.use_Item_actions:
                button = pygame.Rect(x, y, button_size[0], button_size[1])
                if num == self.selected:
                    color = "Green"
                else:
                    color = "Yellow"
                pygame.draw.rect(self.display, color, button, 5)
                self.create_text(option, "White", button.center)
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
                if self.mode == 0: # selecting action
                    self.change_selected(-1, self.basic_actions)
                elif self.mode == 1: # attack action
                    self.change_selected(-1, self.attack_actions)
                elif self.mode == 3: # running action
                    self.change_selected(-1, self.run_away_actions)
                elif self.mode == 4: # item action
                    self.change_selected(-1, self.use_Item_actions)
            
            elif event.key == pygame.K_RIGHT:
                if self.mode == 0: # selecting action
                    self.change_selected(1, self.basic_actions)
                elif self.mode == 1: # attack action
                    self.change_selected(1, self.attack_actions)
                elif self.mode == 3: # running action
                    self.change_selected(1, self.run_away_actions)
                elif self.mode == 4: # item action
                    self.change_selected(1, self.use_Item_actions)

            elif event.key == pygame.K_UP:
                if self.mode == 0: # selecting action
                    self.change_selected(-2, self.basic_actions)

            elif event.key == pygame.K_DOWN:
                if self.mode == 0: # selecting action
                    self.change_selected(2, self.basic_actions)

            elif event.key == pygame.K_RETURN:
                if self.mode == 0:
                    self.mode = self.selected + 1
                    self.selected = 0

            elif event.key == pygame.K_BACKSPACE:
                if self.mode in (1, 2, 3, 4):
                    self.selected =  self.mode - 1
                    self.mode = 0

    def run_combat(self):
        running = True
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
            # Arena screen
            pygame.draw.rect(self.display, (255, 0, 0), self.arena_screen, 2)

            # control panel
            pygame.draw.rect(self.display, "Orange", self.control_panel, 2)
            # draws the buttons
            self.draw_buttons()


            pygame.display.update()