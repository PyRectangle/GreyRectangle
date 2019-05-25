from KeyTranslate import KeyTranslate
from Frame.gui.Button import Button
from Frame.gui.Slider import Slider
from Constants import *
from Menu import Menu


class VideoSettings(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.keyTranslate = KeyTranslate()
        self.menuHandler = menuHandler
        self.addGui(Button, (menuHandler.show, (menuHandler.settings), 60, 940, 300, 100, "Back", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True,
                             30, 30, 0.1, True, [1, 0], None, SOUNDS, menuHandler.window))
        self.addGui(Slider, (menuHandler.getFPSLimit, (200, 200, 200), 60, 80, 800, 120, "FPS Limit", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT,
                             True, 30, 30, 0.1, True, [0, 1], None, SOUNDS, menuHandler.window, 80))
        self.addGui(Button, (self.toggleBusyLoop, (), 60, 240, 800, 120, "Use Busy Loop: on", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30,
                             0.1, True, [1, 1], None, SOUNDS, menuHandler.window, 80))
        self.addGui(Button, (self.toggleFullscreen, (), 60, 400, 800, 120, "Fullscreen: on", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30,
                             0.1, True, [1, 1], None, SOUNDS, menuHandler.window, 80))
        self.addGui(Button, (self.toggleSDL2, (), 60, 560, 800, 120, "Use SDL2: on", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30, 30, 0.1,
                             True, [1, 1], None, SOUNDS, menuHandler.window, 80))
        self.addGui(Button, (menuHandler.show, (19), 60, 720, 800, 120, "Animation Settings", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), FONT, True, 30,
                             30, 0.1, True, [1, 1], None, SOUNDS, menuHandler.window, 80))
    
    def update(self):
        super().update()
        if self.menuHandler.main.config.config["Fullscreen"] != self.menuHandler.window.fullscreen:
            self.toggleFullscreen(False)
        if len(self.createdGuis) == len(self.guis):
            self.toggleSDL2(False)

    def toggleSDL2(self, toggle = True):
        if toggle:
            if self.keyTranslate.installed:
                self.menuHandler.main.warningHandler.createWarning("This option requires a restart to take effect !", 1.5)
                self.menuHandler.main.config.config["SDL2"] = not self.menuHandler.main.config.config["SDL2"]
            else:
                if not self.keyTranslate.installedSdl1:
                    self.menuHandler.main.warningHandler.createWarning("This option requires pygame using SDL-1 to be installed !", 2)
                else:
                    self.menuHandler.main.warningHandler.createWarning("This option requires pygame_sdl2 to be installed !", 2)
        state = "off"
        if self.menuHandler.main.config.config["SDL2"]:
            state = "on"
        self.createdGuis[4].text = "Use SDL2: " + state
    
    def toggleFullscreen(self, toggle = True):
        if toggle:
            self.menuHandler.window.toggleFullscreen()
        self.menuHandler.main.config.config["Fullscreen"] = self.menuHandler.window.fullscreen
        state = "off"
        if self.menuHandler.window.fullscreen:
            state = "on"
        self.createdGuis[3].text = "Fullscreen: " + state
    
    def toggleBusyLoop(self, toggle = True):
        if toggle:
            self.menuHandler.window.useBusyLoop = not self.menuHandler.window.useBusyLoop
        self.menuHandler.main.config.config["UseBusyLoop"] = self.menuHandler.window.useBusyLoop
        state = "off"
        if self.menuHandler.window.useBusyLoop:
            state = "on"
        self.createdGuis[2].text = "Use Busy Loop: " + state

    def create(self):
        super().create()
        limit = self.menuHandler.main.window.fpsLimit
        if self.menuHandler.main.window.fpsLimit == 0:
            limit = 100
        percent = limit / 0.9 - 11
        self.createdGuis[1].sliderText = str(self.createdGuis[1].function(percent))
        self.createdGuis[1].pos = percent
        self.toggleBusyLoop(False)
        self.toggleFullscreen(False)
