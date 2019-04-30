from Frame.gui.Button import Button
from pygameImporter import pygame
from Frame.Render import Render
from Constants import *
from Menu import Menu


class DeleteLevel(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.level = None
        self.alpha = 0
        self.up = True
        self.do = False
        self.window = menuHandler.window
        self.renderObj = Render(menuHandler.window)
        self.addGui(Button, (menuHandler.edit, (), 40, 900, 400, 100, "Cancel", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30, 0.1, True,
                             [0, -1], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.deleteLevel, (), 1000, 900, 400, 100, "Delete", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30, 0.1,
                             True, [0, -1], None, SOUNDS, menuHandler.window))

    def update(self):
        super().update()
        if self.do:
            if self.up:
                self.alpha += self.window.dt
                if self.alpha > 255:
                    self.alpha = 255
                    self.do = False
            else:
                self.alpha -= self.window.dt
                if self.alpha < 1:
                    self.do = False
                    self.alpha = 1

    def render(self):
        super().render()
        text = "Do you really want to delete \"" + self.level.name + "\" ?"
        self.renderObj.text(FONT, self.renderObj.getTextSizeForWidth(text, 100, SURFACE_SIZE[0], FONT), text, True, (0, 0, 0), None, self.window.surface, addY = -55,
                            alpha = self.alpha)
        self.renderObj.text(FONT, 100, "It will be lost forever !", True, (0, 0, 0), None, self.window.surface, addY = 55, alpha = self.alpha)
        self.renderObj.text(FONT, 100, "Delete", True, (0, 0, 0), None, self.window.surface, addY = -400, alpha = self.alpha)
