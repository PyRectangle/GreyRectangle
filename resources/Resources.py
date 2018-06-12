import pygame


class Resources():
    def __init__(self):
        self.IMAGE_PATH = "resources/images/"
    
    def load_textures(self, textures):
        self.images = []
        for texture in textures:
            self.images.append(pygame.image.load(self.IMAGE_PATH + texture))
