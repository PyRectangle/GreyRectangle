from Frame.gui.Button import Button
from Constants import *
from Menu import Menu


class ActionMenu(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.addGui(Button, (menuHandler.continuePlay, (), 40, 975, 300, 40, "Back", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30,
                             0.1, True, [0, -1], (60, 1240), SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.saveLevel, (), 40, 925, 300, 40, "Save", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [0, -1], (60, 1240), SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.showBlockSelection, (), 40, 875, 300, 40, "Select Block", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [0, -1], (60, 1240), SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.rotateBlocks, (), 40, 825, 300, 40, "Rotate", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [0, -1], (60, 1240), SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.toggleSolid, (), 40, 775, 300, 40, "Toggle Solid", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [0, -1], (60, 1240), SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.toggleDeath, (), 40, 725, 300, 40, "Toggle Death", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [0, -1], (60, 1240), SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.setBlocksDefault, (), 40, 675, 300, 40, "Default", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [0, -1], (60, 1240), SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.setSpawn, (), 40, 625, 300, 40, "Set Spawn", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [0, -1], (60, 1240), SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.main.editor.selectRegion, (), 40, 575, 300, 40, "Select Regions", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0),
                             FONT, True, 30, 30, 0.1, True, [0, -1], (60, 1240), SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.main.editor.selectBlock, (), 40, 525, 300, 40, "Select", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30,
                             0.1, True, [0, -1], (60, 1240), SOUNDS, menuHandler.window))
