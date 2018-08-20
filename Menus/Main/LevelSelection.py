from Frame.gui.Button import Button
from Menu import Menu


class LevelSelection(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.addGui(Button, (menuHandler.showMainMenuOutOfLevelSelection, (), 60, 940, 300, 100, "Back", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), 
                             menuHandler.FONT, True, 30, 30, 0.1, True, [0, -1], (60, 1240), self.SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.openLevel, (), 420, 940, 300, 100, "Start", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), menuHandler.FONT,
                             True, 30, 30, 0.1, True, [0, -1], (420, 1240), self.SOUNDS, menuHandler.window))
