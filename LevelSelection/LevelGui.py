from LevelSelection.Graphic import Graphic
from Frame.Render import Render
from Constants import *
import math


class LevelGui:
    def __init__(self, level, levels, startDegrees, first, window, levelGuiHandler, guiId, main):
        self.main = main
        self.level = levels[level]
        self.levelCount = level
        self.levels = levels
        self.first = first
        self.window = window
        self.mouseTouch = False
        self.x = 0
        self.y = 0
        self.guiId = guiId
        self.levelGuiHandler = levelGuiHandler
        self.degrees = startDegrees
        self.goToDegrees = startDegrees
        self.center = [540, 30]
        self.distance = 540
        self.scrollCount = 0
        self.touchCount = 0
        self.secCount = 0
        self.near = False
        self.levelIndex = self.levelCount
        self.wasSelected = False
        self.pressed = False
        self.renderObj = Render(self.window)
        size = self.renderObj.getTextSizeForWidth(self.level.data.description, 40, 390, FONT)
        self.graphics = [Graphic(LEVEL_GUI_COLOR, [[1440, 360], [975, 360], [900, 510], [975, 660], [1440, 660], [1440, 610], [1000, 610], [950, 510], [1000, 410],
                                              [1440, 410]], [800, 0], 1, window),
                         Graphic((120, 120, 120), [[1440, 410], [1000, 410], [950, 510], [1000, 610], [1440, 610]], [800, 0], 1, window,
                                 (FONT, self.renderObj.getTextSizeForWidth(self.level.name, 140, 440, FONT), self.level.name, True, (0, 0, 0), None), 1000, 420),
                         Graphic((120, 120, 120), [[1440, 410], [1440, 410], [1440, 410]], [800, 0], 1, window, (FONT, size, self.level.data.description, True,
                                                                                                                 (0, 0, 0), None), 1050, 565)]

    def rotate(self):
        radians = math.radians(self.degrees)
        self.x = self.center[0] - math.sin(radians) * self.distance
        self.y = self.center[1] - math.cos(radians) * self.distance
    
    def toggle(self):
        for graphic in self.graphics:
            graphic.toggle()
    
    def getLevelIndex(self):
        return self.levelCount
    
    def setLevelIndex(self, index):
        if not index < 0:
            try:
                self.levelCount = index
                self.level = self.levels[self.levelCount]
                self.notRender = False
                try:
                    self.graphics[1].text = (FONT, 140, self.level.name, True, (0, 0, 0), None)
                    self.graphics[2].text = (FONT, 40, self.level.data.description, True, (0, 0, 0), None)
                except AttributeError:
                    pass
            except IndexError:
                self.notRender = True
        else:
            self.notRender = True
    
    def update(self):
        mousePos = self.window.mousePos
        hitCoords = [[self.x + 900, self.y + 360], [self.x + 1440, self.y + 660]]
        speed = self.window.dt / 4
        round = 0.5
        if self.degrees < 0:
            round = -0.5
        elif self.degrees > 0:
            round = 0.5
        self.near = int(self.degrees / 45 + round) * 45 == self.goToDegrees
        if self.goToDegrees > self.degrees:
            self.degrees += speed
            if self.degrees > self.goToDegrees:
                self.degrees = self.goToDegrees
        if self.goToDegrees < self.degrees:
            self.degrees -= speed
            if self.goToDegrees > self.degrees:
                self.degrees = self.goToDegrees
        self.rotate()
        self.secCount += 1
        fps = self.window.fps / LEVEL_GUI_SEC_DIVIDER
        if self.secCount >= fps:
            self.secCount = 0
            multiplier = 1
            if fps < 1:
                multiplier = 1 / fps
            if self.mouseTouch:
                self.touchCount += 1 * multiplier
            else:
                self.touchCount -= 1 * multiplier
                if self.touchCount <= 0:
                    self.touchCount = 0
        if self.touchCount > 45:
            self.touchCount = 45
        self.x -= self.touchCount
        for graphic in self.graphics:
            graphic.x = self.x
            graphic.y = self.y
            graphic.update()
        self.position = self.goToDegrees / 45
        self.mouseTouch = mousePos[0] > hitCoords[0][0] and mousePos[1] > hitCoords[0][1] and mousePos[1] < hitCoords[1][1] and self.degrees > 0 and \
                          self.degrees < 180 and not self.notRender
        self.selected = self.mouseTouch and self.window.mousePressed != (0, 0, 0)
        if self.selected and not self.wasSelected:
            self.wasSelected = True
            if self.pressed:
                self.main.levelPreview.pressLevel(None)
                self.levelGuiHandler.selected = None
            else:
                self.main.levelPreview.pressLevel(self.level)
                self.levelGuiHandler.deselect()
                self.levelGuiHandler.selected = self.guiId
        elif self.window.mousePressed == (0, 0, 0):
            self.wasSelected = False
    
    def render(self):
        if not self.notRender:
            self.graphics[0].render()
            self.graphics[1].render()
            self.graphics[2].render()
    
    levelIndex = property(getLevelIndex, setLevelIndex)
