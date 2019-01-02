from Level.Render import Render
from Level.Data import Data
from Constants import *
import os


class Level:
    def __init__(self, folder, main):
        self.name = folder
        self.folder = LEVEL_PATH + "/" + folder
        self.dataFiles = []
        files = os.listdir(self.folder)
        for file in files:
            if file[0:4] == "data":
                self.dataFiles.append(file)
        self.render = Render(self, main)
        self.data = Data(self)
    
    def openSection(self, number):
        self.close()
        self.data = Data(self, number)
    
    def save(self):
        self.data.save()
        for region in self.data.regions:
            if region.loaded:
                region.save()
            region.save()

    def close(self):
        self.data.close()
        del self.data
