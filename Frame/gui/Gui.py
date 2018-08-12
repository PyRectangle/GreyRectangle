import pygame


class Gui:
    def __init__(self, x, y, width, height, text, color, frameColor, selectColor, textColor, fontFile, antialias,
                 pressDifference, steps, sec, comeIn, direction, window):
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
        self.pressed = False
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
        self.surface = pygame.Surface((self.width, self.height))
        self.comeIn = comeIn
        self.rightCoords = True
        self.remove = False
        if self.comeIn:
            self.rightCoords = False
            self.goTo = [self.x, self.y]
            self.direction = direction
            self.inScreen = True
            while self.inScreen:
                self.x -= self.direction[0]
                self.y -= self.direction[1]
                self.inScreen = self.x <= self.window.surface.get_width() and self.x + self.width >= 0 and self.y <= self.window.surface.get_height() and \
                                self.y + self.height >= 0
        self.updateSurface()

    def update(self):
        if self.comeIn and not self.rightCoords:
            if self.remove and self.inScreen:
                self.x -= self.direction[0] * self.window.dt
                self.y -= self.direction[1] * self.window.dt
                self.inScreen = self.x <= self.window.surface.get_width() and self.x + self.width >= 0 and self.y <= self.window.surface.get_height() and \
                                self.y + self.height >= 0
            elif not self.remove:
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
        self.mouseTouchesButton = self.window.mousePos[0] <= self.x + self.width and \
                                  self.window.mousePos[0] >= self.x and \
                                  self.window.mousePos[1] <= self.y + self.height and \
                                  self.window.mousePos[1] >= self.y
        if self.window.fps <= 0:
            inOneTick = 0
        else:
            inOneTick = self.steps / self.sec / self.window.fps
        inOneTick += self.lastInOneTick
        self.lastInOneTick = inOneTick - int(inOneTick)
        for i in range(int(inOneTick)):
            if self.mouseTouchesButton:
                self.setSize(True)
            else:
                self.setSize(False)
        if self.wasTouched != self.mouseTouchesButton:
            self.updateSurface()
        self.wasTouched = self.mouseTouchesButton
        self.pressed = self.mouseTouchesButton and self.window.mousePressed != (0, 0, 0)

    def render(self):
        self.window.surface.blit(self.surface, (self.x, self.y))

    def resize(self, difference):
        if self.last != difference:
            self.step = 0
        self.last = difference
        self.step += 1
        if self.step <= self.steps:
            self.x += self.xStep * difference
            self.y += self.yStep * difference
            self.height -= self.yStep * difference * 2
            self.width -= self.xStep * difference * 2
            self.surface = pygame.Surface((self.width, self.height))

    def setSize(self, pos):
        if self.rightCoords:
            if pos:
                self.resize(-1)
                if self.x < self.pressCoords[0]:
                    self.resize(1)
            else:
                self.resize(1)
                if self.x > self.startCoords[0]:
                    self.resize(-1)
            self.updateSurface()

    def updateSurface(self):
        if self.mouseTouchesButton and self.rightCoords:
            self.surface.fill(self.selectColor)
        else:
            self.surface.fill(self.color)
        self.renderObj.text(self.fontFile, int(self.height), self.text, self.antialias, self.textColor, None,
                            self.surface, None, None)
        pygame.draw.lines(self.surface, self.frameColor, 4, [[0, 0], [self.width - 1, 0],
                                                             [self.width - 1, self.height - 1], [0, self.height - 1],
                                                             [0, 0]], 1)
