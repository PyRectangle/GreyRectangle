from Menus.Main.Settings.KeyBindings import KeyBindings
from Menus.Main.LevelSelection import LevelSelection
from Menus.Main.Settings import Settings
from Frame.gui.Button import Button
from Menus.Main import MainMenu
from Menu import Menu


class MenuHandler:
    def __init__(self, main):
        self.menus = []
        self.main = main
        self.window = main.window
        self.FONT = "resources/fonts/freesansbold.ttf"
        self.mainMenu = None
        self.settings = None
        self.keyBindings = None
        self.levelSelection = None
        self.mainMenu = MainMenu(self)
        self.levelSelection = LevelSelection(self)
        self.settings = Settings(self)
        self.keyBindings = KeyBindings(self)

    
    def create(self):
        self.mainMenu = MainMenu(self)
        self.levelSelection = LevelSelection(self)
        self.settings = Settings(self)
        self.keyBindings = KeyBindings(self)
        self.menus = [self.mainMenu, self.levelSelection, self.settings, self.keyBindings]
    
    def openLevel(self):
        pass
    
    def showMainMenuOutOfLevelSelection(self):
        self.show(self.mainMenu)
        self.main.levelSelection.toggle()
    
    def play(self):
        self.show(self.levelSelection)
        self.main.levelSelection.toggle()

    def update(self):
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
