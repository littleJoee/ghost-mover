import pygame
import sys

from data.scripts.utils import load_image
from data.scripts.entites import Player, Bell

class Game:
    screen_size = (960, 620)
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.display = pygame.Surface((self.screen_size[0] / 2, self.screen_size[1] / 2))
        self.clock = pygame.time.Clock()

        self.assets = {
            'player': load_image('ghost.png'),
            'target': load_image('target.png'),
            'bell': load_image('bell.png'),
            'button': load_image('button.png')
        }
        self.player = Player(self, [0, 0], 'player')
        self.movement = [False, False, False, False]
        self.action = False

        self.entities = {
            Bell(self, [3 * 16, 3 * 16]),
            Bell(self, [5 * 16, 3 * 16]),
        }

    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            self.player.update(self.entities, [self.movement[1] - self.movement[0], self.movement[3] - self.movement[2]])
            self.player.render(self.display)

            for bell in self.entities:
                bell.update()
                bell.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                    if event.key == pygame.K_x:
                        self.action = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False
                    if event.key == pygame.K_x:
                        self.action = False
                    

            self.screen.blit(pygame.transform.scale(self.display, self.screen_size), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    Game().run()