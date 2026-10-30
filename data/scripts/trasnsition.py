# OBSOLETE
import pygame

class Transition:
    def __init__(self):
        self.transition = 60
        self.speed = 1
        self.done = False

    def update(self):
        if self.done:
            del self

        self.transition -= self.speed
        if self.transition == 0:
            return True
        if self.transition == -60:
            self.done = True

    def render(self, surf: pygame.Surface):
        transition_surf = pygame.Surface(surf.get_size())
        pygame.draw.circle(transition_surf, (255, 255, 255), (surf.get_width() // 2, surf.get_height() // 2), (30 - abs(self.transition)) * 8)
        transition_surf.set_colorkey((255, 255, 255))
        surf.blit(transition_surf, (0, 0))