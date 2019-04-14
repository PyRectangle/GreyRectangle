from LevelSelection.LevelGui import LevelGui
from Constants import *


class LevelGuiHandler:
    def __init__(self, levels, main):
        self.levelGuis = []
        self.main = main
        self.window = main.window
        count = -1
        first = True
        guiId = 0
        self.pos = 0
        self.levels = levels
        self.selected = None
        self.lastLevelPos = 0
        self.newSelect = False
        self.lastSelected = None
        self.canChange = True
        if len(self.levels) < 5:
            self.pos = 90
            self.levelPos = 0
            forList = (0, len(self.levels), 1)
        else:
            self.levelPos = -2
            forList = (-1, 4, 1)
        for i in range(*forList):
            try:
                count += 1
                self.levelGuis.append(LevelGui(count, levels, (i + 3) * 45, first, self.window, self, guiId, main))
                first = False
                guiId += 1
            except IndexError:
                pass
    
    def updateText(self):
        for gui in self.levelGuis:
            gui.updateText()
        
    def deselect(self):
        self.selected = None
        for gui in self.levelGuis:
            gui.pressed = False
        
    def toggle(self):
        self.selected = None
        for gui in self.levelGuis:
            gui.toggle()
    
    def update(self):
        if len(self.levels) > 0:
            movedKey = False
            selected = self.selected
            if self.canChange and not self.main.levelSelection.toggleClosed:
                if self.window.key == self.main.config.config["Controls"]["goRight"]:
                    movedKey = True
                    if self.selected == None:
                        self.selected = 2
                        if len(self.levels) < 5:
                            self.selected = 0
                    else:
                        self.selected += 1
                if self.window.key == self.main.config.config["Controls"]["goLeft"]:
                    movedKey = True
                    if self.selected == None:
                        self.selected = 2
                        if len(self.levels) < 5:
                            self.selected = 0
                    else:
                        self.selected -= 1
            if self.selected != None:
                try:
                    if self.levelGuis[self.selected].notRender:
                        self.selected = selected
                except IndexError:
                    self.selected = selected
            if self.levelGuis[0].near:
                if self.window.keys[self.main.config.config["Controls"]["goDown"]]:
                    self.pos -= 45
                if self.window.keys[self.main.config.config["Controls"]["goUp"]]:
                    self.pos += 45
                self.pos += 45 * self.window.mouseScroll
                if not len(self.levels) < 5:
                    if self.levelPos + -self.pos / 45 == -3 and self.pos > 0:
                        self.pos = 0
                    if self.pos < 0 and self.levelGuis[-1].goToDegrees == 180 and self.levelGuis[-2].notRender:
                        self.pos = 0
                else:
                    if self.pos > 90:
                        self.pos = 90
                    endPos = 90 - 45 * len(self.levels) + 45
                    if self.pos < endPos:
                        self.pos = endPos
            if not len(self.levels) < 5:
                move = self.pos == -45
                if self.pos == -45:
                    if self.selected != None:
                        self.selected -= 1
                    self.levelPos += 1
                    self.pos = 0
                    for gui in self.levelGuis:
                        gui.goToDegrees += 45
                        gui.degrees += 45
                if self.pos == 45:
                    if self.selected != None:
                        self.selected += 1
                    self.levelPos -= 1
                    self.pos = 0
                    for gui in self.levelGuis:
                        gui.goToDegrees -= 45
                        gui.degrees -= 45
            if self.selected != None and movedKey:
                try:
                    self.levelGuis[self.selected]
                except IndexError:
                    self.selected = None
                if self.selected != None:
                    if self.selected < 0:
                        self.selected = None
                        if len(self.levels) < 5:
                            self.selected = 0
                    if self.selected != None:
                        if movedKey and not self.selected == self.lastSelected:
                            self.main.levelPreview.pressLevel(self.levelGuis[self.selected].level)
                            self.lastSelected = self.selected
            count = -1
            for gui in self.levelGuis:
                count += 1
                self.levelGuis[count].pressed = False
                self.levelGuis[count].graphics[0].color = LEVEL_GUI_COLOR
                if self.selected != None:
                    if self.selected >= 0:
                        try:
                            self.levelGuis[self.selected].pressed = True
                            self.levelGuis[self.selected].graphics[0].color = LEVEL_GUI_SELECT_COLOR
                        except IndexError:
                            pass
                if self.levelPos != self.lastLevelPos:
                    gui.levelIndex = self.levelPos + count
                gui.goToDegrees = self.pos + count * 45
                gui.update()
            self.lastLevelPos = self.levelPos

    def render(self):
        for gui in self.levelGuis:
            gui.render()
