from pygameImporter import pygame
from Constants import *
from Block import Block
import os


class Blocks:
    def __init__(self, main):
        files = os.listdir(BLOCK_PATH)
        files.sort()
        self.blocks = []
        movieNum = 0
        for file in os.listdir(IMAGE_PATH):
            if file.endswith("mkv"):
                movieNum += 1
        for file in files:
            self.blocks.append(None)
        for file in files:
            self.blocks[int(list(file)[0])] = Block(file, main, movieNum)
        self.resizeTextures((BLOCK_SIZE, BLOCK_SIZE))
        self.size = (BLOCK_SIZE, BLOCK_SIZE)
    
    def resizeTextures(self, size):
        self.size = size
        for block in self.blocks:
            if block.texture != None:
                if block.animation:
                    block.currentSize = size
                else:
                    block.resizedTexture = pygame.transform.scale(block.texture, size)
