from pygameImporter import pygame
from random import randint
from Constants import *
import Frame
import json
import sys
import os


class Window(Frame.Window):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pygame.mixer.music.set_volume(main.config.config["Volume"] / 100)
        self.main = main
        self.key = 0

    def update(self):
        self.key = 0
        super().update()
        if self.keys[pygame.K_LALT] and self.keys[pygame.K_F4]:
            self.exit()

    def handleEvent(self, event):
        super().handleEvent(event)
        if event.type == pygame.KEYDOWN:
            self.key = event.key
    
    def onOptionalSurfaceRender(self):
        self.screenSurfaces = []
    
    def exit(self):
        finished = False
        x0 = -250
        x1 = 0
        while not finished:
            x0 += self.dt * 5
            x1 += self.dt * 4
            if x1 >= 1500:
                finished = True
            pygame.draw.polygon(self.surface, (0, 0, 0), [[x0, 0], [x1, 1080], [0, 1080], [0, 0]])
            self.updateClock()
            self.updateDisplay()
        pygame.quit()
        self.main.config.config["DebugScreenActive"] = self.main.debugScreenActive
        self.main.config.config["FPSLimit"] = self.main.window.fpsLimit
        self.main.config.config["Fullscreen"] = self.fullscreen
        toggledSDL = self.main.config.config["SDL2"] != json.load(open(CONFIG_FILE))["SDL2"]
        if toggledSDL:
            keyTranslate = self.main.menuHandler.videoSettings.keyTranslate
            for key in self.main.config.config["Controls"]:
                if self.main.config.config["SDL2"]:
                    self.main.config.config["Controls"][key] = keyTranslate.translate1to2(self.main.config.config["Controls"][key])
                else:
                    self.main.config.config["Controls"][key] = keyTranslate.translate2to1(self.main.config.config["Controls"][key])
        self.main.config.save()
        if self.main.editor.actions != None:
            self.main.editor.actions.clean()
        sys.exit(0)
