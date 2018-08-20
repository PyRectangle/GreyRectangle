from LevelSelection import LevelSelection
from Window import Window
from MenuHandler import MenuHandler
import Frame
import imp


class Main:
    def __init__(self):
        self.window = Window("GreyRectangle", (640, 480), (1440, 1080), flags = Frame.RESIZABLE | Frame.HWSURFACE | Frame.HWPALETTE | Frame.HWACCEL)
        self.menuHandler = MenuHandler(self)
        self.menuHandler.create()
        self.menuHandler.show(self.menuHandler.mainMenu)
        self.levelSelection = LevelSelection(self)
        self.loadConfig()
        self.loop()
    
    def loadConfig(self):
        self.config = imp.load_source('config', 'config')
        self.window.guiChanger = self.config.GuiChanger
        self.window.guiPresser = self.config.GuiPresser
        
    def loop(self):
        while self.window.isOpen:
            if self.window.keys[self.config.FullScreen]:
                self.window.toggleFullscreen()
            self.window.update()
            self.menuHandler.update()
            self.window.surface.fill((255, 255, 255))
            if self.menuHandler.levelSelection.createdGuis != [] or not self.levelSelection.closed:
                self.levelSelection.update()
                self.levelSelection.render()
            self.menuHandler.render()
            self.window.updateDisplay()
        self.window.exit()

Main()
