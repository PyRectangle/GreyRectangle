from Level.LevelHandler import LevelHandler
from KeyBindingsMenu import KeyBindingsMenu
from LevelSelection import LevelSelection
from WarningHandler import WarningHandler
from MenuHandler import MenuHandler
from DebugScreen import DebugScreen
from pygameImporter import *
from Level.View import View
from Player import Player
from Editor import Editor
from Camera import Camera
from Window import Window
from Config import Config
from Blocks import Blocks
from Constants import *
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
        self.window = Window(self, "GreyRectangle", WINDOW_SIZE, SURFACE_SIZE, flags = Frame.RESIZABLE, icon = self.icon, fullscreen = self.config.config["Fullscreen"])
        self.player = Player(self)
        self.menuHandler = MenuHandler(self)
        self.menuHandler.show(self.menuHandler.loadScreen)
        self.setProgress(0)
        self.blocks = Blocks(self)
        self.editor = Editor(self)
        self.camera = Camera(self)
        self.menuHandler.create()
        self.warningHandler = WarningHandler(self.window)
        self.keyBindingsMenu = KeyBindingsMenu(self)
        self.levelPreview = View(self)
        self.levelHandler = LevelHandler(self)
        self.levelSelection = LevelSelection(self)
        self.debugScreen = DebugScreen(self.window)
        self.window.guiChanger = self.config.config["Controls"]["GuiChanger"]
        self.window.guiPresser = self.config.config["Controls"]["GuiPresser"]
        self.window.guiEscape = self.config.config["Controls"]["Escape"]
        self.debugScreenActive = self.config.config["DebugScreenActive"]
        self.window.fpsLimit = self.config.config["FPSLimit"]
        self.window.useBusyLoop = self.config.config["UseBusyLoop"]
        self.menuHandler.getVolume(self.config.config["Volume"])
        self.window.disableGuiAnimations = not self.config.config["GuiStaticAnimations"]
        self.window.disableGuiComeInAnimations = not self.config.config["GuiComeInAnimations"]
        self.playing = False
        self.editing = False
        if failedSDL2Import:
            self.warningHandler.createWarning("Unable to import pygame_sdl2 !", 2)
        self.setProgress(100)
        self.window.updateClock()
        self.loop()
    
    def setProgress(self, progress):
        self.progress = progress
        self.menuHandler.loadScreen.createdGuis[0].setProgress(progress)
        self.menuHandler.update()
        self.window.update()
        self.window.surface.fill((255, 255, 255))
        self.menuHandler.render()
        self.window.updateDisplay()

    def loop(self):
        while self.window.isOpen:
            if self.window.key == self.config.config["Controls"]["FullScreen"]:
                self.window.toggleFullscreen()
            if self.window.key == self.config.config["Controls"]["ScreenShot"]:
                if pygame.K_F11 > 1000:
                    self.warningHandler.createWarning("Screenshots are not supported in SDL2 !", 3)
                else:
                    if not os.path.exists("Screenshots"):
                        os.makedirs("Screenshots")
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
                if not self.config.config["GuiComeInAnimations"]:
                    self.player.activeCount = 2
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
