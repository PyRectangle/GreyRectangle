from Frame.gui.Button import Button
from Constants import *
from Menu import Menu


class LevelSelection(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.addGui(Button, (menuHandler.showMainMenuOutOfLevelSelection, (), 40, 975, 200, 80, "Back", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), 
                             FONT, True, 30, 30, 0.1, True, [0, -1], (60, 1240), SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.openLevel, (), 280, 975, 200, 80, "Start", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30, 0.1,
                             True, [0, -1], (420, 1240), SOUNDS, menuHandler.window))
