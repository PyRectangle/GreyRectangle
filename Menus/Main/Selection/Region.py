from Frame.gui.Button import Button
from Constants import *
from Menu import Menu


class RegionMenu(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.main = menuHandler.main
        self.addGui(Button, (menuHandler.main.editor.deselect, (), 1100, 975, 300, 60, "Deselect", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [0, -1], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.main.editor.fill, (), 1100, 905, 300, 60, "Fill", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [0, -1], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.main.editor.clone, (), 1100, 835, 300, 60, "Clone", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [0, -1], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.main.editor.removeRegions, (), 1100, 755, 300, 60, "Remove", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [0, -1], None, SOUNDS, menuHandler.window))

    def remove(self):
        super().remove()
        self.main.editor.deselect()
