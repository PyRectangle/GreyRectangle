from Constants import *
import pygame
import json


class Block:
    def __init__(self, jsonFile):
        file = open(BLOCK_PATH + "/" + jsonFile)
        self.json = json.load(file)
        file.close()
        self.name = self.json["Name"]
        self.texture = self.getValue("Texture")
        self.solid = self.json["Solid"]
        self.death = self.json["Death"]
        self.animation = self.getValue("Animation")
        if self.texture == "":
            self.texture = None
        if self.texture != None:
            self.texture = pygame.image.load(IMAGE_PATH + "/" + self.texture).convert()
        self.resizedTexture = None
    
    def getValue(self, value):
        try:
            return self.json[value]
        except KeyError:
            return None
