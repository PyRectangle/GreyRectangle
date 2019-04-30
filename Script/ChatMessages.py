from collections import OrderedDict
from pygameImporter import pygame
from Constants import *


class ChatMessages:
    def __init__(self):
        self.messages = OrderedDict()
        self.scroll = 0
        self.count = 0
    
    def clearChat(self):
        self.messages = OrderedDict()
        self.scroll = 0
        self.count = 0
    
    def postMessage(self, text):
        if len(text) > CHAT_MESSAGE_MAX_CHARS:
            raise Exception("The message is too big.")
        used = False
        textUnused = []
        while list(pygame.font.Font(FONT, 56).size(text))[0] > 1416:
            used = True
            textList = []
            for i in text:
                textList += i
            textUnused.insert(0, textList[-1])
            del textList[-1]
            text = ""
            for char in textList:
                text += char
        self.createMessage(text)
        if used:
            text = ""
            for i in textUnused:
                text += i
            self.postMessage(text)

    def createMessage(self, text):
        while len(self.messages) > CHAT_MAX_MESSAGES:
            del self.messages[list(self.messages.keys())[-1]]
        self.count += 1
        self.messages[chr(self.count) + text] = CHAT_MESSAGE_DURATION
    
    def update(self, dt, opened, main):
        if opened:
            self.scroll -= main.window.mouseScroll
            if self.scroll < 0:
                self.scroll = 0
            if self.scroll > len(self.messages) - 14:
                self.scroll = len(self.messages) - 14
        else:
            self.scroll = 0
        for message in self.messages:
            self.messages[message] -= dt / 1000
            if self.messages[message] < 0:
                self.messages[message] = 0
    
    def render(self, renderObj, opened):
        y = 1010
        count = self.scroll
        for message in reversed(self.messages):
            if count > 0:
                count -= 1
                continue
            y -= 60
            if y > 500 or opened and y > -60:
                if opened:
                    alpha = 255
                else:
                    if self.messages[message] <= CHAT_MESSAGE_FADEOUT_DURATION:
                        alpha = 255 * (self.messages[message] / CHAT_MESSAGE_FADEOUT_DURATION)
                    else:
                        alpha = 255
                surface = pygame.Surface((1420, 60))
                surface.fill((0, 0, 0))
                surface.set_alpha(120 * (alpha / 255))
                renderObj.window.surface.blit(surface, (10, y))
                renderObj.text(FONT, 56, message[1:], True, (255, 255, 255), None, renderObj.window.surface, x = 12, y = y + 2, blit = True, alpha = alpha)
