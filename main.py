import SWF
import pygame
import os
import time
import level

win = SWF.Window(caption="GreyRectangle", icon="images/player.png")
buttons_x = win.window.get_width() / 2 - 105
buttons_y = win.window.get_height() / 2 - 80
player_on_screen_x = win.window.get_width() / 2 - 25
player_on_screen_y = win.window.get_height() / 2 - 50
player_x = 0
player_y = 0
selected_image = 7
selected_image_count = 0
levels = os.listdir("levels")
settings = False
level_selection = False
in_level = False
selected_level = 0
select_level_up_count = 0
select_level_down_count = 0
fall_multiplier = 1.002
fall_count = 1
jump_count = 0
jump_active = False
on_ground = False
images = SWF.resources.load_images(True, ("images/player.png",
                                          "images/stone.png",
                                          "images/grass.png",
                                          "images/dirt.png",
                                          "images/water.png",
                                          "images/lava.png",
                                          "images/door.png",
                                          "images/up.png",
                                          "images/up_pressed.png"))
clock = pygame.time.Clock()
win.create_button(buttons_x, buttons_y, 211, 50, "start game", 40)
win.create_button(buttons_x + 20, buttons_y + 80, 170, 50, "settings", 40)


def render():
    global selected_image, selected_image_count, i
    if level_selection:
        win.window.fill((255, 100, 100))
        pygame.draw.line(win.window, (100, 255, 100), (0, 225), (640, 225), 70)
        for pos in -3, -2, -1, 1, 2, 3, 0:
            try:
                if selected_level + pos >= 0:
                    win.textanzeige(levels[selected_level + pos], 40, (0, 0, 0), 80, pos * 70 + 200)
                    try:
                        win.window.blit(SWF.resources.load_images(True,
                                                                  ("levels/" + levels[selected_level + pos] +
                                                                   "/icon.png",))[0], (10, pos * 70 + 194))
                    except pygame.error:
                        pass
            except IndexError:
                pass
    elif not in_level:
        win.window.fill((255, 255, 255))
        win.handle_buttons()
    else:
        win.window.fill((255, 255, 255))
        player_block_x = int(player_x / 64)
        player_block_y = int(player_y / 64)
        for block_y in range(9):
            for block_x in range(11):
                array_pos_of_block_x = block_x - player_block_x
                array_pos_of_block_y = block_y - player_block_y
                if array_pos_of_block_x >= 0 and array_pos_of_block_y >= 0:
                    try:
                        try:
                            if region[array_pos_of_block_y][array_pos_of_block_x] == 6:
                                win.window.blit(blocks[region[array_pos_of_block_y][array_pos_of_block_x]].texture,
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
                                            (block_y - player_block_y - 1) * 64 + player_y + 127]
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
                                    win.window.blit(images[selected_image],
                                                    ((block_x - player_block_x) * 64 + player_x + 16,
                                                     (block_y - player_block_y - 1) * 64 + player_y - 38))
                                    selected_image_count += 1
                                    if selected_image_count >= 30:
                                        selected_image_count = 0
                                        if selected_image == 7:
                                            selected_image = 8
                                        elif selected_image == 8:
                                            selected_image = 7
                            else:
                                win.window.blit(blocks[region[array_pos_of_block_y][array_pos_of_block_x]].texture,
                                                ((block_x - player_block_x) * 64 + player_x,
                                                 (block_y - player_block_y) * 64 + player_y))
                        except IndexError:
                            pass
                    except TypeError:
                        pass
        win.window.blit(images[0], (player_on_screen_x, player_on_screen_y))


def test_walls(direction):
    player_block_pos_x = -player_x / 64 + 5
    player_block_pos_y = -player_y / 64 + 3
    no_walls = True
    if direction == "up":
        for ind in 0.39, -0.39:
            if blocks[region[int(player_block_pos_y - 0.04)][int(player_block_pos_x + ind)]].solid:
                no_walls = False
        if player_y >= 190:
            no_walls = False
    elif direction == "down":
        try:
            for ind in 0.39, -0.39:
                if blocks[region[int(player_block_pos_y + 1.39)][int(player_block_pos_x + ind)]].solid:
                    no_walls = False
        except IndexError:
            no_walls = False
    elif direction == "right":
        try:
            for ind in 0.03, -0.665, -1.36:
                if blocks[region[int(player_block_pos_y - ind)][int(player_block_pos_x + 0.4)]].solid:
                    no_walls = False
        except IndexError:
            no_walls = False
    elif direction == "left":
        for ind in 0.03, -0.665, -1.36:
            if blocks[region[int(player_block_pos_y - ind)][int(player_block_pos_x + -0.4)]].solid:
                no_walls = False
        if player_x >= 295:
            no_walls = False
    return no_walls


def window_close():
    pygame.quit()
    os.system("rm -r __pycache__")
    os.system("rm -r SWF/__pycache__")
    exit()


class Block:
    def __init__(self, texture, solid, dead, colorkey):
        self.texture = texture
        self.solid = solid
        self.dead = dead
        if colorkey is not None and texture is not None:
            self.texture.set_colorkey(colorkey)


blocks = [
    Block(None, False, False, None),
    Block(images[1], True, False, None),
    Block(images[2], True, False, None),
    Block(images[3], True, False, None),
    Block(images[4], False, False, None),
    Block(images[5], False, True, None),
    Block(images[6], False, False, (255, 255, 255))
]

win.on_close = window_close

while True:
    clock.tick(0)
    win.handle_events()
    if win.button == "settings" and not settings:
        settings = True
        for i in range(2):
            win.remove_button(0)
        win.create_button(30, win.window.get_height() - 80, 110, 50, "back", 45)
    if win.button == "start game":
        level_selection = True
        for i in range(2):
            win.remove_button(0)
        win.handle_buttons()
    if win.keys[pygame.K_ESCAPE] and settings or win.button == "back" and settings:
        settings = False
        win.remove_button(0)
        win.create_button(buttons_x, buttons_y, 211, 50, "start game", 40)
        win.create_button(buttons_x + 20, buttons_y + 80, 170, 50, "settings", 40)
    if level_selection:
        if win.keys[pygame.K_RETURN]:
            level_selection = False
            in_level = True
            opened_level = level.open_level("levels/" + levels[selected_level] + "/region/1.rgn")
            player_x = opened_level[2]
            player_y = opened_level[3]
            region = opened_level[0]
        if win.keys[pygame.K_ESCAPE]:
            level_selection = False
            win.create_button(buttons_x, buttons_y, 211, 50, "start game", 40)
            win.create_button(buttons_x + 20, buttons_y + 80, 170, 50, "settings", 40)
        if win.keys[pygame.K_DOWN] and not levels[selected_level] == levels[-1]:
            select_level_down_count += 1
            selected_level += 1
            time.sleep(0.3 / select_level_down_count)
        else:
            select_level_down_count = 0
        if win.keys[pygame.K_UP]:
            select_level_up_count += 1
            selected_level -= 1
            if selected_level < 0:
                selected_level = 0
            time.sleep(0.3 / select_level_up_count)
        else:
            select_level_up_count = 0
    if in_level:
        speed = int(clock.get_time() / 2)
        fall_speed = int(clock.get_time() / 1.5 * fall_count)
        for index in range(speed):
            if win.keys[pygame.K_ESCAPE]:
                in_level = False
                level_selection = True
            if win.keys[pygame.K_RIGHT] and test_walls("right"):
                player_x -= 1
            if win.keys[pygame.K_LEFT] and test_walls("left"):
                player_x += 1
        if win.keys[pygame.K_SPACE] and on_ground:
            jump_active = True
            jump_count = 1
        for index in range(int(fall_speed)):
            if test_walls("down"):
                if not jump_active:
                    player_y -= 1
                on_ground = False
                fall_count *= fall_multiplier
            else:
                on_ground = True
                fall_count = 1
        if jump_active:
            for index in range(int(25 / jump_count)):
                if test_walls("up"):
                    player_y += 1
                else:
                    jump_count = 25
                    break
            jump_count += 1
            if jump_count >= 25:
                jump_active = False
    render()
    if in_level:
        win.textanzeige("FPS:" + str(int(clock.get_fps())), 25)
    pygame.display.update()
