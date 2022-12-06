#10/11/2022
import pygame
from pygame import mixer

from Movement import Movement
from Combat import Combat
from Teams import Player

pygame.init()

# code help from Tech with tim
class Debug_menu:
    def __init__(self):
        # initializing pygame data
        pygame.display.set_caption("Debug menu")
        self.display_size = [900, 760]
        self.display = pygame.display.set_mode(self.display_size)
        self.clock = pygame.time.Clock()

        # Classes
        self.player = Player()
        self.combat = Combat(self.display, self.clock, self.player)
        self.move_test = Movement(self.display,  self.clock, self.player)

        # options information
        self.options = ("Movement", "Combat", "Inventory", "Item storage", "Ally storage")
        self.current = 0
        
        self.font = pygame.font.SysFont("Britannic", 22)

    def create_text(self, text, color, position, mode = "center"):
        text = self.font.render(text, False, color)
        if mode == "center":
            text_rect = text.get_rect(center=position)
        elif mode == "midleft":
            text_rect = text.get_rect(midleft=position)
        self.display.blit(text, text_rect)

    def change_current(self, increment= True):
        length = len(self.options) - 1
        if not increment:
            number = -1
        else:
            number = 1
        self.current += number
        if self.current < 0:
            self.current = length
        elif self.current > length:
            self.current = 0

    def draw_options(self):
        x = 5
        y = 50
        for option in self.options:
            if self.options.index(option) == self.current:
                color = "Yellow"
            else:
                color = "White"
            self.create_text(option, color, (x, y), "midleft")
            y += 30

    def run_debug(self):
        running = True
        testing = False
        while running:
            self.clock.tick(60)

            # events that control the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Debug is now closed")
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.change_current(False)
                    elif event.key == pygame.K_DOWN:
                        self.change_current()
                    elif event.key == pygame.K_RETURN:
                        testing = True

            # display settings
            self.display.fill((0, 20, 0))  # play screen
            self.create_text("Strong Hold 2 Debug Menu", "Yellow", (self.display_size[0] / 2, 20))

            if testing:
                operation = self.options[self.current]
                if operation == "Movement":
                    testing = self.move_test.run_movement()
                elif operation == "Combat":
                    testing = self.combat.run_combat()
                else:
                    testing = False

            self.draw_options()

            pygame.display.update()

        pygame.quit()