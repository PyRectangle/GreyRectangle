from gui.Base_gui import Base_gui, BUTTON


class Button(Base_gui):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.type = BUTTON
        
        self.update_surface()
