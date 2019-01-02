from Frame.Render import Render
from Constants import *


class GameWarning:
    def __init__(self, timeOut, text, window):
        self.timeOut = timeOut
        self.showTime = 0
        self.text = text
        self.window = window
        self.showing = False
        self.active = False
        self.alpha = 1
        self.renderObj = Render(self.window)
        self.show()
    
    def show(self):
        self.showTime = 0
        self.showing = True

    def update(self):
        if self.showing:
            self.active = True
            self.showTime += self.window.dt / 1000
            if self.showTime >= self.timeOut:
                self.showing = False
        else:
            self.showTime -= self.window.dt / 1000
        self.alpha = self.showTime / self.timeOut * 255
        if self.alpha < 1:
            self.active = False
            self.alpha = 1
    
    def render(self):
        if self.alpha != 1:
            self.renderObj.text(FONT, self.renderObj.getTextSizeForWidth(self.text, 150, SURFACE_SIZE[0], FONT), self.text, True, (255, 0, 0), None, self.window.surface,
                                alpha = self.alpha)
