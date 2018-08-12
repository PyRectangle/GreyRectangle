from Frame.gui.Button import Button
from Menu import Menu


class Menus:
    def __init__(self, main):
        self.menus = []
        self.main = main
        self.window = main.window
        self.FONT = "resources/fonts/freesansbold.ttf"
    
    def create(self):
        self.mainMenu = Menu()
        self.mainMenu.addGui(Button, (self.play, 370, 120, 700, 150, "Play", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), self.FONT, True, 50, 50,
                                      0.3, True, [-2, 0], self.window))
        self.mainMenu.addGui(Button, (self.play, 370, 320, 700, 150, "Editor", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), self.FONT, True, 50, 50,
                                      0.3, True, [2, 0], self.window))
        self.mainMenu.addGui(Button, (self.play, 370, 520, 700, 150, "Settings", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), self.FONT, True, 50, 50,
                                      0.3, True, [-2, 0], self.window))
        self.mainMenu.addGui(Button, (self.window.exit, 370, 720, 700, 150, "Exit", (100, 100, 100), (0, 0, 0), (100, 100, 255), (0, 0, 0), self.FONT, True, 50, 50,
                                      0.3, True, [2, 0], self.window))
        self.menus = [self.mainMenu]
    
    def play(self):
        self.remove()

    def update(self):
        for menu in self.menus:
            if menu.created or menu.createdGuis != []:
                menu.update()
    
    def render(self):
        for menu in self.menus:
            if menu.created or menu.createdGuis != []:
                menu.render()
    
    def remove(self):
        for menu in self.menus:
            if menu.created:
                menu.remove()

    def show(self, menu):
        self.remove()
        if type(menu) == int:
            self.menus[menu].create()
        else:
            menu.create()
