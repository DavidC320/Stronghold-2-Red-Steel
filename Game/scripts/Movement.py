# 9/192022
from turtle import left, screensize, width
import pygame

class Movement:
    def __init__(self, display, clock, player):
        pygame.display.set_caption("Movement Test")
        self.display = display
        self.clock = clock
        self.vel = 3
        self.run_mod = 2

        # player_data
        self.player_data = player
        if len(self.player_data.party.team) <= 0:
            self.player_data.party.generate_allies()

        # what character is currently selceted
        self.current_ally = self.player_data.party.current_ally_class

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

        # running
        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            speed = self.vel * self.run_mod

        # basic movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.position[0] -= speed
            if self.position[0] < self.bounds[0]:
                self.position[0] = self.bounds[0]

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.position[0] += speed
            if self.position[0] > self.bounds[1]:
                self.position[0] = self.bounds[1]

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.position[1] -= speed
            if self.position[1] < self.bounds[2]:
                self.position[1] = self.bounds[2]

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.position[1] += speed
            if self.position[1] > self.bounds[3]:
                self.position[1] = self.bounds[3]

        self.player_rect.midbottom = self.position

    def draw_rectangles(self):
        # draws these rectangles
        list_of_rects = (
            (self.current_ally.color, self.player_rect, 0),  # Player
            ((0, 0, 255), (0, 0, self.screen_size[0], 160), 2),  # Map bar
            ((0, 255, 0), (0, 160, 150, self.screen_size[1] - 160), 2),  # Current member stats
            ((255, 0, 0), (self.screen_size[0] - 150, 160, 160, self.screen_size[1] - 160), 2),  # controls
            ((255, 255, 255), self.map_border, 2)
        )
        for rects in list_of_rects:
            color = rects[0]
            t_rect = rects[1]
            width = rects[2]
            pygame.draw.rect(self.display, color, t_rect, width)

    def create_text(self, text, color, position):
        text = self.font.render(text, False, color)
        text_rect = text.get_rect(midleft=position)
        self.display.blit(text, text_rect)

    def run_debug(self):
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
                        self.current_ally = self.player_data.party.current_ally_class


            self.controller()

            # display settings
            self.display.fill((0, 0, 0))  # play screen
            
            self.draw_rectangles()

            # text
            text = self.font.render(self.current_ally.name, False, (255, 255, 255))
            text_rect = text.get_rect(center=(self.position[0], self.position[1] + 9))
            self.display.blit(text, text_rect)

            # controls
            self.create_text("Controls", (255, 255, 255), (self.screen_size[0] - 120, 170))
            self.create_text("Leader", (255, 255, 255), (6, 170))
            texts = ("w & ^ = up", "a & < = left", "s & v = down", "d & > = right", "shift = run", "f = switch")
            y = 190
            for text in texts:
                self.create_text(text, (255, 255, 255), (self.screen_size[0] - 144, y))
                y += 30
            texts = (f"Name: {self.current_ally.name}",f"Race: {self.current_ally.race}", 
            f"Hp: {self.current_ally.current_health} / {self.current_ally.hitpoints}", 
            f"Eg = {self.current_ally.current_energy} / {self.current_ally.energy}", 
            f"At: {self.current_ally.base_attack} + {self.current_ally.weapon.attack}",
            f"Fight Lv: {self.current_ally.fighter_lv}", f"Hunt: {self.current_ally.hunter_lv}", f"Cast: {self.current_ally.caster_lv}"
            )
            y = 190
            for text in texts:
                self.create_text(text, (255, 255, 255), (6, y))
                y += 30

            pygame.display.update()
        
        return False

