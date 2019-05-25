from Constants import *


class Player:
    def __init__(self, main):
        self._main = main
    
    def setSpawn(self, x, y):
        self._main.player.spawn = [x, y - 29 / BLOCK_SIZE]
    
    def climb(self, climb):
        self._main.player.climb = climb
