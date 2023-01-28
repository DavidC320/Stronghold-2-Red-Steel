# 9/192022
import pygame

from Game_scripts.Tool_box import quick_display_text

class Movement:
    def __init__(self, display, clock, player):
        self.display = display
        self.clock = clock
        self.vel = 3
        self.run_mod = 2

        # player_data
        self.player_data = player
        if len(self.player_data.party.team) <= 0:
            self.player_data.party.generate_allies(16)

        # what character is currently selceted
        self.current_ally = self.player_data.party.current_ally

        # code from Coders Legacy // how to create rectangels
        # these lines are for the player character
        self.screen_size = self.display.get_size()
        self.position = [self.screen_size[0]/2, self.screen_size[1]/2]
        self.player_rect = pygame.Rect(self.position[0], self.position[1], 20, 40)

        self.font = pygame.font.SysFont("Britannic", 22)

        # placeholder ui elements
        self.map_border = pygame.Rect(0, 0, self.screen_size[1] - 160, self.screen_size[1] - 160)
        self.map_border.midtop = (self.screen_size[0] / 2, 160)
        _left = self.map_border.midleft[0]
        _right = self.map_border.midright[0]
        _up = self.map_border.midtop[1]
        _down =self.map_border.midbottom[1]
        self.bounds = (_left, _right, _up, _down)

    def controller(self):
        # sets some of the controls for the player, the f key is to switch party member
        keys = pygame.key.get_pressed()
        speed = self.vel

        # controls
        p_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        p_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        p_up = keys[pygame.K_UP] or keys[pygame.K_w]
        p_down = keys[pygame.K_DOWN] or keys[pygame.K_s]

        p_run = keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]

        # current condition
        moving = p_left or p_right or p_up or p_down

        # running
        if p_run and not self.current_ally.exhausted:
            speed = self.vel * self.run_mod
        
        # spends energy
        if p_run and moving:
            if not self.current_ally.exhausted:
                self.current_ally.change_stamina(-.2)
        else:
            self.current_ally.change_stamina(.2)

        # basic movement
        if p_left:
            self.position[0] -= speed
            if self.position[0] < self.bounds[0]:
                self.position[0] = self.bounds[0]

        if p_right:
            self.position[0] += speed
            if self.position[0] > self.bounds[1]:
                self.position[0] = self.bounds[1]

        if p_up:
            self.position[1] -= speed
            if self.position[1] < self.bounds[2]:
                self.position[1] = self.bounds[2]

        if p_down:
            self.position[1] += speed
            if self.position[1] > self.bounds[3]:
                self.position[1] = self.bounds[3]

        # updates the player's postilion
        self.player_rect.midbottom = self.position

    def draw_rectangles(self):
        # draws these rectangles
        list_of_rects = (
            (self.current_ally.color, self.player_rect, 0),  # Player
            ((0, 0, 255), (0, 0, self.screen_size[0], 160), 2),  # Map bar
            ((0, 255, 0), (0, 160, 150, self.screen_size[1] - 160), 2),  # Current member stats
            ((255, 0, 0), (self.screen_size[0] - 150, 160, 150, self.screen_size[1] - 160), 2),  # controls
            ((255, 255, 255), self.map_border, 2)
        )
        for rects in list_of_rects:
            color = rects[0]
            t_rect = rects[1]
            width = rects[2]
            pygame.draw.rect(self.display, color, t_rect, width)

    def run_movement(self):
        # runs the movement test
        running = True
        while running:
            self.clock.tick(60)

            # events that control the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Debug is now closed")
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.player_data.party.change_current()
                        self.current_ally = self.player_data.party.current_ally


            self.controller()

            # display settings
            self.display.fill((0, 0, 0))  # play screen
            
            self.draw_rectangles()

            # text
            text = self.font.render(self.current_ally.name, False, (255, 255, 255))
            text_rect = text.get_rect(center=(self.position[0], self.position[1] + 9))
            self.display.blit(text, text_rect)

            # controls
            quick_display_text(self.display, "Controls", (255, 255, 255), (self.screen_size[0] - 120, 170), "topleft")
            texts = ("w & ^ = up", "a & < = left", "s & v = down", "d & > = right", "shift = run", "f = switch")
            y = 200
            for text in texts:
                quick_display_text(self.display, text, (255, 255, 255), (self.screen_size[0] - 144, y), "topleft")
                y += 30

            # player data
            quick_display_text(self.display, "Leader", (255, 255, 255), (6, 170), "topleft")
            texts = (f"Party: {self.player_data.party.current_member + 1} / {len(self.player_data.party.team)}", f"Name: {self.current_ally.name}",
            f"Race: {self.current_ally.life_form}", 
            f"Hp: {self.current_ally.current_hp} / {self.current_ally.base_hp}", 
            f"Eg: {int(self.current_ally.current_stamina)} / {self.current_ally.base_stamina}", 
            f"Tired: {self.current_ally.exhausted}",
            #f"At: {self.current_ally.base_attack} + {self.current_ally.weapon.attack}",
            f"Fight Lv: {self.current_ally.fighter_lv}", 
            f"Hunt Lv: {self.current_ally.hunter_lv}", 
            f"Cast Lv: {self.current_ally.caster_lv}"
            )
            y = 200
            for text in texts:
                quick_display_text(self.display, text, (255, 255, 255), (6, y), "topleft")
                y += 30

            pygame.display.update()
        
        return False

