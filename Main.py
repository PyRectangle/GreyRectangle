import os
import sys

try:
    os.chdir(os.path.dirname(sys.argv[0]))
except FileNotFoundError:
    pass

import pygame
import Player
import shutil
import Frame
import time
import Block as Blk
from level import Level
from config import Config
from resources import Music
from gui import Menu, Button, Selection_bar
from level.Section import LEVEL_PATH
from level.Level_selection import Level_selection


class Main():
    def __init__(self):
        self.output("Imported PyGame, Frame and Time.")
        self.output("Creating window...")
        
        self.pg = pygame
        self.window = Frame.Frame()
        self.player = Player.Player(self.window)
        self.block = Blk

        self.FONT_FILE = "freesansbold.ttf"
        self.PLAY = 0
        self.EDITOR = 1
        self.GUI_STANDARD = (100, 100, 100), (0, 0, 0), (100, 100, 200), (0, 0, 0), self.FONT_FILE, True
    
        for block in self.block.blocks:
            if block.texture != None:
                block.texture = self.window.resources.images[block.texture]
                if block.colorkey != None:
                    block.texture.set_colorkey(block.colorkey)
        
        self.musics = []
        for file in os.listdir("resources/music"):
            if not file == "license.html":
                self.musics.append(Music.Music(file, self))
                
        self.menu_active = True
        self.sec_count = 0
        self.levels = os.listdir("levels")
        self.level_selection = Level_selection(self)
        self.level_selection_active = False
        self.opened_level = Level.Level(os.listdir(LEVEL_PATH)[0])
        self.opened_section = self.opened_level.sections[0]
        self.opened_section.load()
        self.out = 0
        self.warning = None
        self.warning_count = 0
        self.escape_count = 0
        self.load_config()
        self.musics[self.opened_section.music].play()

        pos_fps_limit = self.fps_limit - 10

        self.start_menu = [Button.Button(210, 130, 220, 50, "Start", *self.GUI_STANDARD),
                           Button.Button(210, 190, 220, 50, "Editor", *self.GUI_STANDARD),
                           Button.Button(210, 250, 220, 50, "Settings", *self.GUI_STANDARD),
                           Button.Button(210, 310, 220, 50, "Exit", *self.GUI_STANDARD)]
        
        self.settings = [Button.Button(10, 410, 130, 50, "Back", *self.GUI_STANDARD),
                         Button.Button(150, 410, 480, 50, "Reset Window Size", *self.GUI_STANDARD),
                         Selection_bar.Selection_bar(self.volume, (200, 200, 200), True, 1, False, 3, 10, 10, 300, 50, "Volume", *self.GUI_STANDARD),
                         Selection_bar.Selection_bar(pos_fps_limit, (200, 200, 200), False, 90, True, 0, 10, 70, 500, 50, "Fps limit", *self.GUI_STANDARD)]
        
        self.level_selection_start = [Button.Button(10, 410, 140, 50, "Back", *self.GUI_STANDARD),
                                      Button.Button(490, 410, 140, 50, "Start", *self.GUI_STANDARD)]
        
        self.level_selection_editor = self.level_selection_start + [Button.Button(10, 10, 260, 40, "Delete Level", *self.GUI_STANDARD),
                                                                    Button.Button(370, 10, 260, 40, "Create Level", *self.GUI_STANDARD)]
        
        self.menu = Menu.Menu(self.start_menu)
        
        self.update_fps_limit()
        self.clock = self.pg.time.Clock()
        
        self.output("Starting main loop...")
        
        self.loop()
        
    def load_config(self):
        self.output("Loading Settings from config.txt")
        
        self.config = Config()
        self.fps_limit = int(self.config.load("fps_limit", 200))
        self.volume = float(self.config.load("volume", 100))
        self.pg.mixer.music.set_volume(self.volume)


    def save_config(self):
        self.output("Saving Settings to config.txt")
        
        self.config.save("volume", self.volume, "w")
        self.config.save("fps_limit", self.fps_limit, "a")

    def terminate(self):
        self.save_config()
        
        self.output("Removing PyCaches...")
        
        for i in "", "gui/", "level/", "resources/":
            shutil.rmtree(i + "__pycache__")
        
        self.output("Exit program...")
        
    def loop(self):
        last_speed_rest = 0
        
        while self.window.is_open:
            self.clock.tick(self.fps_limit)
            dt = self.clock.get_time()
            self.fps = self.clock.get_fps()

            self.warning_count -= 1
            if int(self.warning_count) == 1:
                self.warning = None
            if self.warning_count < 0:
                self.warning_count = 0
        
            self.sec_count += 1
            if self.menu_active and self.sec_count >= int(self.fps * ((self.opened_section.size_x + self.opened_section.size_y) / 2) / 10):
                self.menu.change_direction()
                self.sec_count = 0
        
            self.speed = dt / 5 + last_speed_rest
            last_speed_rest = self.speed - int(self.speed)
        
            self.window.update()
           
            self.escape_count -= 1
            if self.escape_count < 0:
                self.escape_count = 0
        
            if self.window.get_key_press(self.pg.K_ESCAPE) and self.escape_count == 0:
                if self.level_selection_active:
                    self.level_selection.close(self)
                    self.escape_count = self.fps / 2
                elif not self.menu_active:
                    self.level_selection.open(self)
                    self.escape_count = self.fps / 2
                else:
                    self.window.is_open = False
        
            if self.start_menu[3].pressed:
                self.window.is_open = False
            
            if self.start_menu[2].pressed:
                self.warning = None
        
                self.output("Opening settings...")
                
                self.menu.close()
                self.menu = Menu.Menu(self.settings)
           
            if self.start_menu[1].pressed:
                self.out = self.EDITOR
                self.level_selection.open(self)
           
            if self.start_menu[0].pressed:
                self.out = self.PLAY
                self.level_selection.open(self)
            
            if self.settings[0].pressed:
                self.warning = None
        
                self.save_config()
                
                self.output("Closing settings...")
                
                self.menu.close()
                self.menu = Menu.Menu(self.start_menu)
            if self.settings[1].pressed and self.escape_count == 0:
                self.pg.display.quit()
                self.pg.display.init()
            
                os.environ['SDL_VIDEO_WINDOW_POS'] = self.window.WINDOW_START_POS
            
                self.window.resize(self.window.SIZE, False, False)
                self.window.fullscreen = False
            
                self.pg.display.set_caption("GreyRectangle")
            
                self.escape_count = 3
                
            if self.settings[3].pressed:
                self.update_fps_limit()
        
            if self.menu_active:
                self.menu.update(self)
       
            if self.settings[2].pressed:
                self.volume = self.settings[2].procent
                self.pg.mixer.music.set_volume(self.volume)

            if self.level_selection_active:
                if self.level_selection_editor[2].pressed and self.escape_count == 0:
                    if self.level_selection.count > 1:
                        Level.Level(self.levels[self.level_selection.pos]).delete()
                        self.level_selection.update(self)

                        self.escape_count = self.fps
                    else:
                        self.create_warning("Warning: Cannot delete the last level!")
            
                        self.warning_count = self.fps * 3
       
                if self.level_selection_start[0].pressed:
                    self.level_selection.close(self)
          
                if self.level_selection_start[1].pressed:
                    self.start_level()
     
                self.level_selection.update(self)
        
            if not self.menu_active:
                if self.out == self.PLAY:
                    self.player.make_movements(True, self)
      
            self.window.render.render(self)
            self.pg.display.update()
      
        self.terminate()
    
    def start_level(self):
        self.player.x = 0
        self.player.y = 0

        self.level_selection_active = False
        self.menu_active = False
        self.menu = Menu.Menu([])
    
    def update_fps_limit(self):
        self.settings[3].draw_other = self.settings[3].procent + 10
        self.fps_limit = self.settings[3].draw_other
        if self.settings[3].draw_other == 100:
            self.settings[3].draw_other = "Unlimited"
            self.fps_limit = 0
        self.settings[3].update_surface()
    
    def create_warning(self, warning):
        self.warning = self.window.render.text(self.FONT_FILE, 35, warning, True, (255, 0, 0), None, None, 0, 0, False)
            
    def output(self, text):
        self.time = time.localtime()
        print("[" + str(self.time.tm_hour) + ":" + str(self.time.tm_min) + ":" + str(self.time.tm_sec) + "] " + text)


if __name__ == "__main__":
    Main()
