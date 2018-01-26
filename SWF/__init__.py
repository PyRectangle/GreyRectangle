import pygame
import resources
from screeninfo import get_monitors


def on_close():
    pygame.quit()
    exit()


class Window:
    def __init__(self, size=(640, 480), caption="SWF window", icon=None, mouse_visible=True, flags=0):
        pygame.init()
        pygame.fastevent.init()
        self.size = size
        self.flags = flags
        self.window = pygame.display.set_mode(size, self.flags)
        self.window_surface = pygame.Surface(size)
        self.resizable = pygame.RESIZABLE & flags is not 0
        pygame.display.set_caption(caption)
        pygame.mouse.set_visible(mouse_visible)
        if icon is not None:
            pygame.display.set_icon(pygame.transform.scale(pygame.image.load(icon), (32, 32)))
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
        self.mouse_scroll = 0
        self.buttons_tex = resources.load_images(True, ("SWF/images/button.png",
                                                        "SWF/images/button_pressed.png"))
        self.buttons_objs = []
        self.button = None
        self.button_without_click = None
        self.bars_tex = resources.load_images(True, ("SWF/images/bar.png",
                                                     "SWF/images/line.png",
                                                     "SWF/images/bar_pressed.png",
                                                     "SWF/images/bar_progress.png"))
        self.bars_objs = []
        self.text_input_objs = []
        self.on_close = on_close
        self.clock = pygame.time.Clock()
        self.char = ""
        self.dimensions = size
        self.resolution = get_monitors()[0]
        self.size_before_fullscreen = self.size
        self.dt = 0

    def display_text(self, text="...", size=40, color=(0, 0, 0), posx=0, posy=0):
        self.window_surface.blit(pygame.font.Font('SWF/freesansbold.ttf', size).render(text, 1, color), (posx, posy))

    def display_text_for_input(self, text, size, color, posx, posy, dx, pos, selected, show_line):
        font = pygame.font.Font('SWF/freesansbold.ttf', size)
        img = font.render(text, 1, color)
        text_list = []
        text_to_line = ""
        for i in text:
            text_list.append(i)
        for i in range(pos):
            text_to_line += text_list[i]
        pix_pos = font.render(text_to_line, 1, color).get_rect().width
        rect = img.get_rect()
        if rect.width - rect.x - dx > 0:
            rect.x += rect.width - rect.x - dx + 6
        if pix_pos <= rect.x + dx / 2:
            rect.x = pix_pos - dx / 2
            rect.width = dx - 3
        if pix_pos <= dx / 2:
            rect.x = 0
        if selected and show_line:
            pygame.draw.line(self.window_surface, (0, 0, 0), (pix_pos - rect.x + posx, posy),
                                                             (pix_pos - rect.x + posx, posy + size), 1)
        self.window_surface.blit(img, (posx, posy), rect)

    def toggle_fullscreen(self, boolean):
        if boolean:
            self.size_before_fullscreen = self.dimensions
            self.dimensions = (self.resolution.width, self.resolution.height)
            self.window = pygame.display.set_mode(self.dimensions, self.flags | pygame.FULLSCREEN)
        else:
            self.dimensions = self.size_before_fullscreen
            self.window = pygame.display.set_mode(self.dimensions, self.flags)

    def handle_events(self):
        self.clock.tick(0)
        self.dt = self.clock.get_time()
        self.mouse_scroll = 0
        keydown = False
        for event in pygame.fastevent.get():
            if event.type == pygame.QUIT:
                self.on_close()
            if event.type == pygame.KEYDOWN:
                keydown = True
                self.keys[event.key] = 1
                self.char = event.unicode
            if event.type == pygame.KEYUP:
                self.keys[event.key] = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.mouse_scroll = -1
                if event.button == 5:
                    self.mouse_scroll = 1
            if event.type == pygame.VIDEORESIZE:
                self.window = pygame.display.set_mode(event.size, self.flags)
                self.dimensions = event.size
            self.mouse_pressed = pygame.mouse.get_pressed()
        if not keydown or self.keys[pygame.K_DELETE]:
            self.char = ""

    def get_mouse_pos(self):
        pos_tuple = pygame.mouse.get_pos()
        pos = []
        for i in pos_tuple:
            pos.append(i)
        for i in range(2):
            pos[i] /= self.dimensions[i] / self.size[i]
            pos[i] = int(pos[i])
        return pos

    def display_update(self):
        if self.resizable:
            self.window.blit(pygame.transform.scale(self.window_surface, self.dimensions), (0, 0))
        else:
            self.window.blit(self.window_surface, (0, 0))
        pygame.display.update()

    def create_button(self, x, y, dx, dy, text, size, text_x=3, text_y=5):
        self.buttons_objs.append([x, y, dx, dy, text, size, [text_x, text_y]])

    def remove_button(self, index):
        del self.buttons_objs[index]

    def create_bar(self, x, y, dx, dy, text, size, value, text_x=3, text_y=5, bar_type=0):
        self.bars_objs.append([x, y, dx, dy, text, size, dx / 100 * value, [text_x, text_y], bar_type])

    def remove_bar(self, index):
        del self.bars_objs[index]

    def create_text_input(self, x, y, dx, dy, text_size, text_x, text_y):
        self.text_input_objs.append([x, y, dx, dy, text_size, text_x, text_y, [], False, 0, 0, True, 0])

    def remove_text_input(self, index):
        del self.text_input_objs[index]

    def blit_bar_tex(self, bar):
        self.window_surface.blit(pygame.transform.scale(self.bars_tex[0], (bar[2], bar[3])), (bar[0], bar[1]))
        pygame.draw.polygon(self.window_surface, (0, 0, 0), (
            (bar[0], bar[3] + bar[1]), (bar[2] + bar[0], bar[3] + bar[1]),
            (bar[2] + bar[0], bar[1]), (bar[2] + bar[0], bar[3] + bar[1])),
                            1)

    def get_percent_of_bar(self, index):
        bar = self.bars_objs[index]
        return bar[6] / (bar[2] / 100)

    def set_percent_of_bar(self, index, percent):
        bar = self.bars_objs[index]
        bar[6] = bar[2] / 100 * percent

    def set_text_of_input(self, index, text):
        self.text_input_objs[index][7] = []
        for byte in text:
            self.text_input_objs[index][7].append(byte)
        self.text_input_objs[index][9] = 0

    def get_text_of_input(self, index):
        get_text = ""
        for byte in self.text_input_objs[index][7]:
            get_text += byte
        return get_text

    def get_selected_state_of_input(self, index):
        return self.text_input_objs[index][8]

    def handle_text_inputs(self):
        mouse_pos = self.get_mouse_pos()
        for text_input in self.text_input_objs:
            if not text_input[0] > mouse_pos[0] and not text_input[2] + text_input[0] < mouse_pos[0] and \
                   not text_input[1] > mouse_pos[1] and not text_input[3] + text_input[1] < mouse_pos[1]:
                if self.mouse_pressed != (0, 0, 0):
                    text_input[8] = True
            if text_input[8]:
                text_input[12] += 1
                if text_input[12] >= int(self.clock.get_fps() / 2.5):
                    text_input[11] = not text_input[11]
                    text_input[12] = 0
                if self.keys[pygame.K_RETURN] or self.keys[pygame.K_ESCAPE]:
                    text_input[8] = False
                else:
                    text_input[10] += 1
                    if text_input[10] >= int(self.clock.get_fps() / 10):
                        text_input[10] = int(self.clock.get_fps())
                    if self.keys[pygame.K_RIGHT] and text_input[10] >= int(self.clock.get_fps() / 10):
                        text_input[10] = 0
                        text_input[9] += 1
                        index = 0
                        for i in text_input[7]:
                            index += 1
                        if text_input[9] > index:
                            text_input[9] -= 1
                    if self.keys[pygame.K_LEFT] and text_input[10] >= int(self.clock.get_fps() / 10):
                        text_input[10] = 0
                        text_input[9] -= 1
                        if text_input[9] < 0:
                            text_input[9] += 1
                    if self.keys[8] and text_input[10] >= int(self.clock.get_fps() / 10):
                        text_input[10] = 0
                        try:
                            if text_input[9] - 1 >= 0:
                                del text_input[7][text_input[9] - 1]
                                text_input[9] -= 1
                        except IndexError:
                            pass
                    elif self.keys[pygame.K_DELETE] and text_input[10] >= int(self.clock.get_fps() / 10):
                        text_input[10] = 0
                        try:
                            if text_input[9] >= 0:
                                del text_input[7][text_input[9]]
                        except IndexError:
                            pass
                    elif self.char is not "":
                        text_input[7].insert(text_input[9], self.char)
                        text_input[9] += 1
                self.window_surface.blit(pygame.transform.scale(self.bars_tex[2],
                                                                (text_input[2], text_input[3])),
                                         (text_input[0], text_input[1]))
            else:
                self.window_surface.blit(pygame.transform.scale(self.bars_tex[0],
                                                                (text_input[2], text_input[3])),
                                         (text_input[0], text_input[1]))
            text = ""
            for i in text_input[7]:
                text += i
            self.display_text_for_input(text, text_input[4], (0, 0, 0), text_input[0] +
                                        text_input[5], text_input[1] + text_input[6],
                                        text_input[2], text_input[9], text_input[8], text_input[11])

    def handle_bars(self):
        mouse_pos = self.get_mouse_pos()
        for bar in self.bars_objs:
            if bar[8] == 0:
                if not bar[0] > mouse_pos[0] and not bar[2] + bar[0] < mouse_pos[0] and \
                       not bar[1] > mouse_pos[1] and not bar[3] + bar[1] < mouse_pos[1]:
                    self.window_surface.blit(pygame.transform.scale(self.bars_tex[2], (bar[2], bar[3])),
                                             (bar[0], bar[1]))
                    pygame.draw.polygon(self.window_surface, (0, 0, 0), (
                        (bar[0], bar[3] + bar[1]), (bar[2] + bar[0], bar[3] + bar[1]),
                        (bar[2] + bar[0], bar[1]), (bar[2] + bar[0], bar[3] + bar[1])),
                                        1)
                    if self.mouse_pressed != (0, 0, 0):
                        value_pos = mouse_pos[0] - bar[0]
                        bar[6] = value_pos
                elif not bar[0] - 10 > mouse_pos[0] and not bar[2] + bar[0] < mouse_pos[0] and \
                        not bar[1] > mouse_pos[1] and not bar[3] + bar[1] < mouse_pos[1]:
                    if self.mouse_pressed != (0, 0, 0):
                        value_pos = 0
                        bar[6] = value_pos
                    self.blit_bar_tex(bar)
                elif not bar[0] > mouse_pos[0] and not bar[2] + bar[0] + 10 < mouse_pos[0] and \
                        not bar[1] > mouse_pos[1] and not bar[3] + bar[1] < mouse_pos[1]:
                    if self.mouse_pressed != (0, 0, 0):
                        value_pos = bar[2]
                        bar[6] = value_pos
                    self.blit_bar_tex(bar)
                else:
                    self.blit_bar_tex(bar)
                self.window_surface.blit(pygame.transform.scale(self.bars_tex[1], (10, bar[3] + 3)),
                                         (bar[0] + bar[6] - 5, bar[1] - 1))
                self.display_text(bar[4] + ":" + str(int(bar[6] / (bar[2] / 100))),
                                  bar[5], posx=bar[0] + bar[7][0], posy=bar[1] + bar[7][1])
            elif bar[8] == 1:
                self.blit_bar_tex(bar)
                try:
                    self.window_surface.blit(pygame.transform.scale(self.bars_tex[3], (int(bar[6] - 1), bar[3] - 1)),
                                             (bar[0] + 1, bar[1] + 1))
                except ValueError:
                    pass
                self.display_text(bar[4], bar[5], posx=bar[0] + bar[7][0], posy=bar[1] + bar[7][1])

    def handle_buttons(self):
        mouse_pos = self.get_mouse_pos()
        self.button = None
        for button in self.buttons_objs:
            if not button[0] > mouse_pos[0] and not button[2] + button[0] < mouse_pos[0] and \
                    not button[1] > mouse_pos[1] and not button[3] + button[1] < mouse_pos[1]:
                self.window_surface.blit(pygame.transform.scale(self.buttons_tex[1], (button[2] + 1, button[3] + 1)),
                                         (button[0], button[1]))
                pygame.draw.polygon(self.window_surface, (0, 0, 0), (
                                    (button[0], button[3] + button[1]), (button[2] + button[0], button[3] + button[1]),
                                    (button[2] + button[0], button[1]), (button[2] + button[0], button[3] + button[1])),
                                    1)
                self.button_without_click = button[4]
                if self.mouse_pressed != (0, 0, 0):
                    self.button = button[4]
            else:
                self.window_surface.blit(pygame.transform.scale(self.buttons_tex[0], (button[2] + 1, button[3] + 1)),
                                         (button[0], button[1]))
                pygame.draw.polygon(self.window_surface, (0, 0, 0), (
                                    (button[0], button[3] + button[1]), (button[2] + button[0], button[3] + button[1]),
                                    (button[2] + button[0], button[1]), (button[2] + button[0], button[3] + button[1])),
                                    1)
            self.display_text(button[4], button[5], posx=button[0] + button[6][0], posy=button[1] + button[6][1])
