from Frame.gui.Button import Button
from Constants import *
from Menu import Menu


class EditQuit(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.addGui(Button, (menuHandler.continuePlay, (), 370, 190, 700, 100, "Continue", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30,
                             0.1, True, [0, 1], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.showSettings, (), 370, 340, 700, 100, "Settings", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30,
                             30, 0.1, True, [-1, 1], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.goBack, (), 370, 490, 700, 100, "Back to menu", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30,
                             0.1, True, [-2, 0], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.showLevelOptions, (), 370, 640, 700, 100, "Level Options", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [-1, -1], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.showActions, (), 370, 790, 700, 100, "Actions", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30,
                             0.1, True, [0, -1], None, SOUNDS, menuHandler.window))
