from Frame.gui.Button import Button
from Frame.Render import Render
from Constants import *
from Menu import Menu


class Ask(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.do = False
        self.up = False
        self.alpha = 0
        self.window = menuHandler.window
        self.renderObj = Render(menuHandler.window)
        self.addGui(Button, (menuHandler.continuePlay, (), 40, 940, 200, 100, "Back", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30,
                             0.1, True, [0, -1], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.saveGoBack, (True), 470, 490, 200, 100, "Yes", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30,
                             0.1, True, [1, 0], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.saveGoBack, (False), 770, 490, 200, 100, "No", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30,
                             0.1, True, [-1, 0], None, SOUNDS, menuHandler.window))

    def create(self):
        super().create()
        self.do = True
        self.up = True
    
    def remove(self):
        super().remove()
        self.do = True
        self.up = False

    def update(self):
        super().update()
        if self.do:
            if self.up:
                self.alpha += self.window.dt
                if self.alpha > 255:
                    self.alpha = 255
                    self.do = False
            else:
                self.alpha -= self.window.dt
                if self.alpha < 1:
                    self.do = False
                    self.alpha = 1
    
    def render(self):
        super().render()
        text = "Do you want to save before quitting ?"
        size = self.renderObj.getTextSizeForWidth(text, 100, SURFACE_SIZE[0], FONT)
        self.renderObj.text(FONT, size, text, True, (0, 0, 0), None, self.window.surface, addY = -60 - size, alpha = self.alpha)
