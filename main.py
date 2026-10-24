import pygame
import sys

from data.scripts.utils import load_image
from data.scripts.entites import Player, Bell

from data.scripts.tilemap import Tilemap
from data.scripts.levels import Level

class Game:
    screen_size = (960, 620)
    def __init__(self, is_editor=False):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.display = pygame.Surface((self.screen_size[0] / 2, self.screen_size[1] / 2))
        self.clock = pygame.time.Clock()
        self.is_editor = is_editor
        self.running = True

        self.assets = {
            'player': load_image('ghost.png'),
            'target': load_image('target.png'),
            'bell': load_image('bell.png'),
            'button': load_image('button.png'),
            'wall': load_image('tiles/0.png')
        }
        self.movement = [False, False, False, False]
        self.action = False

        self.tilemap = Tilemap(self, tile_size=16)
        self.level = Level(self.tilemap)

        self.load_level(self.level.get_current_level())

    def load_level(self, map_id):
        self.player = Player(self, [0, 0], 'player') 
        self.tilemap.load(map_id)
        print(self.tilemap.tilemap)

        self.bells = []
        for spawner in self.tilemap.extract([('player', 0), ('bell', 0)]):
            print(spawner)
            if spawner['type'] == 0:
                self.player.pos = [spawner['pos'][0], spawner['pos'][1]]
            else:
                self.bells.append(Bell(self, (spawner['pos'][0], spawner['pos'][1])))

    def select_level(self, level_id: str):
        self.tilemap.load(level_id)

    def run(self):
        while self.running:
            self.display.fill((0, 0, 0))

            self.player.update(self.bells, [self.movement[1] - self.movement[0], self.movement[3] - self.movement[2]])
            self.player.render(self.display)

            for bell in self.bells:
                bell.update()
                bell.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.is_editor:
                        self.running = False
                    else:
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

Game().run()