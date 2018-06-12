from gui.Base_gui import Base_gui, SELECTION_BAR
import pygame


class Selection_bar(Base_gui):
    def __init__(self, selection, cursor_color, draw_procent, possible_selections, round, places, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.cursor_surface = pygame.Surface((self.width / 25, self.height * 1.2))
        self.cursor_surface.fill(cursor_color)
        
        self.draw_procent = draw_procent
        self.draw_other = None
        self.round = round
        self.places = places
        self.possible_selections = possible_selections
        self.text_without_procent = self.text
        self.cursor_pos = self.width / self.possible_selections * selection
        self.type = SELECTION_BAR
        
        self.get_procent()
        self.update_surface()
    
    def get_bytes(self, text, bytes):
        if bytes == 0:
            return text
        else:
            count = 0
            txt = []
        
            for i in text:
                count += 1
                txt.append(i)
                if count >= bytes:
                    break
            
            string = ""
            
            for i in txt:
                string += i
            
            return string
    
    def get_procent(self):
        if self.round:
            self.procent = int(self.possible_selections / self.width * self.cursor_pos + 0.5)
        else:
            self.procent = self.possible_selections / self.width * self.cursor_pos
        
    def update(self, main):
        Base_gui.update(self, main)
        
        if self.pressed:
            self.cursor_pos = main.window.mouse_pos[0] - self.x
        
            self.get_procent()
            self.update_surface()
    
    def update_surface(self):
        if self.draw_procent:
            self.text = self.text_without_procent + ":" + self.get_bytes(str(self.procent), self.places)
        elif self.draw_other != None:
           self.text = self.text_without_procent + ":" + self.get_bytes(str(self.draw_other), self.places)
        
        Base_gui.update_surface(self)
