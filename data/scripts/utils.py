import pygame


IMG_PATH = 'data/images/'
def load_image(path):
    img = pygame.image.load(IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def lerp(a, b, t):
    return a + t(b - a)