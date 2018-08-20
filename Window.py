from random import randint
import pygame
import Frame
import sys
import os


class Window(Frame.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def exit(self):
        finished = False
        x0 = -250
        x1 = 0
        while not finished:
            x0 += self.dt * 5
            x1 += self.dt * 4
            if x1 >= 1500:
                finished = True
            pygame.draw.polygon(self.surface, (0, 0, 0), [[x0, 0], [x1, 1080], [0, 1080], [0, 0]])
            self.updateClock()
            self.updateDisplay()
        pygame.quit()
        if sys.platform == "linux":
            os.system("rm -rf __pycache__ */__pycache__ */*/__pycache__ */*/*/__pycache__")
            os.system("rm -f *.pyc */*.pyc */*/*.pyc */*/*/*.pyc")
        exit()
