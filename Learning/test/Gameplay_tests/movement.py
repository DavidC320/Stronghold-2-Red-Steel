# 10/11/2022
import pygame

class Movement:
    def __init__(self):
        self.screen_size = [800, 600]
        self.display = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Movement Test")
        self.clock = pygame.time.Clock()
        # code from Coders Legacy // how to create rectangels
        self.position = [self.screen_size[0]/2, self.screen_size[1]/2]
        self.player_rect = pygame.Rect(self.position[0], self.position[1], 20, 40)
        self.vel = 3
        self.run_mod = 2

    def controller(self):
        keys = pygame.key.get_pressed()
        speed = self.vel

        # running
        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            speed = self.vel * self.run_mod

        # basic movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.position[0] -= speed
            if self.position[0] < 0:
                self.position[0] = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.position[0] += speed
            if self.position[0] > self.screen_size[0]:
                self.position[0] = self.screen_size[0]

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.position[1] -= speed
            if self.position[1] < 0:
                self.position[1] = 0

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.position[1] += speed
            if self.position[1] > self.screen_size[1]:
                self.position[1] = self.screen_size[1]

        self.player_rect.midbottom = self.position

    def run_debug(self):
        running = True
        while running:
            self.clock.tick(60)

            # events that control the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Debug is now closed")
                    running = False

            self.controller()

            # display settings
            self.display.fill((0, 0, 0))
            pygame.draw.rect(self.display, (255, 0, 0), self.player_rect)
            pygame.display.update()
        
        pygame.quit()

test = Movement()
test.run_debug()