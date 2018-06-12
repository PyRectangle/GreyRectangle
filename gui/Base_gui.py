import Render
import pygame

BUTTON = 0
SELECTION_BAR = 1


class Base_gui():
    def __init__(self, x, y, width, height, text, color, frame_color, select_color, text_color, font_file, antialias):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.frame_color = frame_color
        self.select_color = select_color
        self.text_color = text_color
        self.font_file = font_file
        self.antialias = antialias
        
        self.pressed = False
        self.mouse_touches_button = False
        self.was_touched = False
        
        self.render = Render.Render()
        
        self.surface = pygame.Surface((self.width, self.height))
    
    def update(self, main):
        self.mouse_touches_button = main.window.mouse_pos[0] <= self.x + self.width and main.window.mouse_pos[0] >= self.x and main.window.mouse_pos[1] <= self.y + self.height and \
                                    main.window.mouse_pos[1] >= self.y
        if self.was_touched != self.mouse_touches_button:
            self.update_surface()

        self.was_touched = self.mouse_touches_button
        
        self.pressed = self.mouse_touches_button and main.window.mouse_pressed != (0, 0, 0)
    
    def update_surface(self):
        if self.mouse_touches_button:
            self.surface.fill(self.select_color)
        else:
            self.surface.fill(self.color)

        self.render.text(self.font_file, self.height, self.text, self.antialias, self.text_color, None, self.surface, None, None)
        
        pygame.draw.lines(self.surface, self.frame_color, 4,[[0, 0], [self.width - 1, 0], [self.width - 1, self.height - 1], [0, self.height - 1], [0, 0]], 1)
