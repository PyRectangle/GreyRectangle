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
        self.active = False
        self.activeCount = 0
        self.size = 100
        self.step = BLOCK_SIZE / 100
        self.quit = False
        self.steps = []
        self.edit = None
        self.selectedBlock = 0
        self.actions = None
        self.changed = False
        self.setSpawn = False
        self.playerCoords = []
        self.blockSelection = BlockSelection(self.main, self)
        self.renderObj = Render(self.main.window)
        self.select = False
        self.selectRegions = False
        self.selection = None
        self.selectionTry = None
        self.actionsOpen = False
        self.lastMousePos = None
        self.cloning = False
    
    def update(self):
        if not self.quit and self.active:
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
            if list(self.main.window.mousePressed)[1]:
                if self.lastMousePos != None and self.lastMousePos[0] != self.main.window.mousePos[0] and self.lastMousePos[1] != self.main.window.mousePos[1]:
                    relativePos = [self.main.window.mousePos[0] - self.lastMousePos[0], self.main.window.mousePos[1] - self.lastMousePos[1]]
                    self.x -= relativePos[0] / self.size
                    self.y -= relativePos[1] / self.size
            self.lastMousePos = self.main.window.mousePos.copy()
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
                self.mouseBlockPos = [self.x - SURFACE_SIZE[0] / 2 / blockSize + self.main.window.mousePos[0] / blockSize,
                                      self.y - SURFACE_SIZE[1] / 2 / blockSize + self.main.window.mousePos[1] / blockSize]
                if self.mouseBlockPos[0] < 0:
                    self.mouseBlockPos[0] -= 0.5
                else:
                    self.mouseBlockPos[0] += 0.5
                if self.mouseBlockPos[1] < 0:
                    self.mouseBlockPos[1] -= 0.5
                else:
                    self.mouseBlockPos[1] += 0.5
                self.mouseBlockPos[0] = int(self.mouseBlockPos[0])
                self.mouseBlockPos[1] = int(self.mouseBlockPos[1])
                if not self.cloning:
                    if self.setSpawn:
                        self.changed = True
                        self.actions.level.data.jsonData["SpawnX"] = self.mouseBlockPos[0] + self.actions.level.data.smallest[0] * 16
                        self.actions.level.data.jsonData["SpawnY"] = self.mouseBlockPos[1] + self.actions.level.data.smallest[1] * 16 - \
                                                                    (PLAYER_SIZE[1] * 2 - 144 + 1) / 2 / blockSize * self.size / 100
                        self.actions.level.data.loadJsonData()
                        if self.main.window.mousePressed != (0, 0, 0):
                            self.setSpawn = False
                    else:
                        do = True
                        for i in self.main.window.guiHandler.allGuis:
                            if i.mouseTouchesButton:
                                do = False
                        if do and not self.select:
                            if list(self.main.window.mousePressed)[2]:
                                self.changed = True
                                self.actions.setblock(self.mouseBlockPos[0], self.mouseBlockPos[1], self.selectedBlock, self.blockSelection.data.copy())
                            if list(self.main.window.mousePressed)[0]:
                                self.changed = True
                                self.actions.setblock(self.mouseBlockPos[0], self.mouseBlockPos[1], 0, [])
                        if (do and self.select and self.selectionTry != None) or (do and self.selectionTry != None and self.selectRegions):
                            self.selection = []
                            if self.selectRegions:
                                self.selectionTry[1] = [int(self.mouseBlockPos[0] / 16), int(self.mouseBlockPos[1] / 16)]
                                self.selection.append(self.selectionTry[0].copy())
                                self.selection.append(self.selectionTry[1].copy())
                                for y in range(2):
                                    for x in range(2):
                                        self.selection[y][x] *= 16
                                for i in range(2):
                                    if self.selection[1][i] >= self.selection[0][i]:
                                        self.selection[1][i] += 15
                                    if self.selection[1][i] < self.selection[0][i]:
                                        self.selection[0][i] += 15
                            else:
                                self.selectionTry[1] = self.mouseBlockPos.copy()
                                self.selection.append(self.selectionTry[0].copy())
                                self.selection.append(self.selectionTry[1].copy())
                            for i in range(2):
                                if self.selection[0][i] > self.selection[1][i]:
                                    back = self.selection[0][i]
                                    self.selection[0][i] = self.selection[1][i]
                                    self.selection[1][i] = back
                            if self.main.window.keys[self.main.config.config["Controls"]["GuiPresser"]]:
                                self.select = False
                                self.actionsOpen = self.main.menuHandler.actionMenu.created
                                if self.selectRegions:
                                    self.main.menuHandler.show(self.main.menuHandler.regionMenu)
                                else:
                                    self.main.menuHandler.show(self.main.menuHandler.blockMenu)
                                self.selectRegions = False
                else:
                    if list(self.main.window.mousePressed)[0] or list(self.main.window.mousePressed)[2]:
                        self.actions.clone(*self.selection[0], *self.selection[1], *self.mouseBlockPos)
                        self.cloning = False
                        self.changed = True
            if self.main.window.keys[self.main.config.config["Controls"]["Escape"]]:
                self.quit = True
                self.main.menuHandler.show(6)

    def selectBlock(self):
        self.select = True
        self.selectionTry = [self.mouseBlockPos.copy(), []]
    
    def selectRegion(self):
        self.selectionTry = [[int(self.mouseBlockPos[0] / 16), int(self.mouseBlockPos[1] / 16)], []]
        self.regionSelection = None
        self.selectRegions = True
    
    def deselect(self):
        self.regionSelection = None
        self.selection = None
        self.selectionTry = None
        self.select = False
        self.selectRegions = False
        if self.actionsOpen:
            self.main.menuHandler.show(self.main.menuHandler.actionMenu)
        else:
            self.main.menuHandler.remove()
    
    def fill(self):
        self.actions.fill(*self.selection[0], *self.selection[1], self.selectedBlock, self.blockSelection.data.copy())
        self.changed = True

    def clone(self):
        self.cloning = True
    
    def removeRegions(self):
        selection = self.selectionTry
        for i in range(2):
            if selection[0][i] > selection[1][i]:
                back = selection[0][i]
                selection[0][i] = selection[1][i]
                selection[1][i] = back
        self.actions.deleteRegion(selection[0][0] + self.actions.level.data.smallest[0], selection[0][1] + self.actions.level.data.smallest[1])
        for y in range(selection[1][1] - selection[0][1] + 1):
            for x in range(selection[1][0] - selection[0][0] + 1):
                self.actions.deleteRegion(selection[0][0] + x + self.actions.level.data.smallest[0], selection[0][1] + y + self.actions.level.data.smallest[1])
        self.deselect()
        self.changed = True

    def render(self):
        active = self.active
        self.activeCount += self.main.window.dt / 800
        if self.activeCount >= 1:
            self.activeCount = 0
            self.active = True
        if self.actions != None:
            blockSize = BLOCK_SIZE * self.size / 100
            playerSize = [PLAYER_SIZE[0] * self.size / 100, PLAYER_SIZE[1] * self.size / 100]
            xPx = (self.actions.level.data.spawnX - self.x) * blockSize + SURFACE_SIZE[0] / 2
            yPx = (self.actions.level.data.spawnY - self.y) * blockSize + SURFACE_SIZE[1] / 2
            self.playerCoords = [[xPx - playerSize[0], yPx - playerSize[1]], [xPx + playerSize[0], yPx - playerSize[1]],
                                 [xPx + playerSize[0], yPx + playerSize[1]], [xPx - playerSize[0], yPx + playerSize[1]]]
            pygame.draw.polygon(self.main.window.surface, (150, 150, 150), self.playerCoords)
        self.renderObj.text(FONT, 45, "Zoom: " + str(self.size) + "%", True, (0, 0, 0), None, self.main.window.surface, 1, 1, True)
        if active:
            self.blockSelection.render()
