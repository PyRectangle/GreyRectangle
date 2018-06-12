import os

LEVEL_PATH = "levels/"
BLOCKS = "blocks"
MAPDATA = "map_data"


class Section():
    def __init__(self, section_id, level):
        self.section_id = section_id
        self.level = level

        self.mapdata = LEVEL_PATH + self.level + MAPDATA + str(self.section_id)
        self.blocks = LEVEL_PATH + self.level + BLOCKS + str(self.section_id)
        
    def load(self):
        files = os.listdir(LEVEL_PATH + self.level)
        exists = False

        for file in files:
            if file == MAPDATA + str(self.section_id):
                exists = True
        
        if exists:
            mapdata = open(self.mapdata)
        
            self.music = ord(mapdata.read(1))
            self.lifes = ord(mapdata.read(1))
            self.spawn_x = ord(mapdata.read(1))
            self.spawn_y = ord(mapdata.read(1))
            self.size_x = ord(mapdata.read(1))
            self.size_y = ord(mapdata.read(1))
            
            mapdata.close()
      
            self.region = []
            
            layer = []
            blocks = open(self.blocks)
            
            for y in range(self.size_y):
                for x in range(self.size_x):
                    layer.append(ord(blocks.read(1)))
            
                self.region.append(layer)
                layer = []
            
            blocks.close()
    
    def save(self):
        mapdata = open(self.mapdata, "w")
        
        mapdata.write(chr(self.music))
        mapdata.write(chr(self.lifes))
        mapdata.write(chr(self.spawn_x))
        mapdata.write(chr(self.spawn_y))
        mapdata.write(chr(self.size_x))
        mapdata.write(chr(self.size_y))
        
        mapdata.close()
        
        blocks = open(self.blocks, "w")
        
        for y in range(self.size_y):
            for x in range(self.size_x):
                blocks.write(chr(self.region[y][x]))
        
        blocks.close()
        
        
    def close(self):
        try:
            del self.music, self.lifes, self.spawn_x, self.spawn_y, self.size_x, self.size_y, self.region
        except AttributeError:
            del self
