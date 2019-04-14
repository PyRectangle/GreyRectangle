from Frame.Render import Render
from Constants import *


class DebugScreen:
    def __init__(self, window):
        self.renderObj = Render(window)

    def render(self):
        self.renderObj.text(FONT, 50, "FPS:" + str(int(self.renderObj.window.fps)), True, (0, 0, 0), None, self.renderObj.window.surface, 0, 0)
