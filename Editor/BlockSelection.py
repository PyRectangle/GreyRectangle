from LevelSelection.Graphic import Graphic
from pygameImporter import *
from Constants import *


class BlockSelection:
    def __init__(self, main, editor):
        self.main = main
        self.editor = editor
        self.on = False
        self.timer = 0
        self.goAway = False
        self.block = 0
        self.data = []
        self.blockName = self.main.blocks.blocks[self.block].name
        self.textArgs = (FONT, 80, self.blockName, True, (0, 0, 0), None)
        self.graphics = [Graphic((120, 120, 120), [[110, 1080], [210, 900], [1230, 900], [1330, 1080]], [0, 300], 1, main.window),
                         Graphic((150, 50, 200), [[110, 1080], [10, 1080], [180, 800], [1260, 800], [1430, 1080], [1330, 1080], [1230, 900], [210, 900]], [0, 300], 1,
                                 main.window, self.textArgs, 250, 810)]
    
    def enable(self, mouse = False, scroll = 0):
        if not self.on:
            self.toggle()
        if mouse:
            self.goAway = True
            self.timer = 0
        if scroll != 0:
            self.block += scroll
            if self.block < 0:
                self.block = 0
            if self.block > len(self.main.blocks.blocks) - 1:
                self.block = len(self.main.blocks.blocks) - 1
        self.on = True
    
    def checkBlockBoundary(self, value):
        changed = False
        if value < 0:
            value = 0
            changed = True
        if value > len(self.main.blocks.blocks) - 1:
            value = len(self.main.blocks.blocks) - 1
            changed = True
        return changed
    
    def disable(self):
        if self.on:
            self.toggle()
        self.on = False
    
    def toggle(self):
        self.on = not self.on
        for graphic in self.graphics:
            graphic.toggle()
    
    def update(self):
        if self.main.window.disableGuiComeInAnimations:
            self.blockName = self.main.blocks.blocks[self.block].name
        else:
            self.blockNameChange = self.main.blocks.blocks[self.block].name
            if self.blockNameChange != self.blockName:
                self.graphics[1].textAlpha -= self.main.window.dt
                if self.graphics[1].textAlpha <= 0:
                    self.graphics[1].textAlpha = 0
                    self.blockName = self.blockNameChange
            else:
                self.graphics[1].textAlpha += self.main.window.dt
                if self.graphics[1].textAlpha > 255:
                    self.graphics[1].textAlpha = 255
        self.textArgs = (FONT, 80, self.blockName, True, (0, 0, 0), None)
        self.graphics[1].text = self.textArgs
        if self.goAway:
            self.timer += self.main.window.dt / 1000
            if self.timer >= 1:
                self.timer = 0
                self.goAway = False
                self.disable()
        for graphic in self.graphics:
            graphic.update()
    
    def render(self):
        for graphic in self.graphics:
            graphic.render()
        if self.graphics[1].isChanging or self.graphics[1].isOpen:
            for block in range(5):
                blockID = self.block + block - 2
                if not self.checkBlockBoundary(blockID):
                    bigger = False
                    if blockID == self.block:
                        bigger = True
                    self.main.camera.level.render.block([blockID, self.data], 648 + (block - 2) * 204, self.graphics[0].point[1] + 916, bigger, True)
