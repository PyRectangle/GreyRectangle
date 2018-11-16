from Frame.gui.Button import Button
from Constants import *
from Menu import Menu


class KeyBindings(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.addGui(Button, (menuHandler.closeKeyBindings, (), 60, 940, 300, 100, "Back", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30,
                             0.1, True, [1, 0], None, SOUNDS, menuHandler.window))
