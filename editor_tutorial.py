import time

import pygame

import SWF

window = SWF.Window((600, 440), "editor tutorial")
window.create_button(470, 360, 100, 50, "next", 45)
window.create_button(30, 360, 110, 50, "back", 45)
images = SWF.resources.load_images(True, ("images/editor_tutorial/1.png",))
number = 0
while True:
    if window.button == "next":
        number += 1
        if number > 3:
            number = 0
        time.sleep(0.2)
    if window.button == "back":
        number -= 1
        if number < 0:
            number = 3
        time.sleep(0.2)
    window.window.blit(images[number], (0, 0))
    window.handle_events()
    window.handle_buttons()
    pygame.display.update()
