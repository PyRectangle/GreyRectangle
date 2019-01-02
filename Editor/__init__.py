from Editor.BlockSelection import BlockSelection
from Frame.Render import Render
from Constants import *
import pygame


class Editor:
    def __init__(self, main):
        self.main = main
        self.lastSpeed = self.main.player.lastSpeed
        self.x = self.main.player.x
        self.y = self.main.player.y
        self.size = 100
        self.step = BLOCK_SIZE / 100
        self.quit = False
        self.steps = []
        self.edit = None
        self.selectedBlock = 0
        self.actions = None
        self.setSpawn = False
        self.blockSelection = BlockSelection(self.main, self)
        self.renderObj = Render(self.main.window)
    
    def update(self):
        if not self.quit:
            self.blockSelection.update()
            speed = self.main.window.dt * PLAYER_LOOP_SPEED * 100 + self.lastSpeed
            self.lastSpeed = speed - int(speed)
            speed = int(speed)
            for i in range(speed):
                if self.main.window.keys[self.main.config.config["Controls"]["goRight"]]:
                    self.x += PLAYER_SPEED / self.size
                if self.main.window.keys[self.main.config.config["Controls"]["goLeft"]]:
                    self.x -= PLAYER_SPEED / self.size
                if self.main.window.keys[self.main.config.config["Controls"]["goDown"]]:
                    self.y += PLAYER_SPEED / self.size
                if self.main.window.keys[self.main.config.config["Controls"]["goUp"]]:
                    self.y -= PLAYER_SPEED / self.size
            if self.main.window.keys[self.main.config.config["Controls"]["Zoom"]]:
                self.main.camera.size += self.main.window.mouseScroll * self.step
                self.size += self.main.window.mouseScroll
                if self.size <= 9:
                    self.size = 10
                    self.main.camera.size = self.step * 10
                if self.size > 200:
                    self.size = 200
                    self.main.camera.size = self.step * 200
                self.main.levelPreview.size = self.main.camera.size
            elif self.main.window.mouseScroll != 0:
                self.blockSelection.enable(True, self.main.window.mouseScroll)
            self.selectedBlock = self.blockSelection.block
            if self.actions != None:
                blockSize = BLOCK_SIZE * self.size / 100
                self.mouseBlockPos = [int(self.x - SURFACE_SIZE[0] / 2 / blockSize + self.main.window.mousePos[0] / blockSize + 0.5),
                                      int(self.y - SURFACE_SIZE[1] / 2 / blockSize + self.main.window.mousePos[1] / blockSize + 0.5)]
                if self.setSpawn:
                    self.actions.level.data.jsonData["SpawnX"] = self.mouseBlockPos[0] + self.actions.level.data.smallest[0] * 16
                    self.actions.level.data.jsonData["SpawnY"] = self.mouseBlockPos[1] + self.actions.level.data.smallest[0] * 16 - \
                                                                 (PLAYER_SIZE[1] * 2 - 144 + 1) / 2 / blockSize * self.size / 100
                    self.actions.level.data.loadJsonData()
                    if self.main.window.mousePressed != (0, 0, 0):
                        self.setSpawn = False
                else:
                    do = True
                    for i in self.main.window.guiHandler.allGuis:
                        if i.mouseTouchesButton:
                            do = False
                    if do:
                        if list(self.main.window.mousePressed)[0]:
                            self.actions.setblock(*self.mouseBlockPos, self.selectedBlock + 1, self.blockSelection.data.copy())
                        if list(self.main.window.mousePressed)[2]:
                            self.actions.setblock(*self.mouseBlockPos, 0, [])
            if self.main.window.keys[self.main.config.config["Controls"]["Escape"]]:
                self.quit = True
                self.main.menuHandler.show(6)
    
    def render(self):
        if self.actions != None:
            blockSize = BLOCK_SIZE * self.size / 100
            playerSize = [PLAYER_SIZE[0] * self.size / 100, PLAYER_SIZE[1] * self.size / 100]
            xPx = (self.actions.level.data.spawnX - self.x) * blockSize + SURFACE_SIZE[0] / 2
            yPx = (self.actions.level.data.spawnY - self.y) * blockSize + SURFACE_SIZE[1] / 2
            coords = [[xPx - playerSize[0], yPx - playerSize[1]], [xPx + playerSize[0], yPx - playerSize[1]],
                      [xPx + playerSize[0], yPx + playerSize[1]], [xPx - playerSize[0], yPx + playerSize[1]]]
            pygame.draw.polygon(self.main.window.surface, (150, 150, 150), coords)
        self.renderObj.text(FONT, 45, "Zoom: " + str(self.size) + "%", True, (0, 0, 0), None, self.main.window.surface, 1, 1, True)
        self.blockSelection.render()
