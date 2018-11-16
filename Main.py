from Level.LevelHandler import LevelHandler
from KeyBindingsMenu import KeyBindingsMenu
from LevelSelection import LevelSelection
from MenuHandler import MenuHandler
from DebugScreen import DebugScreen
from Level.View import View
from Player import Player
from Editor import Editor
from Camera import Camera
from Window import Window
from Config import Config
from Blocks import Blocks
import pygame
import Frame
import time
import os


class Main:
    def __init__(self):
        self.config = Config()
        self.config.load()
        self.window = Window(self, "GreyRectangle", (640, 480), (1440, 1080), flags = Frame.RESIZABLE | Frame.HWSURFACE | Frame.HWPALETTE | Frame.HWACCEL,
                             icon = "resources/images/icon.png")
        self.menuHandler = MenuHandler(self)
        self.menuHandler.create()
        self.menuHandler.show(self.menuHandler.mainMenu)
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
        self.debugScreenActive = self.config.config["DebugScreenActive"]
        self.window.fpsLimit = self.config.config["FPSLimit"]
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
            self.window.surface.fill((255, 255, 255))
            if self.playing and not self.levelPreview.shouldRender:
                self.camera.update()
                self.player.update()
                self.camera.render()
                self.player.render()
            if self.editing and not self.levelPreview.shouldRender:
                self.camera.update()
                self.editor.update()
                self.camera.render()
                self.editor.render()
            updatedPreview = False
            if self.levelPreview.shouldRender:
                self.levelPreview.update()
                self.levelPreview.render()
                updatedPreview = True
            if self.menuHandler.levelSelection.createdGuis != [] or not self.levelSelection.closed or self.menuHandler.goToPlay:
                if not updatedPreview:
                    self.levelPreview.update()
                self.levelSelection.update()
                self.levelPreview.render()
                self.levelSelection.render()
            if self.menuHandler.keyBindings.createdGuis != []:
                self.keyBindingsMenu.update()
                self.keyBindingsMenu.render()
            self.menuHandler.render()
            if self.debugScreenActive:
                self.debugScreen.render()
            self.window.updateDisplay()
        self.window.exit()

Main()
