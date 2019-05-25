from Frame.gui.Button import Button
from Constants import *
from Menu import Menu


class AnimationSettings(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.menuHandler = menuHandler
        self.addGui(Button, (menuHandler.show, (menuHandler.videoSettings), 60, 940, 300, 100, "Back", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT,
                             True, 30, 30, 0.1, True, [1, 0], None, SOUNDS, menuHandler.window))
        self.addGui(Button, (self.toggleGuiComeIn, (), 60, 80, 900, 120, "Gui Transitions: on", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30,
                             30, 0.1, True, [1, 1], None, SOUNDS, menuHandler.window, 80))
        self.addGui(Button, (self.toggleGuiAnimations, (), 60, 240, 900, 120, "Gui Animations: on", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [1, 1], None, SOUNDS, menuHandler.window, 80))
        self.addGui(Button, (self.toggleLevelTransitions, (), 60, 400, 900, 120, "Level Transitions: on", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT,
                             True, 30, 30, 0.1, True, [1, 1], None, SOUNDS, menuHandler.window, 80))
        self.addGui(Button, (self.toggleBlockAnimations, (), 60, 560, 900, 120, "Block Animations: on", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT,
                             True, 30, 30, 0.1, True, [1, 1], None, SOUNDS, menuHandler.window, 80))
        self.addGui(Button, (self.toggleExitAnimation, (), 60, 720, 900, 120, "Exit Animation: on", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [1, 1], None, SOUNDS, menuHandler.window, 80))
    
    def update(self):
        super().update()
        if self.menuHandler.main.config.config["GuiComeInAnimations"] == self.menuHandler.window.disableGuiComeInAnimations:
            self.toggleGuiComeIn(False)
        if self.menuHandler.main.config.config["GuiStaticAnimations"] == self.menuHandler.window.disableGuiAnimations:
            self.toggleGuiAnimations(False)

    def toggleBlockAnimations(self, toggle = True):
        if toggle:
            self.menuHandler.main.config.config["BlockAnimations"] = not self.menuHandler.main.config.config["BlockAnimations"]
        state = "off"
        if self.menuHandler.main.config.config["BlockAnimations"]:
            state = "on"
        self.createdGuis[4].text = "Block Animations: " + state

    def toggleLevelTransitions(self, toggle = True):
        if toggle:
            self.menuHandler.main.config.config["LevelTransitions"] = not self.menuHandler.main.config.config["LevelTransitions"]
        state = "off"
        if self.menuHandler.main.config.config["LevelTransitions"]:
            state = "on"
        self.createdGuis[3].text = "Level Transitions: " + state

    def toggleGuiComeIn(self, toggle = True):
        if toggle:
            self.menuHandler.window.disableGuiComeInAnimations = not self.menuHandler.window.disableGuiComeInAnimations
            for gui in self.menuHandler.main.window.guiHandler.allGuis:
                gui.comeIn = not self.menuHandler.window.disableGuiComeInAnimations
                gui.direction = [1, 1]
        self.menuHandler.main.config.config["GuiComeInAnimations"] = not self.menuHandler.window.disableGuiComeInAnimations
        state = "off"
        if not self.menuHandler.window.disableGuiComeInAnimations:
            state = "on"
        self.createdGuis[1].text = "Gui Transitions: " + state

    def toggleGuiAnimations(self, toggle = True):
        if toggle:
            self.menuHandler.window.disableGuiAnimations = not self.menuHandler.window.disableGuiAnimations
            for gui in self.menuHandler.main.window.guiHandler.allGuis:
                gui.x = gui.startCoords[0]
                gui.y = gui.startCoords[1]
                gui.width = gui.startCoords[2]
                gui.height = gui.startCoords[3]
                gui.coords = gui.startCoords.copy()
                gui.noAnimations = self.menuHandler.window.disableGuiAnimations
        self.menuHandler.main.config.config["GuiStaticAnimations"] = not self.menuHandler.window.disableGuiAnimations
        state = "off"
        if not self.menuHandler.window.disableGuiAnimations:
            state = "on"
        self.createdGuis[2].text = "Gui Animations: " + state

    def toggleExitAnimation(self, toggle = True):
        if toggle:
            self.menuHandler.main.config.config["ExitAnimation"] = not self.menuHandler.main.config.config["ExitAnimation"]
        state = "off"
        if self.menuHandler.main.config.config["ExitAnimation"]:
            state = "on"
        self.createdGuis[5].text = "Exit Animation: " + state        

    def create(self):
        super().create()
        self.toggleGuiComeIn(False)
        self.toggleGuiAnimations(False)
        self.toggleLevelTransitions(False)
        self.toggleBlockAnimations(False)
        self.toggleExitAnimation(False)
