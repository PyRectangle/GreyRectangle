from KeyBindingsMenu.Binding import Binding


class KeyBindingsMenu:
    def __init__(self, main):
        self.main = main
        self.bindings = []
        y = 0
        for control in self.main.config.config["Controls"]:
            self.bindings.append(Binding(y, main.config.config["Controls"][control], main.config.config["ControlsDescription"][control], 5, control,
                                         main.config.config, main.window))
            y += 50
    
    def create(self):
        for binding in self.bindings:
            binding.create()

    def remove(self):
        for binding in self.bindings:
            binding.remove()
    
    def update(self):
        self.main.window.guiEscape = self.main.config.config["Controls"]["Escape"]
        for binding in self.bindings:
            binding.update()
    
    def render(self):
        self.main.window.screenSurfaces = []
        for binding in self.bindings:
            binding.render()
