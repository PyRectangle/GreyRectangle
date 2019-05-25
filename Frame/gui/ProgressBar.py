from pygameImporter import pygame
from Frame.baseFunctions import *
from Frame.gui.Gui import Gui


class ProgressBar(Gui):
    def __init__(self, fillPercentage, fillColor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        output("Progress Bar: Creating " + self.text + " progress bar...", "debug")
        self.progress = fillPercentage
        self.fillColor = fillColor
        self.touchable = False
    
    def setProgress(self, progress):
        output("Progress Bar: Setting progress to " + str(progress) + "%...", "debug")
        if progress > 100:
            progress = 100
        self.progress = progress
        
    def render(self):
        super().render(False)
        output("Progress Bar: Getting points for drawing...", "complete")
        points = [[self.coords[0] + 1, self.coords[1] + 1], [self.coords[0] + self.coords[2] * self.progress / 100 - 1, self.coords[1] + 1],
                  [self.coords[0] + self.coords[2] * self.progress / 100 - 1, self.coords[1] + self.coords[3] - 1],
                  [self.coords[0] + 1, self.coords[1] + self.coords[3] - 1]]
        output("Progress Bar: Drawing...", "complete")
        pygame.draw.polygon(self.window.surface, self.fillColor, points)
        output("Progress Bar: Rendering text...", "complete")
        try:
            if not self.writable and self.text == "":
                self.renderObj.text(self.fontFile, int(self.textSize + self.height - self.startCoords[3]), self.enterText, self.antialias, self.textColor, None,
                                    self.window.surface, width = self.width, height = self.height, addX = self.x, addY = self.y)
        except AttributeError:
            self.renderObj.text(self.fontFile, int(self.textSize + self.height - self.startCoords[3]), self.text, self.antialias, self.textColor, None,
                                self.window.surface, width = self.width, height = self.height, addX = self.x, addY = self.y)
