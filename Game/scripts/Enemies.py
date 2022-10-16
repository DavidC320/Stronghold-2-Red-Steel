# 10/14/2022
import pygame

from Tool_box import create_text

class Enemy_rectangel:
    def __init__(self, character_info):
        self.data = character_info  # A Character class
        self.rect = pygame.Rect(0, 0, 30, 70)
        
    def display_character(self, screen):
        pygame.draw.rect(screen, self.data.color, self.rect)
        text_pos = (self.rect.midbottom[0], self.rect.midbottom[1] + 5)