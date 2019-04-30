from pygameImporter import pygame
from Constants import *
from Block import Block
import os


class Blocks:
    def __init__(self):
        files = os.listdir(BLOCK_PATH)
        files.sort()
        self.blocks = []
        for file in files:
            self.blocks.append(None)
        for file in files:
            self.blocks[int(list(file)[0])] = Block(file)
        self.resizeTextures((144, 144))
        self.size = (144, 144)
    
    def resizeTextures(self, size):
        self.size = size
        for block in self.blocks:
            if block.texture != None:
                block.resizedTexture = pygame.transform.scale(block.texture, size)
