from Level.LevelHandler import LevelHandler
from KeyBindingsMenu import KeyBindingsMenu
from LevelSelection import LevelSelection
from WarningHandler import WarningHandler
from MenuHandler import MenuHandler
from DebugScreen import DebugScreen
from Level.View import View
from Player import Player
from Editor import Editor
from Camera import Camera
from Window import Window
from Config import Config
from Blocks import Blocks
from Constants import *
import pygame
import Frame
import time
import os


class Main:
    def __init__(self):
        self.config = Config()
        self.config.load()
        self.icon = pygame.Surface((32, 32))
        self.icon.set_colorkey((0, 0, 0))
        pygame.draw.polygon(self.icon, (150, 150, 150), [[8, 0], [8, 32], [24, 32], [24, 0]])
        self.window = Window(self, "GreyRectangle", WINDOW_SIZE, SURFACE_SIZE, flags = Frame.RESIZABLE | Frame.HWSURFACE | Frame.HWPALETTE | Frame.HWACCEL,
                             icon = self.icon)
        self.menuHandler = MenuHandler(self)
        self.menuHandler.create()
        self.menuHandler.show(self.menuHandler.mainMenu)
        self.warningHandler = WarningHandler(self.window)
        self.levelHandler = LevelHandler(self)
        self.levelSelection = LevelSelection(self)
        self.keyBindingsMenu = KeyBindingsMenu(self)
        self.levelPreview = View(self)
        self.player = Player(self)
        self.editor = Editor(self)
        self.camera = Camera(self)
        self.debugScreen = DebugScreen(self.window)
        self.window.guiChanger = self.config.config["Controls"]["GuiChanger"]
        self.window.guiPresser = self.config.config["Controls"]["GuiPresser"]
        self.window.guiEscape = self.config.config["Controls"]["Escape"]
        self.debugScreenActive = self.config.config["DebugScreenActive"]
        self.window.fpsLimit = self.config.config["FPSLimit"]
        self.window.useBusyLoop = self.config.config["UseBusyLoop"]
        self.menuHandler.getVolume(self.config.config["Volume"])
        self.blocks = Blocks()
        self.playing = False
        self.editing = False
        self.loop()

    def loop(self):
        while self.window.isOpen:
            if self.window.key == self.config.config["Controls"]["FullScreen"]:
                self.window.toggleFullscreen()
            if self.window.key == self.config.config["Controls"]["ScreenShot"]:
                currentTime = time.localtime()
                count = ""
                name = "Screenshots/screenshot-" + str(currentTime.tm_hour) + ":" + str(currentTime.tm_min) + ":" + str(currentTime.tm_sec)
                while os.path.exists(name + str(count) + ".png"):
                    if count == "":
                        count = 0
                    count -= 1
                pygame.image.save(self.window.surface, name + str(count) + ".png")
            if self.window.key == self.config.config["Controls"]["DebugScreen"]:
                self.debugScreenActive = not self.debugScreenActive
            self.window.update()
            self.menuHandler.update()
            self.warningHandler.update()
            self.window.surface.fill((255, 255, 255))
            if self.playing and not self.levelPreview.shouldRender:
                self.camera.update()
                self.player.update()
                self.camera.render()
                self.player.render()
            if self.editing and not self.levelPreview.shouldRender:
                self.editor.update()
                self.camera.update()
                self.camera.render()
                self.editor.render()
            updatedPreview = False
            if self.levelPreview.shouldRender:
                self.levelPreview.update()
                self.levelPreview.render()
                updatedPreview = True
            if self.menuHandler.levelSelection.createdGuis != [] or self.menuHandler.levelSelectionEdit.createdGuis != [] or not self.levelSelection.closed or \
               self.menuHandler.goToPlay:
                self.player.update(False)
                self.player.render()
                if not updatedPreview:
                    self.levelPreview.update()
                self.levelSelection.update()
                self.levelPreview.render()
                self.levelSelection.render()
            if self.menuHandler.keyBindings.createdGuis != []:
                self.keyBindingsMenu.update()
                self.keyBindingsMenu.render()
            self.menuHandler.render()
            if self.warningHandler.isActive:
                self.warningHandler.render()
            if self.debugScreenActive:
                self.debugScreen.render()
            self.window.updateDisplay()
        self.window.exit()

Main()
