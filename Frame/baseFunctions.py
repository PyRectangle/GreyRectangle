from pygameImporter import pygame
import time
import os


def output(text, level="info"):
    try:
        completeDebug = os.environ["LOG_LEVEL"] == "complete"
        debug = os.environ["LOG_LEVEL"] == "debug"
        info = os.environ["LOG_LEVEL"] == "info"
    except KeyError:
        completeDebug = False
        debug = False
        info = False
    underCompleteLevel = level == "info" or level == "debug"
    if level == "info" and info or debug and underCompleteLevel or completeDebug:
        currentTime = time.localtime()
        print("[" + str(currentTime.tm_hour) + ":" + str(currentTime.tm_min) + ":" + str(currentTime.tm_sec) + "] " + text)

def setColorkey(colorkey, surface, unusedColor = [0, 0, 0]):
    if len(colorkey) == 2:
        for y in range(surface.get_height()):
            for x in range(surface.get_width()):
                color = list(surface.get_at((x, y)))[0:3]
                for i in range(3):
                    if color[i] > colorkey[0][i] and color[i] < colorkey[1][i]:
                        color[i] = unusedColor[i]
                if color == unusedColor:
                    surface.set_at((x, y), color)
        surface.set_colorkey(unusedColor)
    else:
        surface.set_colorkey(colorkey)
    return surface
