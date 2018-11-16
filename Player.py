from Constants import *
import pygame


class Player:
    def __init__(self, main):
        self.main = main
        self.lastSpeed = 0
        self.x = 0
        self.y = 0
        self.quitMenu = False
    
    def getBlockAt(self, x, y):
        if x < 0 or y < 0:
            return None
        if self.main.camera.level != None:
            grid = self.main.camera.level.data.regionsGrid
            index = [x, y]
            regionIndex = [int(index[0] / 16), int(index[1] / 16)]
            for i in range(2):
                index[i] -= regionIndex[i] * 16
            try:
                region = grid[regionIndex[1]][regionIndex[0]]
                if region.loaded:
                    return region.region[index[1]][index[0]]
            except IndexError:
                return None
        return None
    
    def collide(self, direct):
        return False
    
    def update(self):
        if not self.quitMenu:
            speed = self.main.window.dt * PLAYER_LOOP_SPEED + self.lastSpeed
            self.lastSpeed = speed - int(speed)
            speed = int(speed)
            for i in range(speed):
                if self.main.window.keys[self.main.config.config["Controls"]["goRight"]]:
                    if not self.collide("x+"):
                        self.x += PLAYER_SPEED
                if self.main.window.keys[self.main.config.config["Controls"]["goLeft"]]:
                    if not self.collide("x-"):
                        self.x -= PLAYER_SPEED
                if self.main.window.keys[self.main.config.config["Controls"]["goDown"]]:
                    if not self.collide("y+"):
                        self.y += PLAYER_SPEED
                if self.main.window.keys[self.main.config.config["Controls"]["goUp"]]:
                    if not self.collide("y-"):
                        self.y -= PLAYER_SPEED
            self.xPx = (self.x - (self.main.camera.x - self.main.window.surface.get_width() / 288)) * 144
            self.yPx = (self.y - (self.main.camera.y - self.main.window.surface.get_height() / 288)) * 144
            self.coords = [[self.xPx - PLAYER_SIZE[0], self.yPx - PLAYER_SIZE[1]], [self.xPx + PLAYER_SIZE[0], self.yPx - PLAYER_SIZE[1]],
                           [self.xPx + PLAYER_SIZE[0], self.yPx + PLAYER_SIZE[1]], [self.xPx - PLAYER_SIZE[0], self.yPx + PLAYER_SIZE[1]]]
            if self.main.window.keys[self.main.config.config["Controls"]["Escape"]]:
                self.quitMenu = True
                self.main.menuHandler.show(self.main.menuHandler.playQuit)
    
    def render(self):
        pygame.draw.polygon(self.main.window.surface, (150, 150, 150), self.coords)
