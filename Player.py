from Frame.Render import Render
from Constants import *
from Lifes import Lifes
import pygame
import math


class Player:
    def __init__(self, main):
        self.main = main
        self.lastSpeed = 0
        self.x = 0
        self.y = 0
        self.active = False
        self.activeCount = 0
        self.quitMenu = False
        self.fallSpeed = 0
        self.lastFallSpeed = 0
        self.first = True
        self.jumping = False
        self.jumpCount = 0
        self.jumpTime = 0
        self.jumpHeight = 0
        self.alpha = 0
        self.alphaUp = False
        self.alphaMove = False
        self.lifes = 1
        self.lifesObj = Lifes()
        self.go = False
        self.renderObj = Render(self.main.window)
        self.onGround = False
        self.center = [0, 0]
    
    def getBlockAt(self, x, y, load = False):
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
                if region == None:
                    return None
                if region.loaded:
                    return region.region[index[1]][index[0]]
                elif load:
                    region.load()
                    return region.region[index[1]][index[0]]
            except IndexError:
                return None
        return None
    
    def collide(self, direct):
        changeX = 0
        changeY = 0
        if list(direct)[0] == "x":
            changeX = float(list(direct)[1] + str(PLAYER_SPEED))
        if list(direct)[0] == "y":
            changeY = float(list(direct)[1] + str(PLAYER_SPEED))
        x = self.x + changeX
        y = self.y + changeY
        points = [[x - PLAYER_BLOCK_SIZE[0], y - PLAYER_BLOCK_SIZE[1]],
                  [x + PLAYER_BLOCK_SIZE[0], y - PLAYER_BLOCK_SIZE[1]],
                  [x + PLAYER_BLOCK_SIZE[0], y + PLAYER_BLOCK_SIZE[1]],
                  [x - PLAYER_BLOCK_SIZE[0], y + PLAYER_BLOCK_SIZE[1]],
                  [x + PLAYER_BLOCK_SIZE[0], y],
                  [x - PLAYER_BLOCK_SIZE[0], y]]
        collide = False
        for point in points:
            block = self.getBlockAt(int(point[0] + 0.5), int(point[1] + 0.5))
            if block != None:
                if block[1] != []:
                    if bool(int(block[1][1])):
                        collide = True
                elif self.main.blocks.blocks[block[0]].solid:
                    collide = True
        if changeY == 0:
            if changeX < 0:
                if self.xPx <= PLAYER_SIZE[0]:
                    collide = True
            else:
                if self.xPx >= SURFACE_SIZE[0] - PLAYER_SIZE[0]:
                    collide = True
        elif changeX == 0:
            if changeY < 0:
                if self.yPx <= PLAYER_SIZE[1]:
                    collide = True
            else:
                if self.yPx >= SURFACE_SIZE[1] - PLAYER_SIZE[1]:
                    collide = True
        return collide
    
    def getTouch(self):
        points = [[self.x - PLAYER_BLOCK_SIZE[0], self.y - PLAYER_BLOCK_SIZE[1]],
                  [self.x + PLAYER_BLOCK_SIZE[0], self.y - PLAYER_BLOCK_SIZE[1]],
                  [self.x + PLAYER_BLOCK_SIZE[0], self.y + PLAYER_BLOCK_SIZE[1]],
                  [self.x - PLAYER_BLOCK_SIZE[0], self.y + PLAYER_BLOCK_SIZE[1]],
                  [self.x + PLAYER_BLOCK_SIZE[0], self.y],
                  [self.x - PLAYER_BLOCK_SIZE[0], self.y]]
        blocks = []
        for point in points:
            blocks.append(self.getBlockAt(int(point[0] + 0.5), int(point[1] + 0.5)))
        return blocks

    def fall(self):
        self.fallSpeed *= self.main.camera.level.data.fallSpeedMultiplier
        speed = self.fallSpeed
        speed += self.lastFallSpeed
        self.lastFallSpeed = speed - int(speed)
        for i in range(int(speed)):
            if not self.collide("y+"):
                self.y += PLAYER_SPEED
            else:
                self.onGround = True
                self.fallSpeed = self.main.camera.level.data.fallSpeed
                return
    
    def jump(self):
        self.jumpCount = 0
        self.jumped = 0
        self.jumping = True
        
    def jumpUpdate(self):
        self.jumpCount += (self.main.window.dt / 1000) / self.jumpTime
        end = False
        if self.jumpCount >= 1:
            self.jumpCount = 1
            end = True
        goTo = self.jumpHeight - math.pow(2, -self.jumpCount) * self.jumpHeight
        jumpInTick = goTo * 2 - self.jumped
        self.jumped += jumpInTick
        if end or self.jumpGoTick(jumpInTick):
            self.jumping = False
    
    def jumpGoTick(self, distance):
        end = False
        loop = distance / PLAYER_SPEED
        over = loop - int(loop)
        loop = int(loop)
        for i in range(loop):
            if not self.collide("y-"):
                self.y -= PLAYER_SPEED
            else:
                end = True
                break
        if not self.collide("y-"):
            self.y -= PLAYER_SPEED * over
        else:
            end = True
        return end
        
    def update(self, go = True):
        self.activeCount += self.main.window.dt / 1000
        if self.activeCount >= 2:
            self.active = True
        self.go = go
        if go and not self.alphaMove:
            self.getPixelCoords()
        if not self.quitMenu:
            if self.first and self.main.camera.level != None:
                self.fallSpeed = self.main.camera.level.data.fallSpeed
                self.jumpTime = self.main.camera.level.data.jumpTime
                self.jumpHeight = self.main.camera.level.data.jumpHeight
                self.lifes = self.main.camera.level.data.lifes
                self.lifesObj.update(self.lifes)
                self.first = False
            if self.active:
                self.onGround = False
                if go and not self.alphaMove:
                    self.getPixelCoords()
                    speed = self.main.window.dt * PLAYER_LOOP_SPEED * self.main.camera.level.data.walkSpeed + self.lastSpeed
                    self.lastSpeed = speed - int(speed)
                    speed = int(speed)
                    for i in range(speed):
                        if self.main.window.keys[self.main.config.config["Controls"]["goRight"]]:
                            if not self.collide("x+"):
                                self.x += PLAYER_SPEED
                        if self.main.window.keys[self.main.config.config["Controls"]["goLeft"]]:
                            if not self.collide("x-"):
                                self.x -= PLAYER_SPEED
                        if self.main.window.keys[self.main.config.config["Controls"]["goUp"]] or self.main.window.keys[self.main.config.config["Controls"]["Jump"]]:
                            if self.onGround:
                                self.jump()
                        if not self.jumping:
                            self.fall()
                    self.getPixelCoords()
                if self.jumping:
                    self.jumpUpdate()
            if self.alphaMove:
                if self.alphaUp:
                    self.alpha += self.main.window.dt / 10
                    if self.alpha > 255:
                        self.alpha = 255
                        self.alphaMove = False
                    self.getPixelCoords()
                else:
                    self.alpha -= self.main.window.dt / 10
                    if self.alpha < 0:
                        self.alpha = 0
                        self.alphaMove = False
            if go and self.active:
                for blockData in self.getTouch():
                    if blockData != None:
                        block = self.main.blocks.blocks[blockData[0]]
                        if block.death or (blockData[1] != [] and bool(int(blockData[1][2]))):
                            self.die()
                            break
                        if blockData[0] == 4: # finished level
                            self.main.menuHandler.goBack()
            if self.main.window.keys[self.main.config.config["Controls"]["Escape"]] and go:
                self.quitMenu = True
                self.main.menuHandler.show(self.main.menuHandler.playQuit)
    
    def getPixelCoords(self):
        self.main.camera.update(True)
        self.xPx = SURFACE_SIZE[0] / 2 + (self.x - self.main.camera.x) * BLOCK_SIZE
        self.yPx = SURFACE_SIZE[1] / 2 + (self.y - self.main.camera.y) * BLOCK_SIZE
        if not self.main.camera.stopX:
            self.xPx -= 1
        if not self.main.camera.stopY:
            self.yPx -= 1
        self.coords = [[self.xPx - PLAYER_SIZE[0], self.yPx - PLAYER_SIZE[1]], [self.xPx + PLAYER_SIZE[0], self.yPx - PLAYER_SIZE[1]],
                       [self.xPx + PLAYER_SIZE[0], self.yPx + PLAYER_SIZE[1]], [self.xPx - PLAYER_SIZE[0], self.yPx + PLAYER_SIZE[1]]]
        self.center = [0, 0]
        for coord in self.coords:
            for i in range(2):
                self.center[i] += coord[i]
        for i in range(2):
            self.center[i] /= 4
        
    def die(self):
        self.main.camera.setCoords(self.main.camera.level)
        self.jumping = False
        self.lifes -= 1
        self.lifesObj.update(self.lifes)
        if self.lifes <= 0: # game over
            self.main.menuHandler.goBack()
    
    def render(self):
        if self.alpha == 255:
            pygame.draw.polygon(self.main.window.surface, (150, 150, 150), self.coords)
        else:
            if self.alpha != 0:
                surface = pygame.Surface((PLAYER_SIZE[0] * 2 + 1, PLAYER_SIZE[1] * 2 + 1))
                surface.fill((150, 150, 150))
                surface.set_alpha(self.alpha)
                self.main.window.surface.blit(surface, self.coords[0])
        if self.main.playing or not self.go:
            self.lifesObj.render(self.renderObj, self.alpha)
