import pygame
import screeninfo
import Render
import os
from resources import Resources


class Frame():
    def __init__(self):
        self.pg = pygame
        self.pg.init()
        
        self.SIZE = [640, 480]
        self.SURFACE_SIZE = self.SIZE
        self.TEXTURES = ["stone.png", "grass.png", "dirt.png", "obsidian.png", "portal.png", "heart_0.png", "ladder.png", "dorns.png", "lever_0.png", "piston.png", "checkpoint_0.png",
                         "lava.png", "coal_ore.png", "diamond_ore.png", "iron_ore.png", "gold_ore.png", "lapis_ore.png", "redstone_ore.png", "water.png", "gravity.png", "gold_block.png",
                         "sand.png", "cactus.png", "sandstone.png", "quicksand.png", "teleporter.png", "planks.png", "button_0.png", "gravel.png"]
        self.RESOLUTION = screeninfo.get_monitors()[0]
        self.WINDOW_RES_MULTIPLIER = self.SIZE[1] / self.SIZE[0]
        self.WINDOW_START_POS = "%d, %d" % (self.RESOLUTION.width / 2 - self.SIZE[0] / 2, self.RESOLUTION.height / 2 - self.SIZE[1] / 2)

        os.environ['SDL_VIDEO_WINDOW_POS'] = self.WINDOW_START_POS
        
        self.screen = self.pg.display.set_mode(self.SIZE, self.pg.RESIZABLE)
        
        self.pg.display.set_caption("GreyRectangle")

        self.render = Render.Render()
        
        self.show_title_screen()
        
        self.resources = Resources.Resources()
        self.resources.load_textures(self.TEXTURES)
        
        self.pg.time.wait(1000)
        
        self.size = self.SIZE
        self.is_open = True
 
        self.keys = []
        self.mouse_scroll = 0
        self.mouse_pos = [0, 0]
        self.mouse_pressed = (0, 0, 0)

        self.surface = self.pg.Surface(self.SIZE)
        self.surface_x = 0
        self.surface_y = 0
                
        self.surface_size = self.SIZE
        self.fullscreen = False
    
    def show_title_screen(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.pg.transform.scale(self.pg.image.load("resources/images/logo.png"), (128, 128)), (256, 128))
        self.render.text("freesansbold.ttf", 45, "Developed by PyRectangle", True, (255, 0, 0), None, self.screen, 20, 259)
        self.pg.display.update()
        
    def get_mouse_states(self):
        try:
            mouse_pos_tuple = self.pg.mouse.get_pos()
        
            self.mouse_pos = [mouse_pos_tuple[0], mouse_pos_tuple[1]]
            self.mouse_pos[0] -= self.surface_x
            self.mouse_pos[1] -= self.surface_y
     
            for i in range(2):
                self.mouse_pos[i] /= self.surface_size[i] / self.SIZE[i]
                self.mouse_pos[i] = int(self.mouse_pos[i])
 
            self.mouse_pressed = self.pg.mouse.get_pressed()
        except ZeroDivisionError:
            pass

    def resize(self, size, noframe, set_pos = True):
        if set_pos:
            os.environ['SDL_VIDEO_WINDOW_POS'] = ""

        self.size = list(size)
        
        if noframe:
            self.screen = self.pg.display.set_mode(self.size, self.pg.RESIZABLE | self.pg.NOFRAME)
        else:
            self.screen = self.pg.display.set_mode(self.size, self.pg.RESIZABLE)
       
        self.surface_size = self.size

        do = True
        resize_count = 0
        
        while self.surface_size[0] > self.size[0] or self.surface_size[1] > self.size[1] or do:
            resize_count += 1
            do = False
    
            if resize_count > 2:
                self.surface_size[0] -= 1
                self.surface_size[1] -= 1
            
            if self.surface_size[0] < self.surface_size[1] or resize_count > 1:
                self.surface_size = [self.surface_size[0], int(self.surface_size[0] * self.WINDOW_RES_MULTIPLIER)]
            elif self.surface_size[0] > self.surface_size[1] or resize_count > 1:
                self.surface_size = [int(self.surface_size[1] / self.WINDOW_RES_MULTIPLIER), self.surface_size[1]]
        
        self.surface_x = int(self.size[0] / 2 - self.surface_size[0] / 2)
        self.surface_y = int(self.size[1] / 2 - self.surface_size[1] / 2)
    
    def get_key_press(self, key):
        for i in self.keys:
            if i == key:
                return True
        return False
    
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (0, 0)
      
            self.resize((self.RESOLUTION.width, self.RESOLUTION.height), self.fullscreen, self.fullscreen)
        else:
            os.environ['SDL_VIDEO_WINDOW_POS'] = self.WINDOW_START_POS
            
            self.resize(self.SIZE, False, False)
    
    def update(self):
        self.mouse_scroll = 0
        
        for event in self.pg.event.get():
            if event.type == self.pg.QUIT:
                self.is_open = False
        
            if event.type == self.pg.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.mouse_scroll = -1
                if event.button == 5:
                    self.mouse_scroll = 1
        
            if event.type == self.pg.KEYDOWN:
                if event.key == self.pg.K_F11:
                    self.toggle_fullscreen()
            
                self.keys.append(event.key)
        
            if event.type == self.pg.KEYUP:
                try:
                    self.keys.remove(event.key)
                except ValueError:
                    pass
          
            if event.type == self.pg.VIDEORESIZE:
                print("resizing from " + str(self.size) + " to " + str(event.size))
                self.size = event.size
                self.resize(self.size, False)
                print("resized")

        self.get_mouse_states()
