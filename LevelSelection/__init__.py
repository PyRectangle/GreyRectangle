from LevelSelection.Graphic import Graphic


class LevelSelection:
    def __init__(self, main):
        self.window = main.window
        self.closed = True
        self.graphics = [Graphic((150, 50, 200), [[0, 0], [600, 0], [450, 400], [0, 400]], [-600, -400], 1, self.window),
                         Graphic((150, 150, 150), [[0, 0], [500, 0], [388, 300], [0, 300]], [-600, -400], 1, self.window, (main.menuHandler.FONT, 100, 
                                                                                                                           "Levelinfo", True, (0, 0, 0), None),
                                                                                                                           10, 10),
                         Graphic((150, 50, 200), [[0, 780], [850, 780], [1000, 1080], [0, 1080]], [0, 300], 1, self.window),
                         Graphic((150, 150, 150), [[0, 880], [800, 880], [900, 1080], [0, 1080]], [0, 300], 1, self.window)]
    
    def toggle(self):
        self.closed = False
        for graphic in self.graphics:
            graphic.toggle()

    def update(self):
        self.closed = True
        for graphic in self.graphics:
            graphic.update()
            if not graphic.isClosed:
                self.closed = False
    
    def render(self):
        for graphic in self.graphics:
            graphic.render()
