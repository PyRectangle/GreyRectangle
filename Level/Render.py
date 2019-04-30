from pygameImporter import pygame
from Constants import *


class Render:
    def __init__(self, level, main):
        self.level = level
        self.window = main.window
        self.main = main
        self.red = pygame.Surface((1, 1))
        self.red.fill((255, 0, 0))
        self.lastSize = 144
    
    def blocks(self, x, y, size = BLOCK_SIZE, distance = None):
        size = int(size)
        if size != self.lastSize:
            self.main.blocks.resizeTextures((size, size))
            self.lastSize = size
        if distance == None:
            distance = size
        blocksX = int(list(self.window.START_SURFACE_SIZE)[0] / distance + 3)
        blocksY = int(list(self.window.START_SURFACE_SIZE)[1] / distance + 3)
        if blocksX / 2 == int(blocksX / 2):
            x += 0.5
        if blocksY / 2 == int(blocksY / 2):
            y += 0.5
        startPosX = (x - int(x)) * -distance
        startPosY = (y - int(y)) * -distance
        sizeX = blocksX * distance
        sizeY = blocksY * distance
        blitStartPosX = -(list(self.window.START_SURFACE_SIZE)[0] - sizeX) / 2
        blitStartPosY = -(list(self.window.START_SURFACE_SIZE)[1] - sizeY) / 2
        indexStartPosX = int(x) - int(blocksX / 2)
        indexStartPosY = int(y) - int(blocksY / 2)
        for blockY in range(blocksY):
            for blockX in range(blocksX):
                blitPosX = startPosX + blockX * distance - blitStartPosX
                blitPosY = startPosY + blockY * distance - blitStartPosY
                indexX = indexStartPosX + blockX
                indexY = indexStartPosY + blockY
                regionX = indexX / 16
                regionY = indexY / 16
                try:
                    inLevel = True
                    if not regionX < 0 and not regionY < 0 and not indexX < 0 and not indexY < 0:
                        regionObj = self.level.data.regionsGrid[int(regionY)][int(regionX)]
                        if regionObj != None and regionObj.loaded:
                            try:
                                regionIndexX = int(indexX - int(regionX) * 16)
                                regionIndexY = int(indexY - int(regionY) * 16)
                                block = regionObj.region[regionIndexY][regionIndexX]
                                self.block(block, blitPosX, blitPosY, blockCoords = [indexX, indexY])
                            except IndexError:
                                pass
                        elif regionObj != None and not regionObj.loading:
                            try:
                                regionObj.start()
                            except RuntimeError:
                                pass
                        if regionObj == None:
                            inLevel = False
                    else:
                        inLevel = False
                except IndexError:
                    inLevel = False
                if not inLevel:
                    self.window.surface.blit(pygame.transform.scale(self.red, (size, size)), (blitPosX, blitPosY))

    def rotate(self, texture, attribute):
        if texture != None:
            angle = attribute * 90
            return pygame.transform.rotate(texture, angle)
        return None
    
    def mix(self, texture, color, factor, lineWidth, returnSurface = False):
        if bool(factor):
            if texture == None:
                width, height = self.main.blocks.size
            else:
                width = texture.get_width()
                height = texture.get_height()
            surface = pygame.Surface((width, height))
            surface.fill((0, 0, 0))
            surface.set_colorkey((0, 0, 0))
            pygame.draw.polygon(surface, color, [[0, 0], [width, 0], [width, height], [0, height]], lineWidth)
            if returnSurface:
                return surface
            else:
                texture.blit(surface, (0, 0))
        return texture
    
    def colorTexture(self, texture, color = (255, 0, 0), alpha = 100):
        surface = pygame.Surface((texture.get_width(), texture.get_height()))
        surface.convert()
        surface.fill(color)
        surface.set_alpha(alpha)
        rTexture = texture.copy()
        rTexture.blit(surface, (0, 0))
        return rTexture

    def block(self, block, x, y, bigger = False, useNormalTexture = False, blockCoords = [-1, -1]):
        if useNormalTexture:
            texture = self.main.blocks.blocks[block[0]].texture
        else:
            texture = self.main.blocks.blocks[block[0]].resizedTexture
        if self.main.playing and block[1] != []:
            distanceToBlock = [x + BLOCK_SIZE / 2 - self.main.player.center[0], y + BLOCK_SIZE / 2 - self.main.player.center[1]]
            for i in range(2):
                if distanceToBlock[i] < 0:
                    distanceToBlock[i] = -distanceToBlock[i]
            distanceColor = (distanceToBlock[0] + distanceToBlock[1]) / 4
            if distanceColor > 255:
                distanceColor = 255
            distanceColor = 255 - distanceColor
            if texture == None:
                playTexture = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
                playTexture.fill((255, 255, 255))
            else:
                playTexture = texture
            if block[1][2] != self.main.blocks.blocks[block[0]].death and (not block[1][1] or not self.main.blocks.blocks[block[0]].solid):
                texture = self.colorTexture(playTexture, (255, 0, 0), distanceColor)
            elif (block[1][1] != self.main.blocks.blocks[block[0]].solid and not block[1][1]) or (block[1][2] == False and block[1][2] != self.main.blocks.blocks[block[0]].death and (not block[1][1] or not self.main.blocks.blocks[block[0]].solid)):
                texture = self.colorTexture(playTexture, (255, 255, 255), distanceColor)
        if block[1] != []:
            if texture != None:
                texture = self.rotate(texture, int(block[1][0]))
            if self.main.editing and self.main.editor.active:
                texture = self.mix(texture, (255, 0, 0), int(block[1][2]), 20, texture == None)
                texture = self.mix(texture, (255, 255, 255), 1 - int(block[1][1]), 10, texture == None)
        if self.main.editing and self.main.editor.active:
            if texture == None:
                if useNormalTexture:
                    texture = pygame.Surface((144, 144))
                else:
                    texture = pygame.Surface(self.main.blocks.size)
                texture.fill((255, 255, 255))
            texture = self.mix(self.mix(texture, (255, 0, 0), self.main.blocks.blocks[block[0]].death, 20, texture == None), (255, 255, 255),
                               not self.main.blocks.blocks[block[0]].solid, 10, texture == None)
            if self.main.editor.selection != None and self.main.editor.selection[0][0] <= blockCoords[0] and self.main.editor.selection[0][1] <= blockCoords[1] \
               and self.main.editor.selection[1][0] >= blockCoords[0] and self.main.editor.selection[1][1] >= blockCoords[1]:
                texture = self.colorTexture(texture, (100, 100, 255))
        if texture != None:
            if not bigger:
                self.window.surface.blit(texture, (x, y))
            else:
                self.window.surface.blit(pygame.transform.scale(texture, (164, 164)), (x - 10, y - 10))
    
    def grid(self, x, y, distance = BLOCK_SIZE, size = None):
        distance = int(distance)
        surface = pygame.Surface(self.window.size)
        surface.fill((255, 255, 255))
        surface.set_colorkey((255, 255, 255))
        blocksX = int(list(self.window.START_SURFACE_SIZE)[0] / distance + 3)
        blocksY = int(list(self.window.START_SURFACE_SIZE)[1] / distance + 3)
        if blocksX / 2 == int(blocksX / 2):
            x += 0.5
        if blocksY / 2 == int(blocksY / 2):
            y += 0.5
        startPosX = (x - int(x)) * -distance
        startPosY = (y - int(y)) * -distance
        sizeX = blocksX * distance
        sizeY = blocksY * distance
        if size == None:
            size = distance
        blitStartPosX = -(list(self.window.START_SURFACE_SIZE)[0] - sizeX) / 2
        blitStartPosY = -(list(self.window.START_SURFACE_SIZE)[1] - sizeY) / 2
        for blockY in range(blocksY):
            for blockX in range(blocksX):
                blitPosX = startPosX + blockX * distance - blitStartPosX
                blitPosY = startPosY + blockY * distance - blitStartPosY
                screenBlitPosX, screenBlitPosY = self.window.getScreenCoords(blitPosX, blitPosY)
                pygame.draw.lines(surface, (0, 0, 0), False, [[screenBlitPosX + size, screenBlitPosY], [screenBlitPosX, screenBlitPosY],
                                                              [screenBlitPosX, screenBlitPosY + size]])
        for gui in self.window.guiHandler.allGuis:
            x1, y1 = self.window.getScreenCoords(gui.x, gui.y)
            x2, y2 = self.window.getScreenCoords(gui.x + gui.width, gui.y + gui.height)
            pygame.draw.polygon(surface, (255, 255, 255), [[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
        for graphics in self.main.levelSelection.graphics, self.main.editor.blockSelection.graphics:
            for graphic in graphics:
                if graphic.isOpen or graphic.isChanging:
                    vertices = []
                    for vertex in graphic.renderVertices:
                        coords = self.window.getScreenCoords(vertex[0], vertex[1])
                        vertices.append([coords[0], coords[1]])
                    pygame.draw.polygon(surface, (255, 255, 255), vertices)
        if self.main.editing and self.main.editor.playerCoords != []:
            screenCoords = []
            for coord in self.main.editor.playerCoords:
                screenCoords.append(list(self.window.getScreenCoords(*coord)))
            pygame.draw.polygon(surface, (255, 255, 255), screenCoords)
        if self.window.screenSurfaces == []:
            self.window.screenSurfaces.append(surface)
        else:
            self.window.screenSurfaces[0] = surface
