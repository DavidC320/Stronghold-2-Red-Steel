# 1/2/2023
import pygame

def create_text(display, text, color, position, mode = "center", size = 22, font = "Britannic"):
    # a simple easy way to create text
    font = pygame.font.SysFont(font, size)
    text = font.render(text, False, color)
    if mode == "center":
        text_rect = text.get_rect(center=position)
    elif mode == "midleft":
        text_rect = text.get_rect(midleft=position)
    elif mode == "topleft":
        text_rect = text.get_rect(topleft=position)
    display.blit(text, text_rect)

def build_buttons(number, rect_info):
    # Creates the spin buttons
    # checks if the number is greater than ir less than 5
    if number > 5: number = 5

    button_list = []
    pos = [rect_info.topleft[0], rect_info.topleft[1]]
    button_size= [120, 300]
    for _ in range(number):
        button = pygame.Rect(pos[0], pos[1], button_size[0], button_size[1])
        pos[0] += button_size[0]
        button_list.append(button)
    return button_list

def build_info(offset, info, info_buttons):
    # shows the info inside fo the buttons
    None
    info_grab_length = len(info_buttons)
    start_number = offset

    info_list = []
    info_index = start_number
    for button in info_buttons:
        if info_index > info_grab_length:
            info_index = 0
        inf = [info[info_index], button.center]
        info_list.append(inf)
        print(info[info_index], button.center)
        info_index += 1
    return info_list
        
def show_info(info_list, display):
    for info in info_list:
        print(info)
        create_text(display, info[0], "white", info[1])


def display_buttons(buttons, display):
    for button in buttons:
        pygame.draw.rect(display, "Blue", button, 5)

pygame.init()
# screen
display_size = [900, 760]
display = pygame.display.set_mode(display_size)
# clock I have no idea what this does
clock = pygame.time.Clock()
# UI
control_panel = pygame.Rect(150, 460, display_size[0] - 300, 300)  # control panel


# stuff
info_offset= -1
info_list= ["A", "B", "C", "D", "E", "F"]
buttons= build_buttons(len(info_list), control_panel)
info= build_info(info_offset, info_list, buttons)

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # displays UI
    create_text(display, f"Items in info_list: {len(info_list)}", "White", [display_size[0]/2, display_size[1]/2])
    show_info(info, display)
    display_buttons(buttons, display)
    pygame.draw.rect(display, "Orange", control_panel, 2)
    # updates the game
    pygame.display.update()
pygame.quit()

# Notes
# The total number of visible buttons that are resonable are 5 at the size 120 x 300 with out 
# Now the goal is to display info