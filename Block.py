from Frame.baseFunctions import setColorkey
from pygameImporter import pygame
from Constants import *
from Movie import Movie
import json


class Block:
    def __init__(self, jsonFile, main, movieNum):
        file = open(BLOCK_PATH + "/" + jsonFile)
        self.json = json.load(file)
        file.close()
        self.ID = self.getID(jsonFile)
        self.name = self.json["Name"]
        self.realtexture = self.getValue("Texture")
        self.fps = self.getValue("FPS")
        self.solid = self.json["Solid"]
        self.death = self.json["Death"]
        self.overlays = self.getValue("Overlays")
        self.colorkey = self.getValue("Colorkey")
        self.startOverlay = self.getValue("StartOverlay")
        self.unusedColor = self.getValue("UnusedColor")
        self.lastTouched = None
        self.lastBlockObject = None
        if self.overlays != None:
            self.overlayFps = self.getValue("OverlayFPS")
            self.overlayColorkey = self.getValue("OverlayColorkey")
            self.overlayResources = []
            count = 0
            for overlay in self.overlays:
                if overlay.endswith(".mkv"):
                    fps = self.overlayFps[count]
                    if fps != None:
                        self.overlayResources.append(Movie(IMAGE_PATH + "/" + overlay, fps, main, movieNum, self.overlayColorkey))
                    else:
                        self.overlayResources.append(None)
                else:
                    self.overlayResources.append(pygame.image.load(IMAGE_PATH + "/" + overlay).convert())
                    if self.overlayColorkey != None:
                        self.overlayResources[-1] = setColorkey(self.overlayColorkey, self.overlayResources[-1])
                count += 1
        self.overlay = {}
        self.events = self.getValue("Events")
        self.animation = False
        if self.realtexture.endswith("mkv"):
            self.animation = True
            self.currentSize = (BLOCK_SIZE, BLOCK_SIZE)
            self.movie = Movie(IMAGE_PATH + "/" + self.realtexture, self.fps, main, movieNum, self.colorkey, self.getValue("TextureFrame"))
            self.movie.play = True
        if self.realtexture == "":
            self.realtexture = None
        if self.realtexture != None and not self.animation:
            self.realtexture = pygame.image.load(IMAGE_PATH + "/" + self.texture).convert()
            if self.colorkey != None:
                if self.unusedColor == None:
                    self.realtexture = setColorkey(self.colorkey, self.realtexture)
                else:
                    self.realtexture = setColorkey(self.colorkey, self.realtexture, self.unusedColor)
        self.resizeTexture = None
    
    def getID(self, string):
        ID = ""
        for i in string:
            if i != "_":
                ID += i
            else:
                break
        return int(ID)
    
    def setTexture(self, texture):
        if self.animation:
            self.movie.surface = texture
        else:
            self.realtexture = texture

    def getTexture(self):
        if self.animation:
            return self.movie.surface
        else:
            return self.realtexture
    
    def setResizedTexture(self, texture):
        self.resizeTexture = texture
    
    def getResizedTexture(self):
        if self.animation:
            self.resizeTexture = pygame.transform.scale(self.texture, self.currentSize)
        if self.resizeTexture != None:
            self.resizeTexture.set_colorkey(self.texture.get_colorkey())
        return self.resizeTexture

    def getValue(self, value):
        try:
            return self.json[value]
        except KeyError:
            return None
    
    texture = property(getTexture, setTexture)
    resizedTexture = property(getResizedTexture, setResizedTexture)
