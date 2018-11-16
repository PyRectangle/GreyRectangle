from Frame.gui.Button import Button
from Frame.gui.Slider import Slider
from Constants import *
from Menu import Menu


class VideoSettings(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.menuHandler = menuHandler
        self.addGui(Button, (menuHandler.show, (menuHandler.settings), 60, 940, 300, 100, "Back", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [1, 0], None, SOUNDS, menuHandler.window))
        self.addGui(Slider, (menuHandler.getFPSLimit, (200, 200, 200), 60, 80, 800, 120, "FPS Limit", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT,
                             True, 30, 30, 0.1, True, [0, 1], None, SOUNDS, menuHandler.window, 80))
    
    def create(self):
        super().create()
        limit = self.menuHandler.main.window.fpsLimit
        if self.menuHandler.main.window.fpsLimit == 0:
            limit = 100
        percent = limit / 0.9 - 11
        self.createdGuis[1].sliderText = str(self.createdGuis[1].function(percent))
        self.createdGuis[1].pos = percent
