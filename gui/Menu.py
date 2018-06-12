from random import randint
import Render


class Menu():
    def __init__(self, guis):
        self.change_direction()
        
        self.render = Render.Render()
        
        self.guis = guis
    
    def change_direction(self):
        direct_1 = randint(0, 3)
        direct_2 = randint(0, 3)
        
        self.direction = (direct_1, direct_2)
        
        while self.direction == (2, 3) or self.direction == (0, 1) or self.direction == (3, 2) or self.direction == (1, 0):
            direct_2 = randint(0, 3)
            self.direction = (direct_1, direct_2)
    
    def close(self):
        for gui in self.guis:
            gui.pressed = False
        
    def update(self, main):
        main.player.move(self.direction, main.speed, False, main)
        
        if main.player.x >= main.opened_section.size_x * self.render.BLOCKWIDTH - main.window.SIZE[0]:
            self.direction = (main.player.LEFT, main.player.LEFT)
            main.player.move(self.direction, main.speed, False, main)
        if main.player.y >= main.opened_section.size_y * self.render.BLOCKWIDTH - main.window.SIZE[1]:
            self.direction = (main.player.UP, main.player.UP)
            main.player.move(self.direction, main.speed, False, main)
        
        if main.player.x <= 0:
            self.direction = (main.player.RIGHT, main.player.RIGHT)
            main.player.move(self.direction, main.speed, False, main)
        if main.player.y <= 0:
            self.direction = (main.player.DOWN, main.player.DOWN)
            main.player.move(self.direction, main.speed, False, main)
        
        for gui in self.guis:
            gui.update(main)
