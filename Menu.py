class Menu:
    def __init__(self):
        self.guis = []
        self.createdGuis = []
        self.created = False
    
    def addGui(self, guiType, args):
        self.guis.append([guiType, args])
    
    def create(self):
        for gui in self.guis:
            self.createdGuis.append(gui[0](*gui[1]))
        self.created = True
    
    def remove(self):
        for gui in self.createdGuis:
            gui.delete()
        self.created = False
    
    def update(self):
        for gui in self.createdGuis:
            gui.update()
        count = 0
        for i in range(len(self.createdGuis)):
            if self.createdGuis[i - count].remove and (not self.createdGuis[i - count].inScreen or not self.createdGuis[i - count].comeIn):
                del self.createdGuis[i - count]
                count += 1
    
    def render(self):
        for gui in self.createdGuis:
            gui.render()
