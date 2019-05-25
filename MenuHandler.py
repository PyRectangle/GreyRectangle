from Menus.Main.Settings.AnimationSettings import AnimationSettings
from Menus.Main.LevelSelectionEdit.DeleteLevel import DeleteLevel
from Menus.Main.LevelSelectionEdit.CreateLevel import CreateLevel
from Menus.Main.LevelSelectionEdit import LevelSelectionEdit
from Menus.Main.Settings.VideoSettings import VideoSettings
from Menus.Main.Settings.KeyBindings import KeyBindings
from Menus.Main.LevelSelectionEdit.Rename import Rename
from Menus.Main.LevelSelection import LevelSelection
from Menus.Main.Selection.Region import RegionMenu
from Menus.Main.Selection.Block import BlockMenu
from Menus.Main.LevelOptions import LevelOptions
from Menus.Main.ActionMenu import ActionMenu
from Menus.Main.ChatMenu import ChatMenu
from Menus.Main.Settings import Settings
from Menus.Main.PlayQuit import PlayQuit
from Menus.Main.EditQuit import EditQuit
from Menus.LoadScreen import LoadScreen
from Frame.gui.Button import Button
from pygameImporter import pygame
from Frame.Render import Render
from Menus.Main import MainMenu
from Menus.Main.Ask import Ask
from Constants import *
from Menu import Menu
import os


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
        self.chatMenu = ChatMenu(self)
        self.loadScreen = LoadScreen(self)
        self.menus = [self.loadScreen]

    def create(self):
        self.mainMenu = MainMenu(self)
        self.levelSelection = LevelSelection(self)
        self.settings = Settings(self)
        self.keyBindings = KeyBindings(self)
        self.videoSettings = VideoSettings(self)
        self.playQuit = PlayQuit(self)
        self.editQuit = EditQuit(self)
        self.actionMenu = ActionMenu(self)
        self.levelSelectionEdit = LevelSelectionEdit(self)
        self.createLevelMenu = CreateLevel(self)
        self.deleteLevelMenu = DeleteLevel(self)
        self.levelOptions = LevelOptions(self)
        self.ask = Ask(self)
        self.rename = Rename(self)
        self.blockMenu = BlockMenu(self)
        self.regionMenu = RegionMenu(self)
        self.chatMenu = ChatMenu(self)
        self.loadSaveLevel = LoadScreen(self, "Saving Level...")
        self.animationSettings = AnimationSettings(self)
        self.menus = [self.mainMenu, self.levelSelection, self.settings, self.keyBindings, self.videoSettings, self.playQuit, self.editQuit, self.levelSelectionEdit,
                      self.createLevelMenu, self.deleteLevelMenu, self.actionMenu, self.levelOptions, self.ask, self.rename, self.blockMenu, self.regionMenu,
                      self.chatMenu, self.loadScreen, self.loadSaveLevel, self.animationSettings]
    
    def showLevelOptions(self):
        self.levelOptions.do = True
        self.levelOptions.up = True
        self.show(self.levelOptions)

    def showEditQuit(self):
        self.levelOptions.do = True
        self.levelOptions.up = False
        self.show(self.editQuit)

    def showEditQuitSave(self):
        if self.levelOptions.setOptions():
            self.showEditQuit()

    def setSpawn(self):
        self.main.editor.setSpawn = True

    def rotateBlocks(self):
        if self.main.editor.blockSelection.data == []:
            block = self.main.blocks.blocks[self.main.editor.selectedBlock]
            self.main.editor.blockSelection.data = [1, int(block.solid), int(block.death)]
        else:
            self.main.editor.blockSelection.data[0] += 1
            if self.main.editor.blockSelection.data[0] > 3:
                self.main.editor.blockSelection.data[0] = 0
    
    def toggleSolid(self):
        if self.main.editor.blockSelection.data == []:
            block = self.main.blocks.blocks[self.main.editor.selectedBlock]
            self.main.editor.blockSelection.data = [0, int(not block.solid), int(block.death)]
        else:
            self.main.editor.blockSelection.data[1] = int(not bool(self.main.editor.blockSelection.data[1]))
    
    def toggleDeath(self):
        if self.main.editor.blockSelection.data == []:
            block = self.main.blocks.blocks[self.main.editor.selectedBlock]
            self.main.editor.blockSelection.data = [0, int(block.solid), int(not block.death)]
        else:
            self.main.editor.blockSelection.data[2] = int(not bool(self.main.editor.blockSelection.data[2]))
    
    def setBlocksDefault(self):
        self.main.editor.blockSelection.data = []

    def showBlockSelection(self):
        self.main.editor.blockSelection.enable()

    def showActions(self):
        self.continuePlay()
        self.show(self.actionMenu)

    def showCreateLevel(self):
        self.show(self.createLevelMenu)
        self.main.levelPreview.pressLevel(None)
        self.main.levelSelection.toggle()

    def showDeleteLevel(self):
        self.deleteLevelMenu.level = self.main.levelPreview.level
        if self.deleteLevelMenu.level == None:
            self.main.warningHandler.createWarning("Select the level you want to delete !", 3)
            return
        self.show(self.deleteLevelMenu)
        self.main.levelPreview.pressLevel(None)
        self.main.levelSelection.toggle()
        self.deleteLevelMenu.do = True
        self.deleteLevelMenu.up = True
    
    def showRenameDialog(self):
        self.rename.level = self.main.levelPreview.level
        if self.rename.level == None:
            self.main.warningHandler.createWarning("Select the level you want to rename !", 3)
            return
        self.show(self.rename)
        self.main.levelPreview.pressLevel(None)
        self.main.levelSelection.toggle()

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
        self.main.warningHandler.remove(0.5)
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
            if self.main.editing:
                self.show(self.editQuit)
            else:
                self.show(self.playQuit)
        else:
            self.show(self.mainMenu)

    def saveGoBack(self, save):
        if save:
            self.main.editor.saveLevel()
        self.main.editor.changed = False
        self.goBack()

    def goBack(self):
        self.main.levelSelection.levelGuiHandler.canChange = True
        if self.main.editing:
            if self.main.editor.changed:
                self.show(self.ask)
                return
            self.goToEdit = True
        if self.main.playing:
            self.main.player.chat.chatMessages.clearChat()
            self.main.player.alphaMove = True
            self.main.player.alphaUp = False
            for block in self.main.blocks.blocks:
                if block.overlays != None:
                    block.overlay = {}
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
        self.main.warningHandler.remove(0.5)
        self.deleteLevelMenu.do = True
        self.deleteLevelMenu.up = False
        self.goToPlay = False
        self.goToEdit = False
        self.outOfPlay = False
        self.main.editor.quit = False
        self.main.player.quitMenu = False
        self.main.levelPreview.level = None
        self.main.levelSelection.levelGuiHandler.selected = None
        self.show(self.levelSelectionEdit)
        self.main.levelSelection.toggle()
        self.editor = True
    
    def saveLevel(self):
        if self.main.editor.actions != None:
            self.main.editor.saveLevel()
    
    def createLevel(self):
        if self.createLevelMenu.name == "":
            self.main.warningHandler.createWarning("You need to give the level a name !", 3)
        else:
            self.main.levelHandler.create(self.createLevelMenu.name, self.createLevelMenu.description)
            self.edit()
    
    def deleteLevel(self):
        if self.deleteLevelMenu.level != None and os.path.exists(self.deleteLevelMenu.level.folder):
            self.main.levelHandler.delete(self.deleteLevelMenu.level)
            self.edit()

    def update(self):
        if self.goToPlay and self.main.levelPreview.size == VIEW_MIN_SIZE:
            self.goToPlay = False
            if self.goToEdit:
                if self.main.editor.actions != None:
                    self.main.editor.actions.clean()
                self.edit()
            else:
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
