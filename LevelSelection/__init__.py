from LevelSelection.LevelGuiHandler import LevelGuiHandler
from LevelSelection.Graphic import Graphic
from Frame.Render import Render
from Constants import *


class LevelSelection:
    def __init__(self, main):
        self.window = main.window
        self.main = main
        self.closed = True
        self.toggleClosed = True
        self.textAlpha = 255
        self.textAlphaUp = False
        self.renderObj = Render(self.window)
        self.text = "Levelinfo"
        self.showText = "Levelinfo"
        self.levelGuiHandler = LevelGuiHandler(main.levelHandler.levelObjs, main)
        self.graphics = [Graphic((150, 50, 200), [[0, 0], [600, 0], [450, 400], [0, 400]], [-600, -400], 1, self.window),
                         Graphic((150, 150, 150), [[0, 0], [500, 0], [388, 300], [0, 300]], [-600, -400], 1, self.window, (FONT, 50, self.text, True, (0, 0, 0),
                                                                                                                           None),
                                 10, 10),
                         Graphic((150, 50, 200), [[0, 850], [570, 850], [660, 1080], [0, 1080]], [0, 250], 1, self.window),
                         Graphic((150, 150, 150), [[0, 950], [510, 950], [560, 1080], [0, 1080]], [0, 250], 1, self.window),
                         Graphic((150, 50, 200), [[900, 1080], [750, 720], [750, 360], [900, 0], [1000, 0], [850, 360], [850, 720], [1000, 1080]], [800, 0], 1,
                                 self.window),
                         Graphic((150, 150, 150), [[1000, 0], [850, 360], [850, 720], [1000, 1080], [1440, 1080], [1440, 0]], [800, 0], 1, self.window)]

    def setText(self, text):
        self.showText = text

    def toggle(self):
        self.toggleClosed = not self.toggleClosed
        self.closed = False
        for graphic in self.graphics:
            graphic.toggle()
        self.levelGuiHandler.toggle()

    def update(self):
        if self.showText != self.text:
            self.textAlphaUp = False
            self.textAlpha -= self.window.dt * LEVEL_INFO_ALPHA_CHANGE_SPEED
            if self.textAlpha < 0:
                self.textAlpha = 0
                self.text = self.showText
                self.textAlphaUp = True
                self.graphics[1].text = (FONT, self.renderObj.getTextSizeForWidth(self.text, 80, 450, FONT), self.text, True, (0, 0, 0), None)
        elif self.textAlpha != 255:
            self.textAlphaUp = True
        if self.textAlphaUp:
            self.textAlpha += self.window.dt * LEVEL_INFO_ALPHA_CHANGE_SPEED
            if self.textAlpha > 255:
                self.textAlpha = 255
                self.textAlphaUp = False
        self.closed = True
        for graphic in self.graphics:
            graphic.update()
            if not graphic.isClosed:
                self.closed = False
        self.levelGuiHandler.update()
    
    def render(self):
        self.graphics[1].textAlpha = self.textAlpha
        for graphic in self.graphics:
            graphic.render()
        self.levelGuiHandler.render()
