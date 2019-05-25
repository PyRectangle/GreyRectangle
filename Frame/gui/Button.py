from Frame.baseFunctions import *
from Frame.gui.Gui import Gui


class Button(Gui):
    def __init__(self, function, functionArgs, *args, **kwargs):
        super().__init__(*args, **kwargs)
        output("Button: Creating " + self.text + " button...", "debug")
        self.wasPressed = False
        self.function = function
        self.functionArgs = functionArgs
        self.oncePressMouse = True

    def update(self):
        super().update()
        output("Button: Creating a click animastion if pressed...", "complete")
        if self.pressed and not self.wasPressed and self.rightCoords:
            if self.noAnimations:
                if type(self.functionArgs) == tuple:
                    self.function(*self.functionArgs)
                else:
                    self.function(self.functionArgs)
            else:
                self.window.guiHandler.createClickAnim(self)
        self.wasPressed = self.pressed
    
    def render(self):
        super().render()
        if self.window.guiHandler.clickAnim != None:
            self.window.guiHandler.clickAnim.render()
