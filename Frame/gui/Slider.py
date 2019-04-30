from Frame.baseFunctions import *
from Frame.gui.Gui import Gui
from pygameImporter import *


class Slider(Gui):
    def __init__(self, function, slideColor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        output("Slider: Creating " + self.text + " slider...", "debug")
        self.wasPressed = False
        self.function = function
        self.slideColor = slideColor
        self.sliderText = None
        self.right = K_RIGHT
        self.left = K_LEFT
        self.pos = 0
    
    def update(self):
        super().update()
        output("Slider: Updating...", "complete")
        if self.rightCoords and self.pressedMouse:
            self.pos = (self.window.mousePos[0] - self.x) / self.width * 100
            self.sliderText = str(self.function(self.pos))
        if self.mouseTouchesButton and self.rightCoords and not self.window.guiHandler.keyActive or self.keyOnGui and self.rightCoords:
            if self.window.keys[self.right]:
                self.pos += self.window.dt / 50
                if self.pos > 100:
                    self.pos = 100
            if self.window.keys[self.left]:
                self.pos -= self.window.dt / 50
                if self.pos < 0:
                    self.pos = 0
            self.sliderText = str(self.function(self.pos))
            
    def render(self):
        output("Slider: Rendering...", "complete")
        text = self.text
        if self.sliderText != None:
            self.text += ":" + self.sliderText
        super().render()
        self.text = text
