from Menus.Main.PlayQuit import PlayQuit
from Frame.gui.Button import Button
from Constants import *


class EditQuit(PlayQuit):
    def __init__(self, menuHandler):
        super().__init__(menuHandler)
        self.addGui(Button, (menuHandler.showActions, (), 370, 790, 700, 100, "Actions", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30,
                             0.1, True, [0, -0.5], None, SOUNDS, menuHandler.window))
