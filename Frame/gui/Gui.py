from Frame.baseFunctions import *
import pygame


class Gui:
    def __init__(self, x, y, width, height, text, color, frameColor, selectColor, textColor, fontFile, antialias,
                 pressDifference, steps, sec, comeIn, direction, startPos, sounds, window):
        output("Gui: Creating a gui with the following args: (x: " + str(x) + ", y: " + str(y) + ", width: " + str(width) + ", height: " + str(height) +
               ", ...) named " + text, "debug")
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.frameColor = frameColor
        self.selectColor = selectColor
        self.textColor = textColor
        self.fontFile = fontFile
        self.antialias = antialias
        self.sounds = []
        for sound in sounds:
            if sound != None:
                self.sounds.append(pygame.mixer.Sound(sound))
        self.pressed = False
        self.wasPressedGui = False
        self.mouseTouchesButton = False
        self.wasTouched = False
        self.sec = sec
        self.pressDifference = pressDifference
        self.aspectRatio = self.height / self.width
        self.startCoords = [self.x, self.y, self.width, self.height]
        self.pressCoords = [self.x - self.pressDifference, self.y - self.pressDifference * self.aspectRatio,
                            self.width + self.pressDifference * 2,
                            self.height + self.pressDifference * self.aspectRatio * 2]
        self.last = -1
        self.step = 0
        self.steps = steps
        self.xStep = (self.startCoords[0] - self.pressCoords[0]) / self.steps
        self.yStep = (self.startCoords[1] - self.pressCoords[1]) / self.steps
        self.window = window
        self.renderObj = window.render
        self.lastInOneTick = 0
        self.coords = [self.x, self.y, self.width, self.height]
        self.comeIn = comeIn
        self.rightCoords = True
        self.remove = False
        self.keyOnGui = False
        self.touchable = True
        self.startPos = startPos
        output("Gui: Getting the start position...", "debug")
        if self.comeIn:
            self.rightCoords = False
            self.goTo = [self.x, self.y]
            self.direction = direction
            self.inScreen = True
            if self.startPos == None:
                while self.inScreen:
                    self.x -= self.direction[0]
                    self.y -= self.direction[1]
                    self.inScreen = self.x <= self.window.surface.get_width() and self.x + self.width >= 0 and self.y <= self.window.surface.get_height() and \
                                    self.y + self.height >= 0
            else:
                self.x, self.y = self.startPos
        self.window.guiHandler.addGui(self)
    
    def getTouch(self):
        output("Gui: Looking for the mouse touching this gui...", "complete")
        self.mouseTouchesButton = self.window.mousePos[0] <= self.x + self.width and \
                                  self.window.mousePos[0] >= self.x and \
                                  self.window.mousePos[1] <= self.y + self.height and \
                                  self.window.mousePos[1] >= self.y
        output("Gui: Succes: " + str(self.mouseTouchesButton), "complete")

    def update(self):
        output("Gui: Updating " + self.text + "...", "complete")
        if self.comeIn and not self.rightCoords:
            if self.remove and self.inScreen:
                output("Gui: Moving out of the screen...", "complete")
                self.x -= self.direction[0] * self.window.dt
                self.y -= self.direction[1] * self.window.dt
                self.inScreen = self.x <= self.window.surface.get_width() and self.x + self.width >= 0 and self.y <= self.window.surface.get_height() and \
                                self.y + self.height >= 0
            elif not self.remove:
                output("Gui: Moving in the screen...", "complete")
                self.inScreen = True
                self.x += self.direction[0] * self.window.dt
                self.y += self.direction[1] * self.window.dt
                count = 0
                if self.x >= self.goTo[0] and self.direction[0] >= 0 or self.x <= self.goTo[0] and self.direction[0] < 0:
                    self.x = self.goTo[0]
                    count += 1
                if self.y >= self.goTo[1] and self.direction[1] >= 0 or self.y <= self.goTo[1] and self.direction[1] < 0:
                    self.y = self.goTo[1]
                    count += 1
                if count == 2:
                    self.rightCoords = True
            self.coords = [self.x, self.y, self.width, self.height]
        if self.touchable:
            if self.keyOnGui:
                self.mouseTouchesButton = True
            else:
                self.getTouch()
        else:
            self.mouseTouchesButton = False
        if self.window.fps <= 0:
            inOneTick = 0
        else:
            inOneTick = self.steps / self.sec / self.window.fps
        output("Gui: Setting size...", "complete")
        inOneTick += self.lastInOneTick
        self.lastInOneTick = inOneTick - int(inOneTick)
        for i in range(int(inOneTick)):
            if self.mouseTouchesButton:
                self.setSize(True)
            else:
                self.setSize(False)
        if not self.wasTouched and self.mouseTouchesButton:
            if self.sounds != None:
                output("Gui: Playing gui hover sound...", "debug")
                self.sounds[0].play()
        self.wasTouched = self.mouseTouchesButton
        self.pressedKey = self.mouseTouchesButton and self.window.keys[self.window.guiPresser]
        self.getTouch()
        self.pressedMouse = self.mouseTouchesButton and self.window.mousePressed != (0, 0, 0)
        self.pressed = self.pressedKey or self.pressedMouse
        if not self.wasPressedGui and self.pressed:
            if self.sounds[1] != None:
                output("Gui: Playing gui click sound...", "debug")
                self.sounds[1].play()
        output("Gui: Is pressed: " + str(self.pressed), "complete")
        self.wasPressedGui = self.pressed

    def render(self):
        output("Gui: Rendering...", "complete")
        points = [self.coords[0:2], [self.coords[0] + self.coords[2], self.coords[1]], [self.coords[0] + self.coords[2], self.coords[1] + self.coords[3]],
                  [self.coords[0], self.coords[1] + self.coords[3]]]
        if self.mouseTouchesButton and self.rightCoords and not self.window.guiHandler.keyActive or self.keyOnGui and self.rightCoords:
            pygame.draw.polygon(self.window.surface, self.selectColor, points)
        else:
            pygame.draw.polygon(self.window.surface, self.color, points)
        self.renderObj.text(self.fontFile, int(self.height), self.text, self.antialias, self.textColor, None,
                            self.window.surface, width = self.width, height = self.height, addX = self.x, addY = self.y)
        pygame.draw.lines(self.window.surface, self.frameColor, 4, [[self.x, self.y], [self.x + self.width - 1, self.y],
                                                                    [self.x + self.width - 1, self.y + self.height - 1], [self.x, self.y + self.height - 1],
                                                                    [self.x, self.y]], 1)

    def resize(self, difference):
        output("Gui: Resizing...", "complete")
        if self.last != difference:
            self.step = 0
        self.last = difference
        self.step += 1
        if self.step <= self.steps:
            self.x += self.xStep * difference
            self.y += self.yStep * difference
            self.height -= self.yStep * difference * 2
            self.width -= self.xStep * difference * 2
            self.coords = [self.x, self.y, self.width, self.height]

    def setSize(self, pos):
        output("Gui: Setting size to something smaller/bigger: " + str(pos) + "...", "complete")
        if self.rightCoords:
            if pos:
                self.resize(-1)
                if self.x < self.pressCoords[0]:
                    self.resize(1)
            else:
                self.resize(1)
                if self.x > self.startCoords[0]:
                    self.resize(-1)
