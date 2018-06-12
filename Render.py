import pygame
from gui.Base_gui import SELECTION_BAR

RESOURCE_PATH = "resources/"


class Render():
    def __init__(self):
        self.BLOCKS_X = 11
        self.BLOCKS_Y = 9
        self.BLOCKWIDTH = 64
    
    def text(self, file, size, text, antialias, color, background, surface, x, y, blit = True):
        text_surface = pygame.font.Font(RESOURCE_PATH + file, size).render(text, antialias, color, background)
        
        if x == None or y == None:
            x = surface.get_width() / 2 - text_surface.get_width() / 2
            y = surface.get_height() / 2 - text_surface.get_height() / 2
        
        if blit:
            surface.blit(text_surface, (x, y))
        else:
            return text_surface
        
    def menu(self, main):
        for gui in main.menu.guis:
            main.window.surface.blit(gui.surface, (gui.x, gui.y))
            if gui.type == SELECTION_BAR:
                main.window.surface.blit(gui.cursor_surface, (int(gui.x + gui.cursor_pos - gui.width / 25 / 2), int(gui.y - gui.height * 0.1)))
    
    def blocks(self, main):
        block_pos_x = main.player.x / self.BLOCKWIDTH
        block_pos_y = main.player.y / self.BLOCKWIDTH
    
        in_block_pos_x = (block_pos_x - int(block_pos_x)) * self.BLOCKWIDTH
        in_block_pos_y = (block_pos_y - int(block_pos_y)) * self.BLOCKWIDTH
        
        region = main.opened_section.region
    
        for y in range(self.BLOCKS_Y):
            for x in range(self.BLOCKS_X):
                try:
                    array_pos_x = x + int(block_pos_x)
                    array_pos_y = y + int(block_pos_y)
        
                    block = main.block.blocks[region[array_pos_y][array_pos_x]]
                    
                    if block.texture != None and array_pos_x >= 0 and array_pos_y >= 0:
                        main.window.surface.blit(block.texture, (x * self.BLOCKWIDTH - in_block_pos_x, y * self.BLOCKWIDTH - in_block_pos_y))
                except IndexError:
                    pass

    def render(self, main):
        main.window.surface.fill((255, 255, 255))
      
        if main.level_selection_active:
            main.level_selection.render(main)
        else:
            self.blocks(main)
    
        if main.menu_active:
            self.menu(main)
        else:
            self.text(main.FONT_FILE, 25, "FPS:" + str(int(main.fps)), True, (0, 0, 0), None, main.window.surface, 1, 1, True)
            if main.out == main.PLAY:
                main.player.render()
   
        if main.warning != None:
            main.window.surface.blit(main.warning, (320 - main.warning.get_width() / 2, 420))
        
        main.window.screen.blit(pygame.transform.scale(main.window.surface, main.window.surface_size), (main.window.surface_x, main.window.surface_y))
