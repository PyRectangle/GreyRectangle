import os
import time
from random import randint
from sys import platform
from SWF import file_manager
import pygame
import SWF
import config
import level
import shutil


def output(text):
    local_time = time.localtime()
    print("[" + str(local_time.tm_hour) + ":" + str(local_time.tm_min) + ":" + str(local_time.tm_sec) + "] " + text)


output("creating window...")
win = SWF.Window(caption="GreyRectangle", icon="images/player.png", flags=pygame.RESIZABLE)
output("setting variables...")
buttons_x = win.window_surface.get_width() / 2 - 105
buttons_y = win.window_surface.get_height() / 2 - 80
player_on_screen_x = win.window_surface.get_width() / 2 - 25
player_on_screen_y = win.window_surface.get_height() / 2 - 50
player_x = 0
player_y = 0
drinking = False
drink_count = 0
delete_this = False
create_new = False
open_button = False
selected_image = 7
selected_image_count = 0
levels = os.listdir("levels")
settings = False
level_selection = False
level_selection_count = 0
in_level = False
level_options = False
selected_level = 0
select_level_up_count = 0
select_level_down_count = 0
fall_multiplier = 1.002
fall_count = 1
jump_count = 0
jump_active = False
height_count = 0
height = 0
on_ground = False
in_blocks = []
level_number = 1
menu_direction = 5
menu_directions = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]
file_index = 0
menu_count = 0
block_image = 0
block_image_count = 0
menu_level_number = 0
level_file_name = ""
in_water = False
editor = False
in_editor = False
editor_x = 0
editor_y = 0
sec_count = 0
selected_block = 1
select_block_count = 0
block_selection = False
block_selection_up = False
block_selection_down = False
block_selection_pos = 100
block_selection_close_count = 0
block_selection_mouse_use = False
create_level = False
delete_level = False
speed_count = 0
fall_speed_count = 0
F1 = False
F11 = False
fullscreen = False
level_resize = False
gravity = True
gravity_count = 0
playing_sound = ""
last_checkpoint = (0, 0)
escape_count = 0
mouse_pos = win.get_mouse_pos()
output("loading config from config.txt...")
volume = float(config.load("volume", "config.txt", 50))
fps_limit = int(config.load("fps_limit", "config.txt", 50))
music = "The music is from audio library more information can be found at the license.html file in the music folder."
output("opening the menu background...")
opened_level = level.open_level("levels/" + levels[selected_level] + "/region/1.rgn")
region = opened_level[0]
lifes = opened_level[5]
menu_x = -opened_level[1][0] * 64 / 2 + 320
menu_y = -opened_level[1][1] * 64 / 2 + 240
output("loading textures...")
images = SWF.resources.load_images(True, ("images/player.png",
                                          "images/stone.png",
                                          "images/grass.png",
                                          "images/dirt.png",
                                          "images/water.png",
                                          "images/lava.png",
                                          "images/door.png",
                                          "images/up.png",
                                          "images/up_pressed.png",
                                          "images/wood.png",
                                          "images/gravity_1.png",
                                          "images/gravity_2.png",
                                          "images/checkpoint_activated.png",
                                          "images/checkpoint_deactivated.png",
                                          "images/heart.png",
                                          "images/leaves.png"))
clock = pygame.time.Clock()
output("creating buttons...")
win.create_button(buttons_x, buttons_y - 30, 180, 50, "Play", 40, 50)
win.create_button(buttons_x, buttons_y + 30, 180, 50, "Editor", 40, 30)
win.create_button(buttons_x, buttons_y + 90, 180, 50, "Settings", 40, 7)
win.create_button(buttons_x, buttons_y + 150, 180, 50, "Exit", 40, 48)
pygame.mixer_music.set_volume(volume)
output("defining functions and classes...")


def refresh_rects():
    rects = []
    for lvl in levels:
        text_surface = pygame.font.Font('SWF/freesansbold.ttf', 40).render(lvl, 1, (0, 0, 0))
        if text_surface.get_width() > 560:
            rects.append(text_surface.get_rect())
        else:
            rects.append(None)
    return rects


def render_level_selection():
    global in_blocks, rect_list
    in_blocks = []
    win.window_surface.fill((255, 50, 50))
    pygame.draw.line(win.window_surface, (50, 255, 50), (0, 225), (640, 225), 70)
    for pos in -3, -2, -1, 1, 2, 3, 0:
        try:
            if selected_level + pos >= 0:
                text_surface = pygame.font.Font('SWF/freesansbold.ttf', 40).render(levels[selected_level + pos], 1,
                                                                                   (0, 0, 0))
                if rect_list[selected_level + pos] is None:
                    win.window_surface.blit(text_surface, (80, pos * 70 + 200))
                else:
                    win.window_surface.blit(text_surface, (80, pos * 70 + 200), rect_list[selected_level + pos])
                try:
                    win.window_surface.blit(SWF.resources.load_images(True,
                                            ("levels/" + levels[selected_level + pos] +
                                             "/icon.png",))[0], (10, pos * 70 + 194))
                except pygame.error:
                    pass
        except IndexError:
            pass
    win.handle_buttons()


def render_menu():
    global in_blocks, menu_x, menu_y, menu_direction, block_image
    in_blocks = []
    win.window_surface.fill((255, 255, 255))
    menu_block_x = int(menu_x / 64)
    menu_block_y = int(menu_y / 64)
    for block_y in range(10):
        for block_x in range(11):
            array_pos_of_block_x = block_x - menu_block_x
            array_pos_of_block_y = block_y - menu_block_y
            if array_pos_of_block_x >= 0 and array_pos_of_block_y >= 0:
                try:
                    if region[array_pos_of_block_y][array_pos_of_block_x] == 8:
                        try:
                            win.window_surface.blit(blocks[region[
                                array_pos_of_block_y][
                                array_pos_of_block_x]].texture[block_image],
                                            ((block_x - menu_block_x) * 64 + menu_x,
                                             (block_y - menu_block_y) * 64 + menu_y))
                        except IndexError:
                            block_image = 0
                    elif region[array_pos_of_block_y][array_pos_of_block_x] == 6:
                        win.window_surface.blit(blocks[region[array_pos_of_block_y][array_pos_of_block_x]].texture,
                                                ((block_x - menu_block_x) * 64 + menu_x,
                                                (block_y - menu_block_y - 1) * 64 + menu_y))
                    elif region[array_pos_of_block_y][array_pos_of_block_x] != 0:
                        win.window_surface.blit(blocks[region[array_pos_of_block_y][array_pos_of_block_x]].texture,
                                                ((block_x - menu_block_x) * 64 + menu_x,
                                                (block_y - menu_block_y) * 64 + menu_y))
                except IndexError:
                    pass
    if menu_x >= 0 or menu_y >= 0:
        menu_direction = change_menu_direction()
    if menu_x <= -opened_level[1][0] * 64 + 640 or menu_y <= -opened_level[1][1] * 64 + 480:
        menu_direction = change_menu_direction()
    win.display_text(music, 12, (0, 0, 0), 3, win.window_surface.get_height() - 12)
    if settings:
        win.display_text("Settings", 50, (0, 0, 0), 210, 0)
    win.handle_buttons()
    win.handle_bars()


def render_game():
    global selected_image, selected_image_count, i, in_blocks, block_image, last_checkpoint, lifes
    in_blocks = []
    win.window_surface.fill((255, 255, 255))
    player_block_x = int(player_x / 64)
    player_block_y = int(player_y / 64)
    for block_y in range(10):
        for block_x in range(11):
            array_pos_of_block_x = block_x - player_block_x
            array_pos_of_block_y = block_y - player_block_y
            if array_pos_of_block_x >= 0 and array_pos_of_block_y >= 0:
                try:
                    try:
                        if region[array_pos_of_block_y][array_pos_of_block_x] == 8:
                            try:
                                win.window_surface.blit(blocks[region[
                                    array_pos_of_block_y][
                                    array_pos_of_block_x]].texture[block_image],
                                                (array_pos_of_block_x * 64 + player_x,
                                                 array_pos_of_block_y * 64 + player_y))
                            except IndexError:
                                block_image = 0
                        in_block = True
                        coordsq1 = [player_on_screen_x,
                                    player_on_screen_y,
                                    player_on_screen_x + 49,
                                    player_on_screen_y + 89]
                        coordsq2 = [array_pos_of_block_x * 64 + player_x,
                                    array_pos_of_block_y * 64 + player_y,
                                    array_pos_of_block_x * 64 + player_x + 63,
                                    array_pos_of_block_y * 64 + player_y + 63]
                        for i in (0, 2, 1), (2, 0, 0), (1, 3, 1), (3, 1, 0):
                            if i[2] == 1:
                                if coordsq1[i[0]] > coordsq2[i[1]]:
                                    in_block = False
                                    break
                            if i[2] == 0:
                                if coordsq1[i[0]] < coordsq2[i[1]]:
                                    in_block = False
                                    break
                        if in_block:
                            in_blocks.append(region[array_pos_of_block_y][array_pos_of_block_x])
                            if region[array_pos_of_block_y][array_pos_of_block_x] == 11:
                                if lifes < opened_level[5]:
                                    region[array_pos_of_block_y][array_pos_of_block_x] = 0
                                    lifes += 1
                                    win.set_percent_of_bar(0, 100 / opened_level[5] * lifes)
                            if region[array_pos_of_block_y][array_pos_of_block_x] == 10:
                                region[array_pos_of_block_y][array_pos_of_block_x] = 9
                                if region[last_checkpoint[1]][last_checkpoint[0]] == 9:
                                    region[last_checkpoint[1]][last_checkpoint[0]] = 10
                                last_checkpoint = (array_pos_of_block_x, array_pos_of_block_y)
                                opened_level[2] = -array_pos_of_block_x * 64 + player_on_screen_x - 7
                                opened_level[3] = -array_pos_of_block_y * 64 + player_on_screen_y + 26
                                output("setting spawn to: " +
                                       str(array_pos_of_block_x) + " " +
                                       str(array_pos_of_block_y) + "...")
                        if region[array_pos_of_block_y][array_pos_of_block_x] == 6:
                            win.window_surface.blit(blocks[region[array_pos_of_block_y][array_pos_of_block_x]].texture,
                                                    ((block_x - player_block_x) * 64 + player_x,
                                                    (block_y - player_block_y - 1) * 64 + player_y))
                            arrow = True
                            coordsq1 = [player_on_screen_x,
                                        player_on_screen_y,
                                        player_on_screen_x + 49,
                                        player_on_screen_y + 89]
                            coordsq2 = [(block_x - player_block_x) * 64 + player_x,
                                        (block_y - player_block_y - 1) * 64 + player_y,
                                        (block_x - player_block_x) * 64 + player_x + 63,
                                        (block_y - player_block_y) * 64 + player_y + 63]
                            for i in (0, 2, 1), (2, 0, 0), (1, 3, 1), (3, 1, 0):
                                if i[2] == 1:
                                    if coordsq1[i[0]] > coordsq2[i[1]]:
                                        arrow = False
                                        break
                                if i[2] == 0:
                                    if coordsq1[i[0]] < coordsq2[i[1]]:
                                        arrow = False
                                        break
                            if arrow:
                                win.window_surface.blit(images[selected_image],
                                                        ((block_x - player_block_x) * 64 + player_x + 16,
                                                        (block_y - player_block_y - 1) * 64 + player_y - 38))
                                selected_image_count += 1
                                if selected_image_count >= 300 / dt:
                                    selected_image_count = 0
                                    if selected_image == 7:
                                        selected_image = 8
                                    elif selected_image == 8:
                                        selected_image = 7
                        elif not region[array_pos_of_block_y][array_pos_of_block_x] == 8:
                            win.window_surface.blit(blocks[region[array_pos_of_block_y][array_pos_of_block_x]].texture,
                                                    ((block_x - player_block_x) * 64 + player_x,
                                                    (block_y - player_block_y) * 64 + player_y))
                    except IndexError:
                        pass
                except TypeError:
                    pass
    win.window_surface.blit(images[0], (player_on_screen_x, player_on_screen_y))
    win.handle_bars()


def render_editor():
    global i, block_image
    win.window_surface.fill((255, 255, 255))
    editor_block_x = int(editor_x / 64)
    editor_block_y = int(editor_y / 64)
    for block_y in range(10):
        for block_x in range(11):
            array_pos_of_block_x = block_x - editor_block_x
            array_pos_of_block_y = block_y - editor_block_y
            if array_pos_of_block_x >= 0 and array_pos_of_block_y >= 0:
                try:
                    if region[array_pos_of_block_y][array_pos_of_block_x] == 8:
                        try:
                            win.window_surface.blit(blocks[region[
                                array_pos_of_block_y][
                                array_pos_of_block_x]].texture[block_image],
                                            ((block_x - editor_block_x) * 64 + editor_x,
                                             (block_y - editor_block_y) * 64 + editor_y))
                        except IndexError:
                            block_image = 0
                    elif region[array_pos_of_block_y][array_pos_of_block_x] == 6:
                        win.window_surface.blit(blocks[region[array_pos_of_block_y][array_pos_of_block_x]].texture,
                                                ((block_x - editor_block_x) * 64 + editor_x,
                                                (block_y - editor_block_y - 1) * 64 + editor_y))
                    elif region[array_pos_of_block_y][array_pos_of_block_x] != 0:
                        win.window_surface.blit(blocks[region[array_pos_of_block_y][array_pos_of_block_x]].texture,
                                                ((block_x - editor_block_x) * 64 + editor_x,
                                                (block_y - editor_block_y) * 64 + editor_y))
                    pygame.draw.polygon(win.window_surface,
                                        (0, 0, 0),
                                        (((block_x - editor_block_x) * 64 + editor_x,
                                          (block_y - editor_block_y) * 64 + editor_y),
                                         ((block_x - editor_block_x) * 64 + editor_x + 63,
                                          (block_y - editor_block_y) * 64 + editor_y),
                                         ((block_x - editor_block_x) * 64 + editor_x + 63,
                                          (block_y - editor_block_y) * 64 + editor_y + 63),
                                         ((block_x - editor_block_x) * 64 + editor_x,
                                          (block_y - editor_block_y) * 64 + editor_y + 63),
                                         ((block_x - editor_block_x) * 64 + editor_x,
                                          (block_y - editor_block_y) * 64 + editor_y)),
                                        1)
                except IndexError:
                    pass
    win.window_surface.blit(images[0], (player_on_screen_x + editor_x - opened_level[2],
                                        player_on_screen_y + editor_y - opened_level[3]))
    if block_selection or block_selection_down or block_selection_up:
        pygame.draw.line(win.window_surface, (0, 0, 0),
                         (0, 426 + block_selection_pos),
                         (640, 426 + block_selection_pos), 90)
        pygame.draw.line(win.window_surface, (255, 255, 255),
                         (0, 426 + block_selection_pos),
                         (640, 426 + block_selection_pos), 70)
        for i in -4, -3, -2, -1, 0, 1, 2, 3, 4:
            try:
                if not selected_block + i < 0:
                    block_texture = blocks[selected_block + i].texture
                    if selected_block + i == 8:
                        if i != 0:
                            block_texture = pygame.transform.scale(block_texture[block_image], (32, 32))
                        else:
                            block_texture = pygame.transform.scale(block_texture[block_image], (64, 64))
                        if i > 0:
                            win.window_surface.blit(block_texture,
                                                    (288 + i * 64 + 32, 410 + block_selection_pos))
                        else:
                            if i == 0:
                                win.window_surface.blit(block_texture,
                                                        (288 + i * 64, 394 + block_selection_pos))
                            else:
                                win.window_surface.blit(block_texture,
                                                        (288 + i * 64, 410 + block_selection_pos))
                    elif block_texture is not None:
                        if i != 0:
                            block_texture = pygame.transform.scale(block_texture, (32, 32))
                        else:
                            block_texture = pygame.transform.scale(block_texture, (64, 64))
                        if i > 0:
                            win.window_surface.blit(block_texture, (288 + i * 64 + 32, 410 + block_selection_pos))
                        else:
                            if i == 0:
                                win.window_surface.blit(block_texture, (288 + i * 64, 394 + block_selection_pos))
                            else:
                                win.window_surface.blit(block_texture, (288 + i * 64, 410 + block_selection_pos))
            except IndexError:
                pass
    win.display_text("press F1 for help", 15, (0, 0, 0), 1, 2)
    if level_resize:
        win.display_text("WARNING", 80, (255, 0, 0), 10, 10)
        win.display_text("If you reduce the size of the section,", 25, (255, 0, 0), 15, 80)
        win.display_text("your edits are made at the border will disappear.", 25, (255, 0, 0), 15, 105)
        win.display_text(str(opened_level[1][0]) + " " + str(opened_level[1][1]), 45, (0, 0, 0), 280, 190)


def render_level_options():
    win.window_surface.fill((255, 255, 255))
    win.display_text("Level options", 60, (0, 0, 0), 0, 27)
    win.display_text("name:", 50, (0, 0, 0), 0, 88)
    win.display_text("music of this section:", 50, (0, 0, 0), 0, 148)
    win.handle_text_inputs()
    win.handle_buttons()


def render():
    if level_selection:
        render_level_selection()
    elif not in_level and not in_editor and not level_options:
        render_menu()
    elif in_level:
        render_game()
    elif in_editor:
        render_editor()
    elif level_options:
        render_level_options()


def test_walls(direction):
    global i
    player_block_pos_x = -player_x / 64 + 5
    player_block_pos_y = -player_y / 64 + 3
    no_walls = True
    if direction == "up":
        for i in 0.39, -0.39:
            if blocks[region[int(player_block_pos_y - 0.04)][int(player_block_pos_x + i)]].solid:
                no_walls = False
        if player_y >= 190:
            no_walls = False
    elif direction == "down":
        try:
            for i in 0.39, -0.39:
                if blocks[region[int(player_block_pos_y + 1.39)][int(player_block_pos_x + i)]].solid:
                    no_walls = False
        except IndexError:
            no_walls = False
    elif direction == "right":
        try:
            for i in 0.03, -0.665, -1.36:
                if blocks[region[int(player_block_pos_y - i)][int(player_block_pos_x + 0.4)]].solid:
                    no_walls = False
        except IndexError:
            no_walls = False
    elif direction == "left":
        for i in 0.03, -0.665, -1.36:
            if blocks[region[int(player_block_pos_y - i)][int(player_block_pos_x + -0.4)]].solid:
                no_walls = False
        if player_x >= 295:
            no_walls = False
    return no_walls


def window_close():
    output("closing window...")
    pygame.quit()
    if platform.lower() == "linux":
        output("removing pycaches...")
        os.system("rm -r __pycache__")
        os.system("rm -r SWF/__pycache__")
    output("saving settings to config.txt...")
    config.save("volume", volume, "config.txt", "w")
    config.save("fps_limit", int(fps_limit), "config.txt", "a")
    output("exiting the program...")
    exit()


def die():
    global player_x, player_y, lifes, in_level, level_selection, gravity
    output("killing the player...")
    player_x = opened_level[2]
    player_y = opened_level[3]
    lifes -= 1
    win.set_percent_of_bar(0, 100 / opened_level[5] * lifes)
    if lifes <= 0:
        lifes = opened_level[5]
        in_level = False
        level_selection = True
        win.remove_bar(0)
        create_buttons_for_level_selection(False)
    gravity = True


def playsound(sound):
    global playing_sound
    if playing_sound != sound:
        pygame.mixer_music.load("music/" + sound)
        pygame.mixer_music.play(-1, 0.0)
        output("playing " + sound + "...")
        playing_sound = sound


def change_menu_direction():
    global i, menu_count, fps
    direction = 0
    count = 0
    for i in menu_directions:
        change = True
        for i2 in range(2):
            if not menu_directions[menu_direction][i2] == -i[i2]:
                change = False
        if change:
            direction = count
        count += 1
    menu_count = fps * 8
    return direction


def move_menu(distance, directon):
    global menu_x, menu_y
    directions = [[distance, 0], [-distance, 0],
                  [0, distance], [0, -distance],
                  [distance, distance], [-distance, -distance],
                  [-distance, distance], [distance, -distance]]
    menu_x += directions[directon][0]
    menu_y += directions[directon][1]


def test(variable, open_file=False):
    if open_file:
        opened_file = open(variable)
        opened_file.close()
    return variable


def move_editor():
    global editor_x, editor_y
    if win.keys[pygame.K_RIGHT]:
        editor_x -= 1
        if editor_x < -opened_level[1][0] * 64 + 320:
            editor_x = -opened_level[1][0] * 64 + 320
    if win.keys[pygame.K_LEFT]:
        editor_x += 1
        if editor_x > 320:
            editor_x = 320
    if win.keys[pygame.K_UP]:
        editor_y += 1
        if editor_y > 240:
            editor_y = 240
    if win.keys[pygame.K_DOWN]:
        editor_y -= 1
        if editor_y < -opened_level[1][1] * 64 + 240:
            editor_y = -opened_level[1][1] * 64 + 240


def create_buttons_for_level_selection(editor_out):
    win.create_button(480, 400, 115, 50, "Start", 45)
    win.create_button(45, 400, 115, 50, "Back", 45)
    if editor_out:
        win.create_button(185, 330, 270, 50, "Delete level", 45)
        win.create_button(185, 400, 270, 50, "Create level", 45)


def remove_buttons_for_level_selection(editor_out):
    global i
    for i in range(2):
        win.remove_button(0)
    if editor_out:
        for i in range(2):
            win.remove_button(0)


class Thread(pygame.threads.Thread):
    def __init__(self):
        pygame.threads.Thread.__init__(self)

    def run(self):
        if platform.lower() == "linux":
            os.system("python3 editor_tutorial.py")
        else:
            os.system("py editor_tutorial.py")


class Block:
    def __init__(self, texture, solid, dead, colorkey):
        self.texture = texture
        self.solid = solid
        self.dead = dead
        try:
            if colorkey is not None and texture is not None:
                self.texture.set_colorkey(colorkey)
        except AttributeError:
            for texture in self.texture:
                texture.set_colorkey(colorkey)


output("defining blocks...")
blocks = [
    Block(None, False, False, None),
    Block(images[1], True, False, None),
    Block(images[2], True, False, None),
    Block(images[3], True, False, None),
    Block(images[4], False, False, None),
    Block(images[5], False, True, None),
    Block(images[6], False, False, (255, 255, 255)),
    Block(images[9], True, False, None),
    Block((images[10], images[11]), False, False, None),
    Block(images[12], False, False, (255, 255, 255)),
    Block(images[13], False, False, (255, 255, 255)),
    Block(images[14], False, False, (255, 255, 255)),
    Block(images[15], True, False, None)
]

rect_list = refresh_rects()
playsound(opened_level[4])
win.on_close = window_close

output("starting mainloop...")
while True:
    clock.tick(fps_limit)
    fps = clock.get_fps()
    dt = clock.get_time()
    win.handle_events()
    escape_count -= 1
    if escape_count < 0:
        escape_count = 0
    if win.keys[pygame.K_F11]:
        F11 = True
    elif F11:
        F11 = False
        fullscreen = not fullscreen
        win.toggle_fullscreen(fullscreen)
    gravity_count += 1
    if gravity_count > fps * 2:
        gravity_count = fps * 2
    block_image_count += 1
    if block_image_count >= fps / 6:
        block_image += 1
        block_image_count = 0
        if block_image > 1:
            block_image = 0
    if in_level and in_water:
        speed = dt / 10
    else:
        speed = dt / 2
    if speed < 1:
        speed_count += speed
        if speed_count >= 1:
            speed = int(speed_count)
            speed_count -= int(speed_count)
        else:
            speed = 0
    else:
        speed_count += speed - int(speed)
        if speed_count > 1:
            speed += speed_count
            speed_count -= int(speed_count)
        speed = int(speed)
    menu_speed = speed / 10
    menu_count += 1
    if menu_count >= fps * 10:
        menu_count = 0
        menu_direction = randint(0, 7)
    move_menu(menu_speed, menu_direction)
    if win.button == "Exit":
        win.on_close()
    if win.button == "Settings" and not settings:
        output("opening settings...")
        settings = True
        for i in range(4):
            win.remove_button(0)
        win.create_bar(20, 60, 250, 50, "volume", 45, volume * 100)
        win.create_bar(320, 60, 280, 50, "fps limit", 45, fps_limit)
        win.create_button(170, win.window_surface.get_height() - 80, 420, 50, "Reset window size", 45)
        win.create_button(20, win.window_surface.get_height() - 80, 115, 50, "Back", 45)
    if settings:
        fps_limit = win.get_percent_of_bar(1)
        if fps_limit < 10:
            fps_limit = 10
            win.set_percent_of_bar(1, 10)
        volume = win.get_percent_of_bar(0) / 100
        pygame.mixer_music.set_volume(volume)
        if win.button == "Reset window size":
            win.dimensions = win.size
            win.window = pygame.display.set_mode(win.size, win.flags)
    if win.button == "Play":
        output("opening level selection...")
        level_selection = True
        for i in range(4):
            win.remove_button(0)
        win.handle_buttons()
        create_buttons_for_level_selection(False)
        editor = False
        level_selection_count = 0
    if win.button == "Editor":
        output("opening level selection...")
        level_selection = True
        for i in range(4):
            win.remove_button(0)
        win.handle_buttons()
        create_buttons_for_level_selection(True)
        editor = True
        level_selection_count = 0
    if win.keys[pygame.K_ESCAPE] and settings or win.button == "Back" and settings:
        output("closing settings...")
        settings = False
        for i in range(2):
            win.remove_bar(0)
        for i in range(2):
            win.remove_button(0)
        win.create_button(buttons_x, buttons_y - 30, 180, 50, "Play", 40, 50)
        win.create_button(buttons_x, buttons_y + 30, 180, 50, "Editor", 40, 30)
        win.create_button(buttons_x, buttons_y + 90, 180, 50, "Settings", 40, 7)
        win.create_button(buttons_x, buttons_y + 150, 180, 50, "Exit", 40, 48)
    if level_selection:
        for rect in rect_list:
            if rect is not None:
                rect.x += int(dt / 5 + 0.5)
                if rect.x >= rect.w - 560:
                    rect.x = 0
        level_selection_count += 1
        mouse_pos = win.get_mouse_pos()
        mouse_click_on_selected_level = \
            win.mouse_pressed != (0, 0, 0) and 260 > mouse_pos[1] > 190 and level_selection_count > fps / 2
        if win.keys[pygame.K_RETURN] or mouse_click_on_selected_level or win.button == "Start":
            output("opening " + levels[selected_level] + "...")
            if editor:
                level_selection = False
                in_editor = True
                level_number = 1
                selected_block = 1
                opened_level = level.open_level("levels/" + levels[selected_level] + "/region/1.rgn")
                editor_x = opened_level[2]
                editor_y = opened_level[3]
                region = opened_level[0]
                lifes = opened_level[5]
                playsound(opened_level[4])
                win.mouse_pressed = (0, 0, 0)
                remove_buttons_for_level_selection(True)
                time.sleep(0.1)
            else:
                gravity = True
                level_selection = False
                in_level = True
                level_number = 1
                opened_level = level.open_level("levels/" + levels[selected_level] + "/region/1.rgn")
                player_x = opened_level[2]
                player_y = opened_level[3]
                region = opened_level[0]
                lifes = opened_level[5]
                win.create_bar(5, 25, 200, 20, "", 45, 100, 0, 0, 1)
                playsound(opened_level[4])
                remove_buttons_for_level_selection(False)
        if win.keys[pygame.K_ESCAPE] or win.button == "Back":
            output("closing level selection...")
            level_selection = False
            menu_x = -opened_level[1][0] * 64 / 2 + 320
            menu_y = -opened_level[1][1] * 64 / 2 + 240
            remove_buttons_for_level_selection(editor)
            win.create_button(buttons_x, buttons_y - 30, 180, 50, "Play", 40, 50)
            win.create_button(buttons_x, buttons_y + 30, 180, 50, "Editor", 40, 30)
            win.create_button(buttons_x, buttons_y + 90, 180, 50, "Settings", 40, 7)
            win.create_button(buttons_x, buttons_y + 150, 180, 50, "Exit", 40, 48)
        if win.keys[pygame.K_DOWN] or win.mouse_pressed != (0, 0, 0) and mouse_pos[1] > 260 and \
           win.button_without_click is None:
            if not levels[selected_level] == levels[-1]:
                select_level_down_count += 1
                selected_level += 1
                time.sleep(0.3 / select_level_down_count)
        else:
            select_level_down_count = 0
        if win.keys[pygame.K_UP] or win.mouse_pressed != (0, 0, 0) and mouse_pos[1] < 190 and\
           win.button_without_click is None:
            select_level_up_count += 1
            selected_level -= 1
            if selected_level < 0:
                selected_level = 0
            time.sleep(0.3 / select_level_up_count)
        else:
            select_level_up_count = 0
        if win.mouse_scroll == 1:
            if not levels[selected_level] == levels[-1]:
                selected_level += 1
        if win.mouse_scroll == -1:
            selected_level -= 1
            if selected_level < 0:
                selected_level = 0
        if win.button == "Create level":
            create_level = True
        if create_level and not win.button == "Create level":
            output("creating new level...")
            create_level = False
            level_name = "new_level"
            while os.path.exists("levels/" + level_name + "/region"):
                level_name += "-"
            os.makedirs("levels/" + level_name + "/region")
            rgn_file = open("levels/" + level_name + "/region/1.rgn", "w")
            rgn_file.write(os.listdir("music")[0] + "\n288\t152\n1\t2\n10\n")
            for i in range(2):
                rgn_file.write("0;")
            rgn_file.write("\n")
            rgn_file.close()
            levels = os.listdir("levels")
            rect_list = refresh_rects()
        if win.button == "Delete level":
            delete_level = True
        if delete_level and not win.button == "Delete level":
            output("deleting " + levels[selected_level] + "...")
            delete_level = False
            level_count = 0
            for i in levels:
                level_count += 1
            if level_count > 1:
                shutil.rmtree("levels/" + levels[selected_level])
                levels = os.listdir("levels")
                rect_list = refresh_rects()
                try:
                    test(levels[selected_level])
                except IndexError:
                    selected_level -= 1
    else:
        for rect in rect_list:
            if rect is not None:
                rect.x = 0
    if in_level:
        if in_water:
            fall_speed = dt / 10 * fall_count
            fall_multiplier = 1.001
            if drinking:
                sec_count += 1
                if sec_count >= fps:
                    drink_count += 1
                    sec_count = 0
                    if drink_count >= 10:
                        die()
                        drink_count = 0
            else:
                drink_count = 0
                sec_count = 0
        else:
            sec_count = 0
            drink_count = 0
            fall_speed = dt / 1.5 * fall_count
            fall_multiplier = 1.002
        if fall_speed < 1:
            fall_speed_count += fall_speed
            if fall_speed_count >= 1:
                fall_speed = int(fall_speed_count)
                fall_speed_count -= int(fall_speed_count)
            else:
                fall_speed = 0
        else:
            fall_speed_count += fall_speed - int(fall_speed)
            if fall_speed_count > 1:
                fall_speed += fall_speed_count
                fall_speed_count -= int(fall_speed_count)
            fall_speed = int(fall_speed)
        for i in range(int(fall_speed)):
            if not jump_active:
                if gravity:
                    if test_walls("down"):
                        player_y -= 1
                        on_ground = False
                        fall_count *= fall_multiplier
                    else:
                        on_ground = True
                        fall_count = 1
                        break
                else:
                    if test_walls("up"):
                        player_y += 1
                        on_ground = False
                        fall_count *= fall_multiplier
                    else:
                        on_ground = True
                        fall_count = 1
                        break
            else:
                on_ground = False
                fall_count = 1
                break
        if win.keys[pygame.K_ESCAPE]:
            output("exiting level...")
            in_level = False
            level_selection = True
            win.remove_bar(0)
            create_buttons_for_level_selection(False)
        if win.keys[pygame.K_SPACE] and in_water:
            for i in range(int(speed * 2)):
                if gravity:
                    if test_walls("up"):
                        player_y += 1
                else:
                    if test_walls("down"):
                        player_y -= 1
        for i in range(speed):
            if win.keys[pygame.K_RIGHT] and test_walls("right"):
                player_x -= 1
            if win.keys[pygame.K_LEFT] and test_walls("left"):
                player_x += 1
        if win.keys[pygame.K_SPACE] and on_ground and not in_water:
            jump_active = True
            jump_count = 0
        for i in range(speed):
            if jump_active:
                jump_count += 1
                if gravity:
                    if jump_count > 100 or not test_walls("up"):
                        jump_active = False
                        break
                    else:
                        player_y += 1
                else:
                    if jump_count > 100 or not test_walls("down"):
                        jump_active = False
                        break
                    else:
                        player_y -= 1
            else:
                break
        gravity_found = False
        in_water = False
        drinking = True
        for i in in_blocks:
            if i == 4:
                in_water = True
            if i != 4:
                drinking = False
            if i == 8 and gravity_count > fps:
                gravity_count = 0
                gravity = not gravity
            if i == 8:
                gravity_found = True
            if i == 6 and win.keys[pygame.K_UP]:
                try:
                    gravity = True
                    level_number += 1
                    opened_level = level.open_level("levels/" +
                                                    levels[selected_level] +
                                                    "/region/" +
                                                    str(level_number) +
                                                    ".rgn")
                    player_x = opened_level[2]
                    player_y = opened_level[3]
                    region = opened_level[0]
                    playsound(opened_level[4])
                except FileNotFoundError:
                    in_level = False
                    level_selection = True
                    win.remove_bar(0)
                    create_buttons_for_level_selection(False)
            if blocks[i].dead:
                die()
                break
        if not gravity_found:
            gravity_count = fps * 2
    if in_editor:
        if level_resize:
            if win.keys[pygame.K_RIGHT]:
                opened_level[1][0] += 1
                for row in region:
                    row.append(0)
                time.sleep(0.1)
            if win.keys[pygame.K_LEFT] and opened_level[1][0] > 1:
                opened_level[1][0] -= 1
                for row in region:
                    del row[opened_level[1][0]]
                time.sleep(0.1)
            if win.keys[pygame.K_UP] and opened_level[1][1] > 2:
                opened_level[1][1] -= 1
                del region[opened_level[1][1]]
                time.sleep(0.1)
            if win.keys[pygame.K_DOWN]:
                opened_level[1][1] += 1
                changed = False
                tmp_array = []
                for x in range(opened_level[1][0]):
                    tmp_array.append(0)
                region.append(tmp_array)
                time.sleep(0.1)
            if win.keys[pygame.K_RETURN]:
                level_resize = False
        else:
            if win.keys[pygame.K_ESCAPE] and escape_count == 0:
                output("exiting editor...")
                in_editor = False
                level_selection = True
                block_selection = False
                block_selection_down = True
                level_file_name = ""
                create_buttons_for_level_selection(True)
            if block_selection:
                block_selection_close_count += 1
                if win.mouse_scroll != 0:
                    selected_block += win.mouse_scroll
                    try:
                        test(blocks[selected_block])
                    except IndexError:
                        selected_block -= 1
                    if selected_block < 1:
                        selected_block = 1
                    block_selection_close_count = 0
                    block_selection_mouse_use = True
                if block_selection_close_count >= fps / 2 and block_selection_mouse_use:
                    block_selection = False
                    block_selection_down = True
            for i in range(speed):
                if block_selection:
                    select_block_count += 1
                    if block_selection_up:
                        block_selection_pos -= 2
                        if block_selection_pos <= 0:
                            block_selection_pos = 0
                            block_selection_up = False
                    if select_block_count > 50:
                        if win.keys[pygame.K_RIGHT]:
                            selected_block += 1
                            try:
                                test(blocks[selected_block])
                            except IndexError:
                                selected_block -= 1
                            select_block_count = 0
                            block_selection_close_count = 0
                        if win.keys[pygame.K_LEFT]:
                            selected_block -= 1
                            if selected_block < 1:
                                selected_block = 1
                            select_block_count = 0
                            block_selection_close_count = 0
                    if win.keys[pygame.K_RETURN]:
                        block_selection = False
                        block_selection_down = True
                else:
                    if block_selection_down:
                        block_selection_pos += 2
                        if block_selection_pos >= 100:
                            block_selection_down = False
                            block_selection_pos = 100
                    move_editor()
            if win.mouse_pressed[0]:
                mouse_pos = win.get_mouse_pos()
                try:
                    array_pos_x = int((-editor_x + mouse_pos[0]) / 64)
                    array_pos_y = int((-editor_y + mouse_pos[1]) / 64)
                    if array_pos_x >= 0 and array_pos_y >= 0:
                        region[array_pos_y][array_pos_x] = 0
                except IndexError:
                    pass
            if win.mouse_pressed[2]:
                mouse_pos = win.get_mouse_pos()
                try:
                    array_pos_x = int((-editor_x + mouse_pos[0]) / 64)
                    array_pos_y = int((-editor_y + mouse_pos[1]) / 64)
                    if array_pos_x >= 0 and array_pos_y >= 0:
                        region[array_pos_y][array_pos_x] = selected_block
                except IndexError:
                    pass
            if win.mouse_pressed[1] and mouse_pos != win.get_mouse_pos():
                mouse_rel = mouse_pos[0] - win.get_mouse_pos()[0], mouse_pos[1] - win.get_mouse_pos()[1]
                mouse_pos = win.get_mouse_pos()
                editor_x -= mouse_rel[0]
                editor_y -= mouse_rel[1]
                if editor_x < -opened_level[1][0] * 64 + 320:
                    editor_x = -opened_level[1][0] * 64 + 320
                if editor_x > 320:
                    editor_x = 320
                if editor_y > 240:
                    editor_y = 240
                if editor_y < -opened_level[1][1] * 64 + 240:
                    editor_y = -opened_level[1][1] * 64 + 240
            mouse_pos = win.get_mouse_pos()
            if win.keys[pygame.K_SPACE]:
                block_selection = True
                block_selection_up = True
                block_selection_close_count = 0
                block_selection_mouse_use = False
            if win.mouse_scroll != 0:
                block_selection = True
                block_selection_up = True
                block_selection_close_count = 0
                block_selection_mouse_use = True
            if win.keys[pygame.K_F1]:
                F1 = True
            elif F1:
                F1 = False
                output("opening tutorial...")
                if fullscreen:
                    fullscreen = False
                    win.toggle_fullscreen(fullscreen)
                Thread().start()
            if win.keys[pygame.K_F2]:
                win.display_text("saving...", 45, (0, 0, 0), 10, 430)
                win.display_update()
                output("saving " + levels[selected_level] + ":" + str(level_number) + "...")
                level.save_level(region,
                                 "levels/" + levels[selected_level] + "/region/" + str(level_number) + ".rgn",
                                 opened_level[1],
                                 opened_level[2],
                                 opened_level[3],
                                 opened_level[4],
                                 opened_level[5])
                if level_file_name != "":
                    os.rename("levels/" + levels[selected_level], "levels/" + level_file_name)
                    levels[selected_level] = level_file_name
                    rect_list = refresh_rects()
                    level_file_name = ""
            if win.keys[pygame.K_F3] or win.keys[pygame.K_F4]:
                F3 = win.keys[pygame.K_F3]
                if F3:
                    level_number -= 1
                else:
                    level_number += 1
                go = True
                try:
                    test("levels/" + levels[selected_level] + "/region/" + str(level_number) + ".rgn", True)
                except FileNotFoundError:
                    go = False
                    if F3:
                        level_number += 1
                    else:
                        level_number -= 1
                if go:
                    if F3:
                        level_number += 1
                    else:
                        level_number -= 1
                    win.display_text("WARNING", 80, (255, 0, 0), 10, 10)
                    win.display_text("When you do this, unsaved changes are deleted in",
                                     25, (255, 0, 0), 15, 90)
                    win.display_text("this section. Do you want to save?", 25, (255, 0, 0), 15, 115)
                    save_menu = True
                    while save_menu:
                        win.handle_events()
                        if win.keys[pygame.K_RETURN]:
                            save_menu = False
                            win.display_text("saving...", 45, (0, 0, 0), 10, 430)
                            win.display_update()
                            output("saving " + levels[selected_level] + ":" + str(level_number) + "...")
                            level.save_level(region,
                                             "levels/" +
                                             levels[selected_level] +
                                             "/region/" +
                                             str(level_number) +
                                             ".rgn",
                                             opened_level[1],
                                             opened_level[2],
                                             opened_level[3],
                                             opened_level[4],
                                             opened_level[5])
                            if level_file_name != "":
                                os.rename("levels/" + levels[selected_level], "levels/" + level_file_name)
                                levels[selected_level] = level_file_name
                                rect_list = refresh_rects()
                                level_file_name = ""
                        if win.keys[pygame.K_ESCAPE]:
                            save_menu = False
                            time.sleep(0.2)
                        win.display_update()
                    if F3:
                        level_number -= 1
                    else:
                        level_number += 1
                    opened_level = level.open_level("levels/" +
                                                    levels[selected_level] +
                                                    "/region/" +
                                                    str(level_number) +
                                                    ".rgn")
                    editor_x = opened_level[2]
                    editor_y = opened_level[3]
                    region = opened_level[0]
                    lifes = opened_level[5]
                    playsound(opened_level[4])
                    time.sleep(0.1)
            if win.keys[pygame.K_F5]:
                level_resize = True
            if win.keys[pygame.K_F6]:
                opened_level[2] = int(editor_x / 64) * 64 + 32
                opened_level[3] = int(editor_y / 64) * 64 - 40
            if win.keys[pygame.K_F7]:
                output("opening level options...")
                level_options = True
                in_editor = False
                win.create_text_input(180, 90, 440, 50, 40, 3, 5)
                win.create_text_input(10, 200, 440, 50, 40, 3, 5)
                win.create_button(460, 200, 170, 50, "Open", 40)
                win.create_button(10, 260, 380, 50, "Create new section", 40)
                win.create_button(10, 320, 370, 50, "Delete this section", 40)
                if level_file_name != "":
                    win.set_text_of_input(0, level_file_name)
                else:
                    win.set_text_of_input(0, levels[selected_level])
                win.set_text_of_input(1, opened_level[4])
    if level_options:
        if not win.get_selected_state_of_input(0) and win.get_text_of_input(0) is not '':
            level_file_name = win.get_text_of_input(0)
        if not win.get_selected_state_of_input(1):
            back_music = opened_level[4]
            opened_level[4] = win.get_text_of_input(1)
            try:
                playsound(opened_level[4])
            except pygame.error:
                opened_level[4] = back_music
        if win.keys[pygame.K_ESCAPE]:
            output("closing level options...")
            level_options = False
            in_editor = True
            for i in range(2):
                win.remove_text_input(0)
            for i in range(3):
                win.remove_button(0)
            escape_count = fps / 2
        if win.button == "Open" and escape_count == 0:
            open_button = True
        elif open_button:
            open_button = False
            back_music = opened_level[4]
            path = file_manager.select_file([("music files", "*")])
            opened_level[4] = path
            if opened_level[4] is not None:
                text_list = []
                for i in opened_level[4]:
                    text_list.append(i)
                letter = ""
                index = -1
                file_text_list = []
                while letter is not "/":
                    file_text_list.insert(0, letter)
                    letter = text_list[index]
                    index -= 1
                opened_level[4] = ""
                for i in file_text_list:
                    opened_level[4] += i
                try:
                    playsound(opened_level[4])
                except pygame.error:
                    clic = "cp " + path + " music"
                    os.system(clic)
                    try:
                        playsound(opened_level[4])
                    except pygame.error:
                        clic = "rm music/" + opened_level[4]
                        os.system(clic)
                        opened_level[4] = back_music
            else:
                opened_level[4] = back_music
            win.set_text_of_input(1, opened_level[4])
        if win.button == "Create new section":
            create_new = True
        elif create_new:
            output("creating new section...")
            create_new = False
            rgn_count = 0
            for i in os.listdir("levels/" + levels[selected_level] + "/region"):
                rgn_count += 1
            rgn_file = open("levels/" + levels[selected_level] + "/region/" + str(rgn_count + 1) + ".rgn", "w")
            rgn_file.write(os.listdir("music")[0] + "\n288\t152\n1\t2\n10\n")
            for i in range(2):
                rgn_file.write("0;")
            rgn_file.write("\n")
            rgn_file.close()
        if win.button == "Delete this section":
            delete_this = True
        elif delete_this:
            output("deleting this section...")
            delete_this = False
            file_count = 0
            for file in os.listdir("levels/" + levels[selected_level] + "/region"):
                file_count += 1
            if file_count > 1:
                clic = "rm levels/" + levels[selected_level] + "/region/" + str(level_number) + ".rgn"
                os.system(clic)
                level_list = os.listdir("levels/" + levels[selected_level] + "/region")
                for i in range(file_count - level_number):
                    clic = "mv levels/" + levels[selected_level] + "/region/" + str(level_number + i + 1) +\
                           ".rgn levels/" + levels[selected_level] + "/region/" + str(level_number + i) + ".rgn"
                    os.system(clic)
                opened_level = level.open_level("levels/" + levels[selected_level] + "/region/1.rgn")
                level_number = 1
                editor_x = opened_level[2]
                editor_y = opened_level[3]
                region = opened_level[0]
                lifes = opened_level[5]
                playsound(opened_level[4])
                win.set_text_of_input(1, opened_level[4])
    render()
    if in_level:
        win.display_text("Lifes:" + str(lifes) + " Breath:" + str(10 - drink_count) +
                         "  FPS:" + str(int(fps)), 25, (0, 0, 0), 5, 0)
    elif in_editor:
        win.display_text("FPS:" + str(int(fps)), 25, (0, 0, 0), 530, 0)
    else:
        win.display_text("FPS:" + str(int(fps)), 25)
    win.display_update()
