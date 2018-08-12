from Frame.gui.ClickAnim import ClickAnim
from Frame.gui.Gui import Gui


class Button(Gui):
    def __init__(self, function, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wasPressed = False
        self.function = function
        self.clickAnims = []

    def update(self):
        super().update()
        if self.pressed and not self.wasPressed and self.rightCoords:
            self.clickAnims.append(ClickAnim(self))
        self.removables = []
        for i in range(len(self.clickAnims)):
            self.clickAnims[i].update()
            if self.clickAnims[i].finished:
                self.removables.append(i)
        subtract = 0
        for i in self.removables:
            del self.clickAnims[i - subtract]
            subtract += 1
        self.wasPressed = self.pressed
    
    def render(self):
        super().render()
        for clickAnim in self.clickAnims:
            clickAnim.render()
