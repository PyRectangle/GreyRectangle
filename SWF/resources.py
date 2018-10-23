import pygame


def load_images(convert=True, files=()):
    images = []
    for file in files:
        if convert:
            images.append(pygame.image.load(file).convert())
        else:
            images.append(pygame.image.load(file))
    return images


def get_tile(surface, x, y, dx, dy):
    rect = surface.get_rect()
    rect.x, rect.y, rect.w, rect.h = x, y, dx, dy
    return rect
