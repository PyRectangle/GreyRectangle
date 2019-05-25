from pygameImporter import pygame
from Constants import *


class Camera:
    def __init__(self, main):
        self.main = main
        self.x = 0
        self.y = 0
        self.window = main.window
        self.player = main.player
        self.editor = main.editor
        self.speed = 1
        self.speedUp = 1
        self.speedDown = 1
        self.level = None
        self.stopUp = 3.25
        self.stopLeft = 4.5
        self.stopDown = 1440
        self.stopRight = 1080
        self.stopped = False
        self.stopX = False
        self.stopY = False
        self.size = BLOCK_SIZE
    
    def setStops(self, level, anyways = False):
        if self.main.playing or anyways:
            self.stopDown = len(level.data.regionsGrid) * 16 - 4.25
            self.stopRight = len(level.data.regionsGrid[0]) * 16 - 5.5
    
    def setCoords(self, level):
        if self.main.editing:
            self.editor.x = level.data.spawnX
            self.editor.y = level.data.spawnY
            self.editor.edit = None
            self.editor.selectedBlock = 0
            self.editor.steps = []
        elif self.main.playing:
            self.player.x = level.data.spawnX
            self.player.y = level.data.spawnY

    def setProps(self, level):
        self.level = level
        self.x = level.data.spawnX
        self.y = level.data.spawnY
        self.setCoords(level)
        self.setStops(level)
        if not self.main.menuHandler.editor:
            self.player.alpha = 0
            self.player.alphaUp = True
            self.player.alphaMove = True
            self.player.getPixelCoords()
    
    def updateCoord(self, player, this, speed):
        if player > this:
            this += self.window.dt * speed
            if this > player:
                this = player
        if player < this:
            this -= self.window.dt * speed
            if this < player:
                this = player
        return this
    
    def getDifference(self, one, two):
        difference = one - two
        if difference < 0:
            difference = -difference
        return difference
    
    def stop(self, stop, coord, bigger):
        if bigger:
            if coord > stop:
                coord = stop
                self.stopped = True
        else:
            if coord < stop:
                coord = stop
                self.stopped = True
        return coord

    def update(self, onlyStops = False):
        self.stopped = False
        if onlyStops:
            self.x = self.stop(self.stopRight, self.stop(self.stopLeft, self.x, False), True)
            self.stopX = self.stopped
            self.stopped = False
            self.y = self.stop(self.stopDown, self.stop(self.stopUp, self.y, False), True)
            self.stopY = self.stopped
        else:
            if self.main.editing:
                self.x = self.editor.x
                self.y = self.editor.y
            elif self.main.playing:
                self.speedX = self.getDifference(self.x, self.player.x) / CAMERA_FREE_MOVE_PIXELS
                self.speedY = self.getDifference(self.y, self.player.y) / CAMERA_FREE_MOVE_PIXELS
                if self.speedX * CAMERA_FREE_MOVE_PIXELS <= BLOCK_PIX:
                    self.speedX = self.getDifference(self.x, self.player.x)
                if self.speedY * CAMERA_FREE_MOVE_PIXELS <= BLOCK_PIX:
                    self.speedY = self.getDifference(self.y, self.player.y)
                self.x = self.stop(self.stopRight, self.stop(self.stopLeft, self.updateCoord(self.player.x, self.x, self.speedX), False), True)
                self.stopX = self.stopped
                self.stopped = False
                self.y = self.stop(self.stopDown, self.stop(self.stopUp, self.updateCoord(self.player.y, self.y, self.speedY), False), True)
                self.stopY = self.stopped
        for block in self.main.blocks.blocks:
            if block.animation:
                block.movie.update(self.main.window.dt)
                block.tmpSurface = None
            if block.overlays != None:
                for overlay in block.overlayResources:
                    if type(overlay) != pygame.Surface:
                        overlay.update(self.main.window.dt)
    
    def render(self):
        if self.level != None:
            self.level.render.blocks(self.x, self.y, self.size)
            if self.main.editing:
                self.level.render.grid(self.x, self.y, self.size)
