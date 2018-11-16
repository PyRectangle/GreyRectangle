from Frame.Render import Render
from Constants import *


class Editor:
    def __init__(self, main):
        self.main = main
        self.lastSpeed = self.main.player.lastSpeed
        self.x = self.main.player.x
        self.y = self.main.player.y
        self.size = 100
        self.step = BLOCK_SIZE / 100
        self.quit = False
        self.renderObj = Render(self.main.window)
        
    def update(self):
        if not self.quit:
            speed = self.main.window.dt * PLAYER_LOOP_SPEED + self.lastSpeed
            self.lastSpeed = speed - int(speed)
            speed = int(speed)
            for i in range(speed):
                if self.main.window.keys[self.main.config.config["Controls"]["goRight"]]:
                    self.x += PLAYER_SPEED
                if self.main.window.keys[self.main.config.config["Controls"]["goLeft"]]:
                    self.x -= PLAYER_SPEED
                if self.main.window.keys[self.main.config.config["Controls"]["goDown"]]:
                    self.y += PLAYER_SPEED
                if self.main.window.keys[self.main.config.config["Controls"]["goUp"]]:
                    self.y -= PLAYER_SPEED
            self.main.camera.size += self.main.window.mouseScroll * self.step
            self.size += self.main.window.mouseScroll
            if self.size <= 0:
                self.size = 1
                self.main.camera.size = self.step
            self.main.levelPreview.size = self.main.camera.size
            if self.main.window.keys[self.main.config.config["Controls"]["Escape"]]:
                self.quit = True
                self.main.menuHandler.show(self.main.menuHandler.editQuit)
    
    def render(self):
        self.renderObj.text(FONT, 45, "Zoom: " + str(self.size) + "%", True, (0, 0, 0), None, self.main.window.surface, 1, 1, True)
