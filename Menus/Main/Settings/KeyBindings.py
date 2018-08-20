from Frame.gui.Button import Button
from Menu import Menu


class KeyBindings(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.addGui(Button, (menuHandler.show, (menuHandler.settings), 60, 940, 300, 100, "Back", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0),
                             menuHandler.FONT, True, 30, 30, 0.1, True, [1, 0], None, self.SOUNDS, menuHandler.window))
