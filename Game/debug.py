#10/11/2022
import pygame
from pygame import mixer

from scripts import Movement, Player

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
        self.player = Player.Player()
        self.move_test = Movement.Movement(self.display,  self.clock, self.player)

        # options information
        self.options = ("movement test")
        self.current = 0

    def run_debug(self):
        running = True
        while running:
            running = self.move_test.run_debug()

        pygame.quit()