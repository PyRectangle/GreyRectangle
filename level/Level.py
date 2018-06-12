import os
import shutil
from level import Section
from level.Section import LEVEL_PATH


class Level():
    def __init__(self, name):
        self.name = name + "/"
        self.sections = []
        
        wait = False
    
        for file in os.listdir(Section.LEVEL_PATH + self.name):
            for i in file:
                if i == "m":
                    wait = True
    
                if wait:
                    try:
                        self.sections.append(Section.Section(int(i), self.name))
                        wait = False
                    except ValueError:
                        pass

    def load_section(self, section):
        self.sctions[section].load()
        
    def close_section(self, section):
        self.sections[section].close()

    def delete(self):
        self.close()
        shutil.rmtree(LEVEL_PATH + self.name)

    def close(self):
        for section in self.sections:
            section.close()
