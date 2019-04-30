from pygameImporter import pygame


class Graphic:
    def __init__(self, color, vertices, point, speed, window, text = None, textX = None, textY = None):
        self.vertices = vertices
        self.firstPoint = point.copy()
        self.color = color
        self.point = point
        self.speed = speed
        self.isChanging = False
        self.isOpen = False
        self.isClosed = True
        self.text = text
        self.textX = textX
        self.textY = textY
        self.window = window
        self.x = 0
        self.y = 0
        self.textAlpha = 255
        self.renderVertices = []

    def toggle(self):
        if self.isChanging:
            if self.isOpen:
                self.finishedClose()
            elif self.isClosed:
                self.finishedOpen()
        self.isChanging = True
    
    def finishedOpen(self):
        self.isChanging = False
        self.isOpen = True
        self.isClosed = False

    def finishedClose(self):
        self.isChanging = False
        self.isOpen = False
        self.isClosed = True
        
    def update(self):
        if self.isChanging:
            if self.isClosed:
                count = 0
                for i in range(2):
                    if self.point[i] < 0:
                        self.point[i] += self.window.dt * self.speed
                        if self.point[i] >= 0:
                            self.point[i] = 0
                            count += 1
                    elif self.point[i] > 0:
                        self.point[i] -= self.window.dt * self.speed
                        if self.point[i] <= 0:
                            self.point[i] = 0
                            count += 1
                    else:
                        count += 1
                if count == 2:
                    self.finishedOpen()
            elif self.isOpen:
                count = 0
                for i in range(2):
                    if self.point[i] < self.firstPoint[i]:
                        self.point[i] += self.window.dt * self.speed
                        if self.point[i] >= self.firstPoint[i]:
                            self.point[i] = self.firstPoint[i]
                            count += 1
                    elif self.point[i] > self.firstPoint[i]:
                        self.point[i] -= self.window.dt * self.speed
                        if self.point[i] <= self.firstPoint[i]:
                            self.point[i] = self.firstPoint[i]
                            count += 1
                    else:
                        count += 1
                if count == 2:
                    self.finishedClose()
        self.renderVertices = []
        for vertex in self.vertices:
            tmp = []
            coords = [self.x, self.y]
            for i in range(2):
                if vertex[i] == 1440:
                    tmp.append(vertex[i] + self.point[i])
                else:
                    tmp.append(vertex[i] + self.point[i] + coords[i])
            self.renderVertices.append(tmp)

    def render(self):
        pygame.draw.polygon(self.window.surface, self.color, self.renderVertices)
        if self.text != None:
            self.window.render.text(*self.text, surface = self.window.surface, x = self.textX + self.point[0] + self.x, y = self.textY + self.point[1] + self.y, blit = True,
                                    alpha = self.textAlpha)
