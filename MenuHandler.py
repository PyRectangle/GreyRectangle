from Menus.Main.Settings.VideoSettings import VideoSettings
from Menus.Main.Settings.KeyBindings import KeyBindings
from Menus.Main.LevelSelection import LevelSelection
from Menus.Main.Settings import Settings
from Menus.Main.PlayQuit import PlayQuit
from Menus.Main.EditQuit import EditQuit
from Frame.gui.Button import Button
from Menus.Main import MainMenu
from Constants import *
from Menu import Menu
import pygame


class MenuHandler:
    def __init__(self, main):
        self.menus = []
        self.main = main
        self.window = main.window
        self.mainMenu = None
        self.settings = None
        self.keyBindings = None
        self.levelSelection = None
        self.mainMenu = MainMenu(self)
        self.levelSelection = LevelSelection(self)
        self.settings = Settings(self)
        self.keyBindings = KeyBindings(self)
        self.editor = False
        self.outOfPlay = False
        self.goToPlay = False
        self.goToEdit = False
            
    def create(self):
        self.mainMenu = MainMenu(self)
        self.levelSelection = LevelSelection(self)
        self.settings = Settings(self)
        self.keyBindings = KeyBindings(self)
        self.videoSettings = VideoSettings(self)
        self.playQuit = PlayQuit(self)
        self.editQuit = EditQuit(self)
        self.menus = [self.mainMenu, self.levelSelection, self.settings, self.keyBindings, self.videoSettings, self.playQuit, self.editQuit]
    
    def showKeyBindings(self):
        self.main.keyBindingsMenu.create()
        self.show(self.keyBindings)

    def closeKeyBindings(self):
        self.main.keyBindingsMenu.remove()
        self.show(self.settings)

    def getFPSLimit(self, percent):
        limit = int(0.9 * percent + 10.5)
        text = limit
        if limit == 100:
            limit = 0
            text = "Unlimited"
        self.main.window.fpsLimit = limit
        return text
    
    def getVolume(self, percent):
        volume = int(percent)
        self.main.config.config["Volume"] = volume
        self.main.window.guiHandler.volume = volume / 100
        pygame.mixer.music.set_volume(volume / 100)
        return volume

    def openLevel(self):
        self.main.levelPreview.open()
    
    def showMainMenuOutOfLevelSelection(self):
        self.main.levelSelection.levelGuiHandler.lastSelected = None
        self.main.levelSelection.levelGuiHandler.selected = None
        self.editor = False
        self.show(self.mainMenu)
        self.main.levelPreview.pressLevel(None)
        self.main.levelSelection.toggle()

    def continuePlay(self):
        self.remove()
        self.main.player.quitMenu = False
        self.main.editor.quit = False
    
    def showSettings(self):
        self.outOfPlay = True
        self.show(self.settings)

    def outOfSettings(self):
        if self.outOfPlay:
            self.show(self.playQuit)
        else:
            self.show(self.mainMenu)

    def goBack(self):
        self.main.levelSelection.levelGuiHandler.canChange = True
        if self.main.editing:
            self.goToEdit = True
        if self.main.playing or self.main.editing:
            self.main.levelPreview.size = self.main.camera.size
            self.main.levelPreview.sizeDirect = False
            self.main.levelPreview.moveSize = True
            self.main.levelPreview.opened = False
            self.main.levelPreview.useBlockWidth = True
            self.main.playing = False
            self.main.editing = False
            self.main.editor.size = 100
        self.goToPlay = True
        self.remove()

    def play(self):
        self.main.levelSelection.levelGuiHandler.selected = None
        self.main.levelPreview.level = None
        self.main.player.quitMenu = False
        self.main.editor.quit = False
        self.goToEdit = False
        self.goToPlay = False
        self.outOfPlay = False
        self.show(self.levelSelection)
        self.main.levelSelection.toggle()
    
    def edit(self):
        self.goToPlay = False
        self.goToEdit = False
        self.main.levelPreview.level = None
        self.main.levelSelection.levelGuiHandler.selected = None
        self.show(self.levelSelection)
        self.main.levelSelection.toggle()
        self.editor = True

    def update(self):
        if self.goToPlay and self.main.levelPreview.size == VIEW_MIN_SIZE:
            self.goToPlay = False
            self.play()
        for menu in self.menus:
            if menu.created or menu.createdGuis != []:
                menu.update()
    
    def render(self):
        for menu in self.menus:
            if menu.created or menu.createdGuis != []:
                menu.render()
    
    def remove(self):
        for menu in self.menus:
            if menu.created:
                menu.remove()

    def show(self, menu):
        self.remove()
        if type(menu) == int:
            self.menus[menu].create()
        else:
            menu.create()
