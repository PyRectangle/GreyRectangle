import pygame


class ClickAnim:
    def __init__(self, button):
        self.button = button
        self.pos = -1
        self.finished = False
        for i in range(int(self.button.pressDifference / 2 + 0.5)):
            self.button.setSize(False)
        self.update()

    def update(self):
        self.pos += self.button.window.dt / 5
        self.coords = [self.button.x - self.pos, self.button.y - self.pos, self.button.width + self.button.x + self.pos, self.button.height + self.button.y +
                       self.pos]
        if self.pos > self.button.pressDifference:
            self.finished = True
            self.button.function()
    
    def render(self):
        pygame.draw.polygon(self.button.window.surface, self.button.frameColor, [[self.coords[0], self.coords[1]], [self.coords[0], self.coords[3]], 
        [self.coords[2], self.coords[3]], [self.coords[2], self.coords[1]]], 1)
