from GameWarning import GameWarning


class WarningHandler:
    def __init__(self, window):
        self.warning = None
        self.window = window
        self.isActive = False
        self.removing = False
    
    def createWarning(self, text, timeOut):
        timeOut /= 2
        self.warning = GameWarning(timeOut, text, self.window)
        
    def remove(self, time):
        if self.warning != None:
            text = self.warning.text
            self.warning = GameWarning(time, text, self.window)
            self.warning.show()
            self.warning.showTime = time / 2
            self.removing = True

    def update(self):
        if self.warning != None:
            self.warning.update()
            self.isActive = self.warning.active
            if not self.isActive and self.removing:
                self.warning = None
                self.removing = False
            elif not self.warning.showing and not self.isActive:
                self.warning = None
        else:
            self.isActive = False

    def render(self):
        if self.warning != None:
            self.warning.render()
