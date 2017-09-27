import pygame
import resources


def on_close():
    pygame.quit()
    exit()


class Window:
    def __init__(self, size=(640, 480), caption="SWF window", icon=None, mouse_visible=True, *flags):
        pygame.init()
        pygame.fastevent.init()
        self.window = pygame.display.set_mode(size, *flags)
        pygame.display.set_caption(caption)
        pygame.mouse.set_visible(mouse_visible)
        if icon is not None:
            pygame.display.set_icon(pygame.transform.scale(pygame.image.load(icon).convert(), (32, 32)))
        self.keys = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.mouse_pressed = [0, 0, 0]
        self.buttons_tex = resources.load_images(True, ("SWF/images/button.png", "SWF/images/button_pressed.png"))
        self.buttons_objs = []
        self.button = None
        self.on_close = on_close

    def textanzeige(self, anz="...", gr=40, color=(0, 0, 0), posx=0, posy=0):
        img = pygame.font.Font('SWF/freesansbold.ttf', gr).render(anz, 1, color)
        rect = img.get_rect()
        rect.x = posx
        rect.y = posy
        self.window.blit(img, rect)

    def handle_events(self):
        for event in pygame.fastevent.get():
            if event.type == pygame.QUIT:
                self.on_close()
            if event.type == pygame.KEYDOWN:
                self.keys[event.key] = 1
            if event.type == pygame.KEYUP:
                self.keys[event.key] = 0
            self.mouse_pressed = pygame.mouse.get_pressed()

    def create_button(self, x, y, dx, dy, text, gr):
        self.buttons_objs.append([x, y, dx, dy, text, gr])

    def remove_button(self, index):
        del self.buttons_objs[index]

    def handle_buttons(self):
        mouse_pos = pygame.mouse.get_pos()
        self.button = None
        for button in self.buttons_objs:
            if not button[0] > mouse_pos[0] and not button[2] + button[0] < mouse_pos[0] and \
                    not button[1] > mouse_pos[1] and not button[3] + button[1] < mouse_pos[1]:
                self.window.blit(pygame.transform.scale(self.buttons_tex[1], (button[2] + 1, button[3] + 1)),
                                 (button[0], button[1]))
                pygame.draw.polygon(self.window, (0, 0, 0), (
                                    (button[0], button[3] + button[1]), (button[2] + button[0], button[3] + button[1]),
                                    (button[2] + button[0], button[1]), (button[2] + button[0], button[3] + button[1])),
                                    1)
                if self.mouse_pressed != (0, 0, 0):
                    self.button = button[4]
            else:
                self.window.blit(pygame.transform.scale(self.buttons_tex[0], (button[2] + 1, button[3] + 1)),
                                 (button[0], button[1]))
                pygame.draw.polygon(self.window, (0, 0, 0), (
                                    (button[0], button[3] + button[1]), (button[2] + button[0], button[3] + button[1]),
                                    (button[2] + button[0], button[1]), (button[2] + button[0], button[3] + button[1])),
                                    1)
            self.textanzeige(button[4], button[5], posx=button[0] + 3, posy=button[1] + 5)
