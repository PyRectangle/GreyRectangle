from Constants import *
import pygame


class Render:
    def __init__(self, level, main):
        self.level = level
        self.window = main.window
        self.main = main
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
                    if not regionX < 0 and not regionY < 0 and not indexX < 0 and not indexY < 0:
                        regionObj = self.level.data.regionsGrid[int(regionY)][int(regionX)]
                        if regionObj != None and regionObj.loaded:
                            try:
                                regionIndexX = int(indexX - int(regionX) * 16)
                                regionIndexY = int(indexY - int(regionY) * 16)
                                block = regionObj.region[regionIndexY][regionIndexX]
                                self.block(block, blitPosX, blitPosY)
                            except IndexError:
                                pass
                        elif regionObj != None and not regionObj.loading:
                            try:
                                regionObj.start()
                            except RuntimeError:
                                pass
                except IndexError:
                    pass

    def block(self, block, x, y):
        texture = self.main.blocks.blocks[block[0]].resizedTexture
        if texture != None:
            self.window.surface.blit(texture, (x, y))
    
    def grid(self, x, y, distance = BLOCK_SIZE):
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
        blitStartPosX = -(list(self.window.START_SURFACE_SIZE)[0] - sizeX) / 2
        blitStartPosY = -(list(self.window.START_SURFACE_SIZE)[1] - sizeY) / 2
        for blockY in range(blocksY):
            for blockX in range(blocksX):
                blitPosX = startPosX + blockX * distance - blitStartPosX
                blitPosY = startPosY + blockY * distance - blitStartPosY
                screenBlitPosX, screenBlitPosY = self.window.getScreenCoords(blitPosX, blitPosY)
                pygame.draw.lines(surface, (0, 0, 0), False, [[screenBlitPosX + distance, screenBlitPosY], [screenBlitPosX, screenBlitPosY],
                                                              [screenBlitPosX, screenBlitPosY + distance]])
        for gui in self.window.guiHandler.allGuis:
            x1, y1 = self.window.getScreenCoords(gui.x, gui.y)
            x2, y2 = self.window.getScreenCoords(gui.x + gui.width, gui.y + gui.height)
            pygame.draw.polygon(surface, (255, 255, 255), [[x1, y1], [x2, y1], [x2, y2], [x1, y2]])
        for graphic in self.main.levelSelection.graphics:
            if graphic.isOpen or graphic.isChanging:
                vertices = []
                for vertex in graphic.renderVertices:
                    coords = self.window.getScreenCoords(vertex[0], vertex[1])
                    vertices.append([coords[0], coords[1]])
                pygame.draw.polygon(surface, (255, 255, 255), vertices)
        if self.window.screenSurfaces == []:
            self.window.screenSurfaces.append(surface)
        else:
            self.window.screenSurfaces[0] = surface
