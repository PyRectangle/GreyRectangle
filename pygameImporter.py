from Constants import CONFIG_FILE
import json


failedSDL2Import = False
if json.load(open(CONFIG_FILE))["SDL2"]:
    try:
        import pygame_sdl2 as pygame
        from pygame_sdl2.locals import *
    except ImportError:
        failedSDL2Import = True
        print("Could not import pygame_sdl2.")
        print("Falling back to the normal pygame.")
        import pygame
        from pygame.locals import *
else:
    import pygame
    from pygame.locals import *
