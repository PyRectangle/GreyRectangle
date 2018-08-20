from Frame.baseFunctions import *
import pygame


class Render:
    def __init__(self, window):
        output("Render: Creating render object...", "debug")
        self.window = window

    def text(self, file, size, text, antialias, color, background, surface, x = None, y = None, blit = True, width = None, height = None, addX = 0, addY = 0):
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
        if blit:
            if surface == None:
                surface = self.window.surface
            surface.blit(textSurface, (x + addX, y + addY))
        else:
            return textSurface
