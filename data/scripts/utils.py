import pygame
import os


IMG_PATH = 'data/images/'
def load_image(path):
    img = pygame.image.load(IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

def draw_text():
    pass

def lerp(a, b, t):
    return a + t(b - a)