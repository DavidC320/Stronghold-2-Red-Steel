# 12/8/2022
from Base_scripts.Character_Info import Base_Character
from Base_scripts.Game_info import character_life_forms
import pygame

class Stronghold_character(Base_Character):
    # This class is just he same as the Base Character class but is created to better use pygame and to de clutter a bunch of stuff.

    def __init__(self, 
        # info
        id, name, description, life_form, species, location, 
        # Stats
        level, xp, current_health, health, base_speed, base_stamina, defense, base_attack, inventory_slots, arm_slots, pocket_slots,
        # Skills
        fight_lv, fight_xp, hunt_lv, hunt_xp, cast_lv, cast_xp,
        # equipment
        head=None, body=None, legs=None, feet=None, back=None, hands=None, pockets=None):

        super().__init__(
            id, name, description, life_form, species, location, 
            level, xp, current_health, health, base_speed, base_stamina, defense, base_attack, inventory_slots, arm_slots, pocket_slots, 
            fight_lv, fight_xp, hunt_lv, hunt_xp, cast_lv, cast_xp, 
            head, body, legs, feet, back, hands, pockets)

        # character combat rectangle
        self.color = character_life_forms.get(self.life_form).get("color")
        self.rect = pygame.Rect(0, 0, 30, 70)

        # Character combat icon
        self.combat_icon_pos = (0, 0)
        self.config = None

        # setup
        self.build_combat_icon(True)
        
    def display_character(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def build_combat_icon(self, party_of_four):
        # Creates the combat icons.
        icon_configuration = {
            True : {
                "name" : 22,
                "health" : 22, 
                "size" : 150},
            False : {
                "name" : 14,
                "health" : 11, 
                "size" : 75},
        }
        config = icon_configuration.get(party_of_four)
        self.config = config
        x = self.combat_icon_pos[0]
        y = self.combat_icon_pos[1]

        # Icon image
        self.combat_icon_rect = pygame.Rect(x, y, config.get("size"), config.get("size"))
        
        # text
        self.build_icon_text()

    def build_icon_text(self):
        if self.config != None:
        #hi david // Armok
            self.name_text_rect = self.create_icon_text(.3, self.name, self.config.get("name"))
            self.health_text_rect = self.create_icon_text(.7, f"Hp: {self.current_hp} / {self.base_hp}", self.config.get("health"))
            self.stamina_text_rect = self.create_icon_text(.85, f"St: {self.current_stamina} / {self.base_stamina}", self.config.get("health"))

    def create_icon_text(self, y_offset, text, size):
        # This creates the text for the icon
        # getting the font size
        font = pygame.font.SysFont("Britannic", size)

        # getting the position
        text_position = self.combat_icon_rect.midtop
        name_offset = self.combat_icon_rect.size[0] * y_offset
        name_pos = (text_position[0], text_position[1] + name_offset)

        # setting up the text
        i_text = font.render(text, False, "White")
        i_rect = i_text.get_rect(center=name_pos)
        return i_text, i_rect

    def display_combat_icon(self, display, is_playable= True, is_selected= False, show_selected= False):
        # draws the characters combat icon.
        # icon
        if is_selected and show_selected:
            pygame.draw.rect(display, "Dark blue", self.combat_icon_rect)

        if is_playable:
            pygame.draw.rect(display, "Cyan", self.combat_icon_rect, 6)
        pygame.draw.rect(display, self.color, self.combat_icon_rect, 4)

        if self.dead:
            pygame.draw.rect(display, "Grey", self.combat_icon_rect)

        # text
        for text_rect in (self.name_text_rect, self.health_text_rect, self.stamina_text_rect):
            display.blit(text_rect[0], text_rect[1])