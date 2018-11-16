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
        self.size = BLOCK_SIZE
    
    def setStops(self, level, anyways = False):
        if self.main.playing or anyways:
            self.stopDown = len(level.data.regionsGrid) * 16 - 4.25
            self.stopRight = len(level.data.regionsGrid[0]) * 16 - 5.5
    
    def setCoords(self, level):
        if self.main.editing:
            self.editor.x = level.data.spawnX
            self.editor.y = level.data.spawnY
        elif self.main.playing:
            self.player.x = level.data.spawnX
            self.player.y = level.data.spawnY

    def setProps(self, level):
        self.level = level
        self.x = level.data.spawnX
        self.y = level.data.spawnY
        self.setCoords(level)
        self.setStops(level)
    
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
        else:
            if coord < stop:
                coord = stop
        return coord

    def update(self):
        if self.main.editing:
            self.speedX = self.getDifference(self.x, self.editor.x) / CAMERA_FREE_MOVE_PIXELS_EDITOR
            self.speedY = self.getDifference(self.y, self.editor.y) / CAMERA_FREE_MOVE_PIXELS_EDITOR
            self.x = self.updateCoord(self.editor.x, self.x, self.speedX)
            self.y = self.updateCoord(self.editor.y, self.y, self.speedY)
        elif self.main.playing:
            self.speedX = self.getDifference(self.x, self.player.x) / CAMERA_FREE_MOVE_PIXELS
            self.speedY = self.getDifference(self.y, self.player.y) / CAMERA_FREE_MOVE_PIXELS
            self.x = self.stop(self.stopRight, self.stop(self.stopLeft, self.updateCoord(self.player.x, self.x, self.speedX), False), True)
            self.y = self.stop(self.stopDown, self.stop(self.stopUp, self.updateCoord(self.player.y, self.y, self.speedY), False), True)
    
    def render(self):
        if self.level != None:
            self.level.render.blocks(self.x, self.y, self.size)
            if self.main.editing:
                self.level.render.grid(self.x, self.y, self.size)
