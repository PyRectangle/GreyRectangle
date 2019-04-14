from Frame.baseFunctions import *
from Frame.gui.Gui import Gui
import pyperclip
import pygame


class LineEdit(Gui):
    def __init__(self, lineEditColor, lineSelectColor, charLimit, *args, **kwargs):
        super().__init__(*args, **kwargs)
        output("LineEdit: Creating " + self.text + " lineEdit...", "debug")
        self.backX = self.startCoords[0]
        self.enterText = self.text
        self.text = ""
        self.charLimit = charLimit
        self.lineEditColor = lineEditColor
        self.lineSelectColor = lineSelectColor
        self.wasPressed = False
        self.pos = 0
        self.posLeft = False
        self.posRight = False
        self.delLeftCount = 0
        self.delRightCount = 0
        self.firstDelLeft = True
        self.firstDelRight = True
        self.writable = False
        self.rightPosPressCount = 0
        self.leftPosPressCount = 0
        self.startCount = 0
        self.started = False
        self.waitToEnter = self.window.fps * 10
        self.selectStart = None
        self.textPixelPos = 0
        self.selectWasStarted = False

    def delRight(self, textList):
        try:
            if self.pos >= 0:
                del textList[self.pos]
        except IndexError:
            pass
        return textList

    def delLeft(self, textList):
        try:
            if self.pos - 1 >= 0:
                del textList[self.pos - 1]
                self.moveLeft()
        except IndexError:
            pass
        return textList
    
    def moveRight(self):
        self.pos += 1
        if self.pos > len(self.text) + 1:
            self.pos = len(self.text) + 1
    
    def moveLeft(self):
        self.pos -= 1
        if self.pos < 0:
            self.pos = 0
    
    def getLenght(self, text):
        return list(pygame.font.Font(self.fontFile, self.textSize).size(text))[0]

    def getAmount(self, number):
        if number < 0:
            number = -number
        return number

    def getDifferrence(self, one, two):
        return self.getAmount(self.getAmount(one) - self.getAmount(two))

    def update(self):
        super().update()
        if self.writable:
            self.pressed = False
        output("LineEdit: Setting it on writable if it is pressed...", "complete")
        self.waitToEnter += self.window.dt / 100
        if self.waitToEnter >= 1:
            self.waitToEnter = 1
        if self.pressed and not self.wasPressed and self.rightCoords and self.waitToEnter >= 1:
            for gui in self.window.guiHandler.allGuis:
                try:
                    gui.writable = False
                except AttributeError:
                    pass
            self.writable = True
            self.startCount = 0
            self.started = not self.pressedKey
            self.selectStart = None
        if self.pressedMouse:
            pixelPos = self.window.mousePos[0] - self.backX + self.textPixelPos
            pixelCheckPos = 0
            nearest = 0
            count = 0
            text = ""
            for char in self.text:
                text += char
                pixelCheckPos = self.getLenght(text)
                if self.getDifferrence(pixelCheckPos, pixelPos) < self.getDifferrence(nearest, pixelPos):
                    nearest = pixelCheckPos
                if pixelCheckPos > pixelPos:
                    self.pos = count
                    break
                if pixelPos > pixelCheckPos:
                    self.pos = len(self.text)
                count += 1
        if self.window.keys[self.window.guiEscape]:
            self.writable = False
        self.wasPressed = self.pressed
        if self.writable:
            movedRight = False
            moved = False
            deleted = False
            if not self.started:
                self.startCount += self.window.dt / 100
                if self.startCount >= 1:
                    self.started = True
            textList = list(self.text)
            lastTextList = textList.copy()
            lastPos = self.pos
            if self.window.keys[self.window.guiMove[0]]:
                self.leftPosPressCount += self.window.dt / 100
                if self.leftPosPressCount >= 1:
                    self.leftPosPressCount -= 1
                    self.posLeft = False
                if not self.posLeft:
                    moved = True
                    movedRight = False
                    self.moveLeft()
                    self.posLeft = True
            else:
                self.posLeft = False
                self.leftPosPressCount = 0
            if self.window.keys[self.window.guiMove[1]]:
                self.rightPosPressCount += self.window.dt / 100
                if self.rightPosPressCount >= 1:
                    self.rightPosPressCount -= 1
                    self.posRight = False
                if not self.posRight:
                    moved = True
                    movedRight = True
                    self.moveRight()
                    self.posRight = True
            else:
                self.posRight = False
                self.rightPosPressCount = 0
            if self.window.keys[8]:
                if self.firstDelLeft:
                    self.firstDelLeft = False
                    deleted = True
                    if self.selectStart == None:
                        textList = self.delLeft(textList)
                else:
                    self.delLeftCount += self.window.dt / 100
                    while self.delLeftCount >= 1:
                        self.delLeftCount -= 1
                        deleted = True
                        if self.selectStart == None:
                            textList = self.delLeft(textList)
            else:
                self.firstDelLeft = True
                self.delLeftCount = 0
            if self.window.keys[127]:
                if self.firstDelRight:
                    self.firstDelRight = False
                    deleted = True
                    if self.selectStart == None:
                        textList = self.delRight(textList)
                else:
                    self.delRightCount += self.window.dt / 100
                    while self.delRightCount >= 1:
                        self.delRightCount -= 1
                        deleted = True
                        if self.selectStart == None:
                            textList = self.delRight(textList)
            else:
                self.firstDelRight = True
                self.delRightCount = 0
            if self.window.keys[304] or self.window.keys[303] or self.pressedMouse:
                if not self.selectWasStarted:
                    self.selectWasStarted = True
                    self.selectStart = self.pos
            elif moved:
                if self.selectStart != None:
                    if self.pos > self.selectStart and not movedRight:
                        self.pos = self.selectStart
                    if self.pos < self.selectStart and movedRight:
                        self.pos = self.selectStart
                self.selectWasStarted = False
                self.selectStart = None
            elif deleted:
                textList = self.deleteSelection(textList)
            elif not self.pressedMouse and not self.window.keys[304] or not self.window.keys[303]:
                self.selectWasStarted = False
            if self.window.char != "":
                if ord(self.window.char) == 8 or ord(self.window.char) == 127 or ord(self.window.char) == self.window.guiChanger:
                    pass
                elif ord(self.window.char) == 3:
                    pyperclip.copy(self.getClip())
                elif ord(self.window.char) == 22:
                    clip = pyperclip.paste()
                    textList = self.deleteSelection(textList)
                    for i in clip:
                        if textList == []:
                            textList = [i]
                        else:
                            textList.insert(self.pos, i)
                        self.pos += 1
                        if self.pos > len(textList):
                            self.pos = len(textList)
                elif ord(self.window.char) == 13:
                    if self.started:
                        self.writable = False
                        self.waitToEnter = 0
                else:
                    textList = self.deleteSelection(textList)
                    if textList == []:
                        textList = [self.window.char]
                    else:
                        textList.insert(self.pos, self.window.char)
                    self.moveRight()
            if len(textList) > self.charLimit:
                textList = lastTextList
                self.pos = lastPos
            self.text = ""
            for char in textList:
                self.text += char

    def getClip(self):
        clip = ""
        if self.selectStart != None:
            if self.selectStart < self.pos:
                clip = self.text[self.selectStart:self.pos]
            elif self.selectStart > self.pos:
                clip = self.text[self.pos:self.selectStart]
        return clip

    def deleteSelection(self, textList):
        if self.selectStart != None:
            if self.selectStart < self.pos:
                del textList[self.selectStart:self.pos]
            elif self.selectStart > self.pos:
                del textList[self.pos:self.selectStart]
        self.selectWasStarted = False
        self.selectStart = None
        return textList

    def renderLineEdit(self):
        try:
            textSurface = self.renderObj.text(self.fontFile, self.textSize, self.text, self.antialias, self.textColor, None, None, None, None, False)
            shortText = self.text
        except pygame.error:
            count = 1
            shortText = self.text[self.pos - count:self.pos + count]
            while self.getLenght(shortText) < self.width * 2:
                count += 1
                shortText = self.text[self.pos - count:self.pos + count]
            textSurface = self.renderObj.text(self.fontFile, self.textSize, shortText, self.antialias, self.textColor, None, None, None, None, False)
        textRect = textSurface.get_rect()
        textPosList = list(self.text)
        for i in range(len(self.text) - self.pos):
            del textPosList[-1]
        textPosString = ""
        for char in textPosList:
            textPosString += char
        textPixelPos = list(pygame.font.Font(self.fontFile, self.textSize).size(textPosString))[0]
        while self.textPixelPos + self.width - self.width / 10 < textPixelPos:
            self.textPixelPos += 1
        while self.textPixelPos + self.width / 10 > textPixelPos:
            self.textPixelPos -= 1
        textPos = self.textPixelPos
        textPixelPos -= textPos
        textRect.width = self.width
        try:
            sub = self.getLenght(self.text[0:self.pos - count - 1])
        except UnboundLocalError:
            sub = 0
        textRect.x += textPos + (self.x - self.backX) - sub
        if self.writable and self.selectStart != None:
            points = [self.getLenght(self.text[0:self.selectStart]) + self.backX - textPos, self.getLenght(self.text[0:self.pos]) + self.backX - textPos]
            for i in range(len(points)):
                if points[i] <= self.x:
                    points[i] = self.x + 1
                if points[i] >= self.x + self.width:
                    points[i] = self.x + self.width - 1
            pygame.draw.polygon(self.window.surface, self.lineSelectColor, [[points[0], self.y + 2], [points[1], self.y + 2], [points[1], self.y + self.height - 2],
                                                                            [points[0], self.y + self.height - 2]])
        self.window.surface.blit(textSurface, (self.x, self.y + self.height / 2 - textSurface.get_height() / 2), textRect)
        if self.writable:
            textPixelPos += self.backX
            width = self.width / 200
            height = self.height - 4
            y = (self.height - height) / 2
            points = [[textPixelPos - width / 2, self.y + y], [textPixelPos - width / 2, self.y + y + height], [textPixelPos + width / 2, self.y + y + height],
                      [textPixelPos + width / 2, self.y + y]]
            pygame.draw.polygon(self.window.surface, self.textColor, points)

    def delete(self):
        self.writable = False
        super().delete()
