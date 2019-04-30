error1 = False
error2 = False
try:
    import pygame
except ImportError:
    error1 = True
try:
    import pygame_sdl2
except ImportError:
    error2 = True


class KeyTranslate:
    def __init__(self):
        self.installedSdl1 = not error1
        self.installedSdl2 = not error2
        self.installed = self.installedSdl1 and self.installedSdl2
        if self.installed:
            self.generateTables()

    def generateTables(self):
        self.table1to2 = {}
        for attrib in dir(pygame):
            if attrib[0:2] == "K_":
                exec(compile("self.table1to2[pygame." + attrib + "] = pygame_sdl2." + attrib, "", "exec"))
        self.table2to1 = {}
        for attrib in dir(pygame_sdl2):
            if attrib[0:2] == "K_":
                try:
                    exec(compile("self.table2to1[pygame_sdl2." + attrib + "] = pygame." + attrib, "", "exec"))
                except AttributeError:
                    exec(compile("self.table2to1[pygame_sdl2." + attrib + "] = None", "", "exec"))
    
    def translate1to2(self, key):
        return self.table1to2[key]

    def translate2to1(self, key):
        return self.table2to1[key]
