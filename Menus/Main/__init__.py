from Frame.gui.Button import Button
from Menu import Menu


class MainMenu(Menu):
    def __init__(self, menuHandler):
        super().__init__()
        self.addGui(Button, (menuHandler.play, (), 370, 120, 700, 150, "Play", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), menuHandler.FONT, True,
                             50, 50, 0.1, True, [-2, 0], None, self.SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.play, (), 370, 320, 700, 150, "Editor", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), menuHandler.FONT, True,
                             50, 50, 0.1, True, [2, 0], None, self.SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.show, (2), 370, 520, 700, 150, "Settings", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), menuHandler.FONT,
                             True, 50, 50, 0.1, True, [-2, 0], None, self.SOUNDS, menuHandler.window))
        self.addGui(Button, (menuHandler.window.exit, (), 370, 720, 700, 150, "Exit", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), menuHandler.FONT,
                             True, 50, 50, 0.1, True, [2, 0], None, self.SOUNDS, menuHandler.window))
