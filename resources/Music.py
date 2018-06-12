import pygame

MUSIC_PATH = "resources/music/"

playing_sound = ""


class Music():
    def __init__(self, name, main):
        self.name = name
        self.main = main
    
    def play(self):
        global playing_sound
        
        self.main.output("Playing " + self.name + "...")
 
        if playing_sound != self.name:
            pygame.mixer.music.load(MUSIC_PATH + self.name)
            pygame.mixer.music.play(-1, 0)
        
            playing_sound = self.name
