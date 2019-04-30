from pygameImporter import pygame
from Frame.baseFunctions import *


class ClickAnim:
    def __init__(self, button):
        output("ClickAnim: Creating a click animation...", "debug")
        self.button = button
        self.pos = -1
        self.finished = False
        output("ClickAnim: Resizing the button for a bit...", "complete")
        for i in range(int(self.button.pressDifference / 2 + 0.5)):
            self.button.setSize(False)
        self.rendered = False
        self.update()

    def update(self):
        self.rendered = False
        output("ClickAnim: Getting a bit bigger...", "complete")
        self.pos += self.button.window.dt / 5
        output("ClickAnim: Getting the coords used to render the click animation...", "complete")
        self.coords = [self.button.x - self.pos, self.button.y - self.pos, self.button.width + self.button.x + self.pos, self.button.height + self.button.y +
                       self.pos]
        if self.pos > self.button.pressDifference:
            output("Executing the \"onClick\" function...")
            self.finished = True
            if type(self.button.functionArgs) == tuple:
                self.button.function(*self.button.functionArgs)
            else:
                self.button.function(self.button.functionArgs)
    
    def render(self):
        self.rendered = True
        output("ClickAnim: Rendering the click animation...", "complete")
        pygame.draw.polygon(self.button.window.surface, self.button.frameColor, [[self.coords[0], self.coords[1]], [self.coords[0], self.coords[3]], 
                                                                                 [self.coords[2], self.coords[3]], [self.coords[2], self.coords[1]]], 1)
