# 1/28/2023
from pygame import mixer
from random import choice
import os

mixer.init()

class Music_manager:
    def __init__(self):
        self.music_list = []
        self.sfx_list = []
        self.grab_music()
        self.grab_sfx()

    def grab_sfx(self):
        music = []
        music_folder = r"Sfx//"
        for file in os.listdir(music_folder):
            file_path = music_folder+ file
            sound =  mixer.Sound(file_path)
            music.append(sound)
        self.sfx_list = music

    def play_sound(self, index):
        self.sfx_list[index].set_volume(.05)
        self.sfx_list[index].play()


    def grab_music(self):
        music = []
        music_folder = r"Music//"
        for file in os.listdir(music_folder):
            file_path = music_folder+ file
            music.append(file_path)
        self.music_list = music

    def stop_music(slef):
        mixer.music.stop()

    def play_music(self):
        self.stop_music()
        music_choice = choice(self.music_list)
        print(music_choice)
        mixer.music.load(music_choice)
        mixer.music.set_volume(.07)
        mixer.music.play(-1, fade_ms=2000)

Music_manager().grab_music()