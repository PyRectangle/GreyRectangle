from Frame.gui.LineEdit import LineEdit
from Frame.gui.Button import Button
from Constants import *
from Menu import Menu


class Rename(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.level = None
        self.name = ""
        self.menuHandler = menuHandler
        self.addGui(Button, (menuHandler.edit, (), 40, 900, 400, 100, "Cancel", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30, 0.1, True,
                             [0, -1], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (self.rename, (), 1000, 900, 400, 100, "Rename", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30, 0.1,
                             True, [0, -1], None, SOUNDS, menuHandler.window))
        self.addGui(LineEdit, ((100, 100, 255), (200, 200, 255), 30, 220, 350, 1000, 100, "Enter a level name.", (150, 150, 150), (0, 0, 0), (100, 100, 255),
                               (0, 0, 0), FONT, True, 30, 30, 0.1, True, [1, 0], None, SOUNDS, menuHandler.window))

    def rename(self):
        if self.level != None:
            if self.name == "":
                self.menuHandler.main.warningHandler.createWarning("You need to type in a name !", 5)
            else:
                self.level.rename(self.name)
                self.menuHandler.edit()

    def update(self):
        super().update()
        try:
            self.name = self.createdGuis[2].text
        except (IndexError, AttributeError):
            self.name = ""
