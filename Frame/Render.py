import pygame


class Render:
    def __init__(self, window):
        self.window = window

    def text(self, file, size, text, antialias, color, background, surface, x = None, y = None, blit = True):
        textSurface = pygame.font.Font(file, size).render(text, antialias, color, background)
        if x == None or y == None:
            if surface == None:
                surface = self.window.surface
            x = surface.get_width() / 2 - textSurface.get_width() / 2
            y = surface.get_height() / 2 - textSurface.get_height() / 2
        if blit:
            if surface == None:
                surface = self.window.surface
            surface.blit(textSurface, (x, y))
        else:
            return textSurface
