from Frame.gui.ProgressBar import ProgressBar
from Constants import *
from Menu import Menu


class LoadScreen(Menu):
    def __init__(self, menuHandler, text = "Loading Game..."):
        super().__init__()
        self.start = text == "Loading Game..."
        self.menuHandler = menuHandler
        self.addGui(ProgressBar, (0, (255, 0, 0), 20, 440, 1400, 200, text, (100, 100, 100), (0, 0, 0), (100, 100, 100), (0, 0, 0), FONT, True, 0, 1, 0.1,
                                  self.start, [0, -2], [20, 440], None, menuHandler.window, 100))

    def create(self):
        super().create()
    
    def update(self):
        super().update()
        if self.start:
            if self.createdGuis[0].progress == 100:
                self.menuHandler.show(self.menuHandler.mainMenu)
                self.start = False
