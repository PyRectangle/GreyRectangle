from Frame.gui.Button import Button
from Frame.gui.Slider import Slider
from Constants import *
from Menu import Menu


class Settings(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.menuHandler = menuHandler
        self.addGui(Button, (menuHandler.outOfSettings, (), 60, 940, 300, 100, "Back", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30,
                             0.1, True, [0, -1], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.showKeyBindings, (), 60, 80, 800, 120, "KeyBindings", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [0, 1], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.show, (4), 60, 220, 880, 120, "Video Settings", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30,
                             0.1, True, [0, 1], None, SOUNDS, menuHandler.window))
        self.addGui(Slider, (menuHandler.getVolume, (200, 200, 200), 60, 360, 800, 120, "Volume", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [0, 1], None, SOUNDS, menuHandler.window))

    def create(self):
        super().create()
        self.createdGuis[3].pos = self.menuHandler.main.config.config["Volume"]
        self.createdGuis[3].sliderText = str(self.menuHandler.main.config.config["Volume"])
