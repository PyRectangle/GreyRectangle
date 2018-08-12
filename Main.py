from Window import Window
from Menus import Menus
import Frame
import imp


class Main:
    def __init__(self):
        self.window = Window("GreyRectangle", (640, 480), (1440, 1080), flags = Frame.RESIZABLE)
        self.menus = Menus(self)
        self.menus.create()
        self.menus.show(0)
        self.loop()
    
    def loadConfig(self):
        self.config = imp.load_source('config', 'config')
        
    def loop(self):
        while self.window.isOpen:
            if self.window.keys[Frame.K_SPACE]:
                self.window.toggleFullscreen()
            self.window.update()
            self.menus.update()
            self.window.surface.fill((255, 255, 255))
            self.menus.render()
            self.window.updateDisplay()
        self.window.exit()

Main()
