from Constants import *
import json


class Config:
    def __init__(self):
        self.file = CONFIG_FILE
        self.config = None
    
    def load(self):
        file = open(self.file, "r")
        self.config = json.load(file)
        file.close()
    
    def save(self):
        file = open(self.file, "w")
        file.write(json.dumps(self.config, sort_keys = True, indent = 4))
        file.close()
