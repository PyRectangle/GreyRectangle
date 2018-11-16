from Level import Level
import os


class LevelHandler:
    def __init__(self, main):
        self.levels = os.listdir("Levels")
        self.levels.sort()
        self.levelObjs = []
        for level in self.levels:
            self.levelObjs.append(Level(level, main))
        for level in self.levelObjs:
            level.data.load()
