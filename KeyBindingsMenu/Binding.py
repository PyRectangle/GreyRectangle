from LevelSelection.Graphic import Graphic
from Frame.gui.Button import Button
from pygameImporter import pygame
from Frame.Render import Render
from Constants import *


class Binding:
    def __init__(self, y, key, text, speed, name, dictionary, window):
        self.window = window
        self.y = y
        self.key = key
        self.name = name
        self.speed = speed
        self.renderObj = Render(window)
        self.dictionary = dictionary
        self.graphics = [Graphic((100, 100, 100), [[0, y], [1440, y], [1440, y + 50], [0, y + 50]], [-1440, 0], speed, window, (FONT, 45, text, True, (0, 0, 0), None), 0, y),
                         Graphic((100, 100, 100), [[0, y], [0, y], [0, y]], [-1440, 0], speed, window, (FONT, 50, self.getKeyName(key), True, (0, 0, 0), None), 800, y)]
        self.button = None

    def create(self):
        for graphic in self.graphics:
            if graphic.isClosed:
                graphic.toggle()
        self.button = Button(self.change, (), 1200, self.y + 5, 200, 40, "Change", (150, 150, 150), (0, 0, 0), (150, 150, 255), (0, 0, 0), FONT, True, 30, 30, 0.1,
                             True, [self.speed, 0], None, SOUNDS, self.window)
    
    def remove(self):
        for graphic in self.graphics:
            if graphic.isOpen:
                graphic.toggle()
        self.button.delete()
    
    def getKeyName(self, key):
        keyText = pygame.key.name(key)
        if type(keyText) == bytes:
            keyText = keyText.decode()
        return keyText
    
    def change(self):
        self.key = 0
        pressed = False
        while not pressed:
            self.window.guiHandler.clickAnim = None
            self.renderObj.text(FONT, 80, "Press a key!", True, (0, 0, 0), None, self.window.surface)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.key = event.key
                    pressed = True
            self.window.updateDisplay()
        self.graphics[1].text = (FONT, 50, self.getKeyName(self.key), True, (0, 0, 0), None)
        self.dictionary["Controls"][self.name] = self.key

    def update(self):
        for graphic in self.graphics:
            graphic.update()
        if self.button != None:
            self.button.update()
        self.window.guiPresser = self.dictionary["Controls"]["GuiPresser"]
        self.window.guiChanger = self.dictionary["Controls"]["GuiChanger"]
        for gui in self.window.guiHandler.allGuis:
            gui.right = self.dictionary["Controls"]["goRight"]
            gui.left = self.dictionary["Controls"]["goLeft"]

    def render(self):
        for graphic in self.graphics:
            graphic.render()
        if self.button != None:
            self.button.render()
