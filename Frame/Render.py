from Frame.baseFunctions import *
import pygame


class Render:
    def __init__(self, window):
        output("Render: Creating render object...", "debug")
        self.window = window
    
    def getTextSizeForWidth(self, text, startSize, width, font):
        size = startSize
        textWidth = list(pygame.font.Font(font, size).size(text))[0]
        while textWidth > width:
            size -= 1
            textWidth = list(pygame.font.Font(font, size).size(text))[0]
        return size

    def text(self, file, size, text, antialias, color, background, surface, x = None, y = None, blit = True, width = None, height = None, addX = 0, addY = 0,
             alpha = 255):
        output("Render: Rendering \"" + text + "\"...", "complete")
        textSurface = pygame.font.Font(file, size).render(text, antialias, color, background)
        if x == None or y == None:
            if surface == None:
                surface = self.window.surface
            if width == None or height == None:
                x = surface.get_width() / 2 - textSurface.get_width() / 2
                y = surface.get_height() / 2 - textSurface.get_height() / 2
            else:
                x = width / 2 - textSurface.get_width() / 2
                y = height / 2 - textSurface.get_height() / 2
        if alpha != 255:
            textSurfaceAlpha = pygame.Surface((textSurface.get_width(), textSurface.get_height()))
            otherColor = []
            for i in color:
                rgb = i + 127.5
                while rgb > 255:
                    rgb -= 255
                otherColor.append(rgb)
            textSurfaceAlpha.fill(otherColor)
            textSurfaceAlpha.set_colorkey(otherColor)
            textSurfaceAlpha.blit(textSurface, (0, 0))
            textSurfaceAlpha.set_alpha(alpha)
            textSurface = textSurfaceAlpha
        if blit:
            if surface == None:
                surface = self.window.surface
            surface.blit(textSurface, (x + addX, y + addY))
        else:
            return textSurface
