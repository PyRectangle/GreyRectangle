from Frame.gui.Button import Button
from Constants import *
from Menu import Menu


class LevelSelectionEdit(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.addGui(Button, (menuHandler.showMainMenuOutOfLevelSelection, (), 40, 1035, 200, 30, "Back", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT,
                             True, 30, 30, 0.1, True, [0, -1], (60, 1290), SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.openLevel, (), 280, 1035, 200, 30, "Start", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30, 0.1,
                             True, [0, -1], (420, 1290), SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.showDeleteLevel, (), 40, 995, 200, 30, "Delete Level", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30,
                             30, 0.1, True, [0, -1], (60, 1240), SOUNDS, menuHandler.window, 30))
        self.addGui(Button, (menuHandler.showCreateLevel, (), 280, 995, 200, 30, "Create Level", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30,
                             30, 0.1, True, [0, -1], (420, 1240), SOUNDS, menuHandler.window, 30))
        self.addGui(Button, (menuHandler.showRenameDialog, (), 40, 955, 200, 30, "Rename", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30,
                             30, 0.1, True, [0, -1], (60, 1195), SOUNDS, menuHandler.window, 30))
