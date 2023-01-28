# 10/15/2022
# This is a tool box for misc funtions
import pygame

def create_text(text, color, position, mode = "center", size = 22, font = "Britannic", just_rects= False):
    font = pygame.font.SysFont(font, size)
    text = font.render(text, False, color)
    if mode == "center":
        text_rect = text.get_rect(center=position)
    elif mode == "midleft":
        text_rect = text.get_rect(midleft=position)
    elif mode == "midright":
        text_rect = text.get_rect(midright=position)
    elif mode == "topleft":
        text_rect = text.get_rect(topleft=position)

    return(text, text_rect)

def quick_display_text(display, text, color, position, mode = "center", size = 22, font = "Britannic", just_rects= False):
        text, text_rect = create_text(text, color, position, mode, size, font, just_rects)

        display.blit(text, text_rect)

def create_timer(current_time, wait_time, start_time):
    return current_time - start_time >= wait_time