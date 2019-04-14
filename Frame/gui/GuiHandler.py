from Frame.gui.ClickAnim import ClickAnim
from Frame.baseFunctions import *


class GuiHandler:
    def __init__(self, window):
        output("GuiHandler: Creating gui handler...", "debug")
        self.allGuis = []
        self.keyActive = False
        self.selectedGui = 0
        self.window = window
        self.wasPressed = False
        self.clickAnim = None
        self.volume = 1
    
    def createClickAnim(self, button):
        output("GuiHandler: Creating click animation for " + button.text + "...", "debug")
        self.clickAnim = ClickAnim(button)
    
    def addGui(self, gui):
        output("GuiHandler: Adding gui to gui handler...", "debug")
        self.allGuis.append(gui)
    
    def update(self):
        output("GuiHandler: Looking for guis with right position...", "complete")
        self.guis = []
        for gui in self.allGuis:
            if gui.remove and gui.inScreen:
                self.keyActive = False
            if not gui.remove and gui.rightCoords:
                self.guis.append(gui)
        count = 0
        for i in range(len(self.allGuis)):
            try:
                if self.allGuis[i].remove and not self.allGuis[i].inScreen:
                    del self.allGuis[i - count]
                    count += 1
            except IndexError:
                pass
        output("GuiHandler: Looking for gui changer key to press...", "complete")
        if self.window.keys[self.window.guiChanger] and not self.wasPressed:
            output("GuiHandler: Changing gui...", "debug")
            self.wasPressed = True
            if self.keyActive == False:
                self.selectedGui = -1
            self.keyActive = True
            self.selectedGui += 1
            if self.selectedGui >= len(self.guis):
                self.selectedGui = 0
        elif not self.window.keys[self.window.guiChanger]:
            self.wasPressed = False
        for gui in self.guis:
            gui.keyOnGui = False
            gui.touchable = True
        if self.keyActive:
            try:
                self.guis[self.selectedGui].keyOnGui = True
            except IndexError:
                pass
            for gui in self.guis:
                gui.getTouch()
                if gui.mouseTouchesButton and not gui.keyOnGui:
                    gui.touchable = False
        if self.clickAnim != None:
            self.clickAnim.update()
            if self.clickAnim != None:
                if self.clickAnim.finished:
                    self.clickAnim = None
        for gui in self.allGuis:
            gui.setVolume(self.volume)
