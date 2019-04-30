from pygameImporter import pygame
from Frame.Render import Render
from Constants import *
import sys


class DebugScreen:
    def __init__(self, window):
        self.renderObj = Render(window)
        versionString = sys.version.replace("\n", "").split(" ")
        self.pythonVersion = "Python: "
        self.gccVersion = "Compiler: "
        pyv = True
        for part in versionString:
            if part[0] == "[":
                pyv = False
            if pyv:
                self.pythonVersion += part + " "
            else:
                self.gccVersion += part + " "
        self.gccVersion = self.gccVersion.replace("[", "").replace("]", "")
        self.pythonVersionData = self.getSizeWidth(50, self.pythonVersion, 1140)
        self.gccVersionData = self.getSizeWidth(50, self.gccVersion, 1440)
        self.pygameVersion = "PyGame: " + pygame.version.ver + "  SDL: "
        count = 0
        for i in list(pygame.get_sdl_version()):
            count += 1
            self.pygameVersion += str(i)
            if count < 3:
                self.pygameVersion += "."
        self.pygameVersion += " "
        self.pygameVersionData = self.getSizeWidth(50, self.pygameVersion, 1440)
    
    def getSizeWidth(self, startSize, text, textWidth):
        width = list(pygame.font.Font(FONT, startSize).size(text))[0]
        size = startSize
        if width > 1140:
            size = self.renderObj.getTextSizeForWidth(text, startSize, textWidth, FONT)
        width = list(pygame.font.Font(FONT, size).size(text))[0]
        return [size, width]

    def render(self):
        try:
            self.renderObj.text(FONT, self.renderObj.window.getScreenScale(50, 1), "FPS:" + str(int(self.renderObj.window.fps)), True, (0, 0, 0), (100, 100, 100),
                                self.renderObj.window.screenSurfaces[0], *self.renderObj.window.getScreenCoords(0, 0))
            self.renderObj.text(FONT, self.renderObj.window.getScreenScale(self.pythonVersionData[0], 1), self.pythonVersion, True, (0, 0, 0), (100, 100, 100),
                                self.renderObj.window.screenSurfaces[0], *self.renderObj.window.getScreenCoords(1440 - self.pythonVersionData[1], 0))
            self.renderObj.text(FONT, self.renderObj.window.getScreenScale(self.pygameVersionData[0], 1), self.pygameVersion, True, (0, 0, 0), (100, 100, 100),
                                self.renderObj.window.screenSurfaces[0], *self.renderObj.window.getScreenCoords(1440 - self.pygameVersionData[1],
                                self.pythonVersionData[0]))
            self.renderObj.text(FONT, self.renderObj.window.getScreenScale(self.gccVersionData[0], 1), self.gccVersion, True, (0, 0, 0), (100, 100, 100),
                                self.renderObj.window.screenSurfaces[0], *self.renderObj.window.getScreenCoords(1440 - self.gccVersionData[1],
                                self.pythonVersionData[0] + self.pygameVersionData[0]))
        except IndexError:
            self.renderObj.text(FONT, 50, "FPS:" + str(int(self.renderObj.window.fps)), True, (0, 0, 0), (100, 100, 100), self.renderObj.window.surface, 0, 0)
            self.renderObj.text(FONT, self.pythonVersionData[0], self.pythonVersion, True, (0, 0, 0), (100, 100, 100), self.renderObj.window.surface,
                                1440 - self.pythonVersionData[1], 0)
            self.renderObj.text(FONT, self.pygameVersionData[0], self.pygameVersion, True, (0, 0, 0), (100, 100, 100), self.renderObj.window.surface,
                                1440 - self.pygameVersionData[1], self.pythonVersionData[0])
            self.renderObj.text(FONT, self.gccVersionData[0], self.gccVersion, True, (0, 0, 0), (100, 100, 100), self.renderObj.window.surface,
                                1440 - self.gccVersionData[1], self.pythonVersionData[0] + self.pygameVersionData[0])
