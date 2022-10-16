# 10/15/2022
# This is a tool box for misc funtions
import pygame

def create_text(display, text, color, position, mode = "center", size = 22, font = "Britannic"):
        font = pygame.font.SysFont(font, size)
        text = font.render(text, False, color)
        if mode == "center":
            text_rect = text.get_rect(center=position)
        elif mode == "midleft":
            text_rect = text.get_rect(midleft=position)
        elif mode == "topleft":
            text_rect = text.get_rect(topleft=position)
        display.blit(text, text_rect)