from Level.Region import Region
from Level import Level
from Constants import *
import shutil
import json
import os


class LevelHandler:
    def __init__(self, main):
        self.main = main
        self.levels = os.listdir(LEVEL_PATH)
        self.levels.sort()
        self.levelObjs = []
        for level in self.levels:
            self.levelObjs.append(Level(level, main))
        for level in self.levelObjs:
            level.data.load()
    
    def create(self, name, description):
        pathToLevelRegion = os.path.join(LEVEL_PATH, name, "region0")
        os.makedirs(pathToLevelRegion)
        jsonData = {
            "ClimbSpeed": 0.008,
            "SpawnX": 0,
            "SpawnY": 1,
            "Lifes": 10,
            "JumpTime": 0.2,
            "JumpHeight": 1.5,
            "WalkSpeed": 1,
            "FallSpeed": 1,
            "FallSpeedMultiplier": 1.003,
            "Description": description
        }
        file = open(os.path.join(LEVEL_PATH, name, "data0.json"), "w")
        file.write(json.dumps(jsonData, sort_keys = True, indent = 4))
        file.close()
        region = Region(None, 0, 0, 0, True, os.path.join(pathToLevelRegion, "0-0.rgn"))
        region.loaded = True
        region.region = [[[0, []]] * 16] * 16
        region.save()
        region.loaded = False
        self.recalculate()
    
    def delete(self, level):
        shutil.rmtree(os.path.join(LEVEL_PATH, level.name))
        self.recalculate()
    
    def recalculate(self):
        self.__init__(self.main)
        self.main.levelSelection.levelGuiHandler.__init__(self.levelObjs, self.main)
