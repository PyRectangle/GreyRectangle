import pygame
import Render
import os


class Level_selection():
    def __init__(self, main):
                
        self.pg = pygame
        
        self.pos = 0
        self.count = 0
        self.up_down_count = 0
        
        self.Render = Render.Render()
        
        self.WIDTH = 80
        self.HALF_WIDTH = self.WIDTH / 2
        self.COLOR = (255, 0, 0)
        self.SELECT_COLOR = (0, 255, 0)
        self.BOTTOM_COLOR = (255, 255, 0)
        
        for level in main.levels:
            self.count += 1
          
    def render(self, main):
        main.window.surface.fill(self.COLOR)

        y = main.window.SIZE[1] / 2
     
        self.pg.draw.line(main.window.surface, self.SELECT_COLOR, (0, y), (main.window.SIZE[0], y), self.WIDTH)
        
        for i in range(-3, 3, 1):
            try:
                array_pos = i + self.pos
                if array_pos >= 0:
                    self.Render.text("freesansbold.ttf", self.WIDTH - 10, main.levels[array_pos], True, (0, 0, 0), None, main.window.surface, 10, i * self.WIDTH + 200)
            except IndexError:
                pass

        y = 440
        
        self.pg.draw.line(main.window.surface, self.BOTTOM_COLOR, (0, y), (main.window.SIZE[0], y), self.WIDTH)
        
        if main.out == main.EDITOR:
            y = 20
        
        self.pg.draw.line(main.window.surface, self.BOTTOM_COLOR, (0, y), (main.window.SIZE[0], y), self.WIDTH)
        
    def update(self, main):
        self.up_down_count -= 1
        if self.up_down_count < 0:
            self.up_down_count = 0
    
        if main.window.get_key_press(self.pg.K_UP) and self.up_down_count == 0:
            self.pos -= 1
            self.up_down_count = main.fps / 10
        if main.window.get_key_press(self.pg.K_DOWN) and self.up_down_count == 0:
            self.pos += 1
            self.up_down_count = main.fps / 10

        self.pos += main.window.mouse_scroll
        
        window_height_half = main.window.SIZE[1] / 2
        mouse_pressed = main.window.mouse_pressed != (0, 0, 0)

        if main.window.mouse_pos[1] < window_height_half - self.HALF_WIDTH and mouse_pressed and self.up_down_count == 0 and main.window.mouse_pos[1] > 60:
            self.pos -= 1
            self.up_down_count = main.fps / 10
        if main.window.mouse_pos[1] > window_height_half + self.HALF_WIDTH and mouse_pressed and self.up_down_count == 0 and main.window.mouse_pos[1] < 400:
            self.pos += 1
            self.up_down_count = main.fps / 10

        if mouse_pressed and window_height_half - self.HALF_WIDTH < main.window.mouse_pos[1] < window_height_half + self.HALF_WIDTH and main.escape_count == 0:
            main.start_level()
        
        if self.pos < 0:
            self.pos = 0
        if self.pos >= self.count:
            self.pos = self.count - 1

        pos = self.pos
        main.levels = os.listdir("levels")
        
        self = Level_selection(main)
        self.pos = pos
    
    def open(self, main):
        main.escape_count = main.fps / 5
        
        main.menu_active = True
        main.warning = None
        
        main.output("Opening level selection...")
        
        main.menu.close()
        
        if main.out == main.PLAY:
            main.menu.guis = main.level_selection_start
        else:
            main.menu.guis = main.level_selection_editor

        main.level_selection_active = True
        
    def close(self, main):
        main.warning = None
        
        main.output("Closing level selection...")
        
        main.menu.close()
        main.menu.guis = main.start_menu
        main.level_selection_active = False
