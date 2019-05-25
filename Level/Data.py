from Level.Region import Region
import json
import os


class Data:
    def __init__(self, level, number = 0):
        self.regions = []
        self.regionsGrid = []
        self.level = level
        self.number = number
        self.deleteCount = 0
        files = os.listdir(level.folder + "/region" + str(number))
        files.sort()
        self.smallest = self.getCoords(files[-1])
        self.biggest = self.getCoords(files[-1])
        for file in files:
            coords = self.getCoords(file)
            for i in range(2):
                if coords[i] < self.smallest[i]:
                    self.smallest[i] = coords[i]
                if coords[i] > self.biggest[i]:
                    self.biggest[i] = coords[i]
        for y in range(self.biggest[1] + 1 - self.smallest[1]):
            line = []
            for x in range(self.biggest[0] + 1 - self.smallest[0]):
                line.append(None)
            self.regionsGrid.append(line)
        for file in files:
            coords = self.getCoords(file)
            region = Region(level, number, *coords, regionIndex = len(self.regions))
            self.regions.append(region)
            self.regionsGrid[coords[1] - self.smallest[1]][coords[0] - self.smallest[0]] = region

    def getCoords(self, string):
        coords = []
        coord = ""
        first = False
        for char in string:
            if char == "-" and coord != "":
                coords.append(int(coord))
                coord = ""
                first = True
            elif char == ".":
                coords.append(int(coord))
                return coords
            else:
                coord += char

    def load(self):
        file = open(self.level.folder + "/data" + str(self.number) + ".json", "r")
        self.jsonData = json.load(file)
        file.close()
        self.loadJsonData()
    
    def loadJsonData(self):
#        self.music = self.jsonData["Music"]
        self.spawnX = self.jsonData["SpawnX"] - self.smallest[0] * 16
        self.spawnY = self.jsonData["SpawnY"] - self.smallest[1] * 16
        self.lifes = self.jsonData["Lifes"]
        self.jumpTime = self.jsonData["JumpTime"]
        self.jumpHeight = self.jsonData["JumpHeight"]
        self.walkSpeed = self.jsonData["WalkSpeed"]
        self.fallSpeed = self.jsonData["FallSpeed"]
        self.fallSpeedMultiplier = self.jsonData["FallSpeedMultiplier"]
        self.climbSpeed = self.jsonData["ClimbSpeed"]
        self.description = self.jsonData["Description"]

    def save(self):
        file = open(self.level.folder + "/data" + str(self.number) + ".json", "w")
        file.write(json.dumps(self.jsonData, sort_keys = True, indent = 4))
        file.close()
    
    def close(self):
        for i in range(len(self.regions)):
            del self.regions[i]
