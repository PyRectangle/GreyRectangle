from Level.Region import Region
from Constants import *
import shutil
import os


class Actions:
    def __init__(self, level, main):
        self.main = main
        self.level = level
        self.clean()
        shutil.copytree(os.path.join(self.level.folder, "region" + str(self.level.data.number)), LEVEL_REGION_EDITOR_TMP)
        for region in self.level.data.regions:
            region.file = LEVEL_REGION_EDITOR_TMP + "/" + str(region.x) + "-" + str(region.y) + ".rgn"
    
    def newRegion(self, regionX, regionY):
        region = Region(self.level, self.level.data.number, regionX, regionY, True, LEVEL_REGION_EDITOR_TMP + "/" + str(regionX) + "-" + str(regionY) + ".rgn")
        region.loaded = True
        region.region = [[[0, []]] * 16] * 16
        region.save()
        self.updateRegions()
        return region
        
    def deleteRegion(self, regionX, regionY):
        os.remove(LEVEL_REGION_EDITOR_TMP + "/" + str(regionX) + "-" + str(regionY) + ".rgn")
        self.updateRegions()

    def getRegion(self, x, y, create = True, load = True):
        regionX, regionY = self.getRegionCoords(x, y)
        region = None
        worked = True
        if not regionX < 0 and not regionY < 0:
            try:
                region = self.level.data.regionsGrid[regionY][regionX]
            except IndexError:
                worked = False
            if region == None and worked:
                worked = False
        else:
            worked = False
        if worked:
            if not region.loaded and load:
                region.load()
            return region
        elif create:
            return self.newRegion(*self.getRegionCoords(x, y, True))
    
    def getRegionCoords(self, x, y, withSmallest = False):
        regionX = x / 16
        regionY = y / 16
        if withSmallest:
            regionX += self.level.data.smallest[0]
            regionY += self.level.data.smallest[1]
        if regionX < 0:
            regionX -= 1
        if regionY < 0:
            regionY -= 1
        return int(regionX), int(regionY)

    def getRegionIndex(self, x, y):
        regionX, regionY = self.getRegionCoords(x, y)
        return int(x - regionX * 16), int(y - regionY * 16)
    
    def updateRegions(self):
        for region in self.level.data.regions:
            region.save()
            region.close()
        smallest = self.level.data.smallest.copy()
        self.level.data.regions = []
        self.level.data.regionsGrid = []
        files = os.listdir(LEVEL_REGION_EDITOR_TMP)
        files.sort()
        self.level.data.smallest = self.level.data.getCoords(files[-1])
        self.level.data.biggest = self.level.data.getCoords(files[-1])
        for file in files:
            coords = self.level.data.getCoords(file)
            for i in range(2):
                if coords[i] < self.level.data.smallest[i]:
                    self.level.data.smallest[i] = coords[i]
                if coords[i] > self.level.data.biggest[i]:
                    self.level.data.biggest[i] = coords[i]
        for y in range(self.level.data.biggest[1] + 1 - self.level.data.smallest[1]):
            line = []
            for x in range(self.level.data.biggest[0] + 1 - self.level.data.smallest[0]):
                line.append(None)
            self.level.data.regionsGrid.append(line)
        for file in files:
            coords = self.level.data.getCoords(file)
            region = Region(self.level, self.level.data.number, *coords, True, os.path.join(LEVEL_REGION_EDITOR_TMP, str(coords[0]) + "-" + str(coords[1]) + ".rgn"))
            self.level.data.regions.append(region)
            self.level.data.regionsGrid[coords[1] - self.level.data.smallest[1]][coords[0] - self.level.data.smallest[0]] = region
        self.level.data.loadJsonData()
        dx = (smallest[0] - self.level.data.smallest[0]) * 16
        dy = (smallest[1] - self.level.data.smallest[1]) * 16
        self.main.editor.x += dx
        self.main.editor.y += dy
        self.main.camera.x += dx
        self.main.camera.y += dy

    def getblock(self, x, y):
        region = self.getRegion(x, y)
        x, y = self.getRegionIndex(x, y)
        return region.region[y][x]

    def setblock(self, x, y, block, blockData):
        region = self.getRegion(x, y)
        x, y = self.getRegionIndex(x, y)
        region.region[y][x] = [block, blockData]

    def fill(self, x1, y1, x2, y2, block, blockData):
        for y in range(y2 - y1):
            for x in range(x2 - x1):
                self.setblock(x1 + x, y1 + y, block, blockData)

    def clone(self, x1, y1, x2, y2, x3, y3, block, blockData):
        for y in range(y2 - y1):
            for x in range(x2 - x1):
                self.setblock(x3 + x, y3 + y, *self.getblock(x1 + x, y1 + y))

    def save(self):
        for region in self.level.data.regions:
            region.save()
        shutil.rmtree(os.path.join(self.level.folder, "region" + str(self.level.data.number)))
        shutil.copytree(LEVEL_REGION_EDITOR_TMP, os.path.join(self.level.folder, "region" + str(self.level.data.number)))
        self.level.data.save()

    def clean(self):
        if os.path.exists(LEVEL_REGION_EDITOR_TMP):
            shutil.rmtree(LEVEL_REGION_EDITOR_TMP)
        self.level.data.__init__(self.level, self.level.data.number)
        self.level.data.load()
