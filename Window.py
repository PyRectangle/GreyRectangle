from random import randint
import Frame


class Window(Frame.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def exit(self):
        self.autoResizing = False
        self.xOrY = randint(0, 1)
        self.posOrNeg = 0
        while self.posOrNeg == 0:
            self.posOrNeg = randint(-1, 1)
        while 1080 > self.__surfaceY > -1080 and 1440 > self.__surfaceX > -1440:
            if self.xOrY:
                self.__surfaceX += self.dt * self.posOrNeg
            else:
                self.__surfaceY += self.dt * self.posOrNeg
            self.updateClock()
            self.updateDisplay()
        exit()
