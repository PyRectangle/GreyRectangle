from pygameImporter import pygame
from Constants import *
import os


class Lifes:
    def __init__(self):
        self.lifes = 1
        self.bar = 0
        self.showLifes = 1
        self.textures = [self.loadImage("emptyLife.png"), self.loadImage("fullLife.png")]
    
    def loadImage(self, image):
        image = pygame.image.load(os.path.join(IMAGE_PATH, image)).convert()
        image.set_colorkey((255, 255, 255))
        return image

    def update(self, lifes):
        self.lifes = lifes
        self.bar = int((self.lifes - 0.1) / LIFE_SHOW_LENGTH)
        self.showLifes = self.lifes - self.bar * LIFE_SHOW_LENGTH
    
    def render(self, render, alpha):
        size = render.getTextSizeForWidth("Lifes: " + str(self.lifes), 64, LIFE_TEXT_WIDTH, FONT)
        render.text(FONT, size, "Lifes: " + str(self.lifes), True, (0, 0, 0), None, render.window.surface, x = 0, y = 0, blit = True, alpha = alpha)
        for texture in self.textures:
            texture.set_alpha(alpha)
        for i in range(LIFE_SHOW_LENGTH):
            active = i < self.showLifes
            render.window.surface.blit(self.textures[int(active)], (LIFE_TEXT_WIDTH + i * 64, 0))
        size = render.getTextSizeForWidth("Bar: " + str(self.bar), 64, SURFACE_SIZE[0] - LIFE_TEXT_WIDTH + 640, FONT)
        render.text(FONT, size, "Bar: " + str(self.bar), True, (0, 0, 0), None, render.window.surface, x = LIFE_TEXT_WIDTH + 640, y = 0, blit = True, alpha = alpha)
