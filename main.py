import pygame
import sys
import random

from data.scripts.utils import load_image, load_images
from data.scripts.entites import Player, Bell, Button, TextObj

from data.scripts.tilemap import Tilemap
from data.scripts.levels import Level
from data.scripts.trasnsition import Transition

class Game:
    screen_size = (960, 620)
    def __init__(self, is_editor=False):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        self.display = pygame.Surface((480, 310), pygame.SRCALPHA)
        self.display_2 = pygame.surface.Surface((480, 310))
        self.clock = pygame.time.Clock()
        self.is_editor = is_editor
        self.running = True

        self.assets = {
            'player': load_image('ghost.png'),
            'target': load_image('target.png'),
            'bell': load_image('bell.png'),
            'button': load_image('button.png'),
            'wall': load_images('tiles'),
            'text_img': load_images('text')
        }
        self.sfx = {
            'ambiance': pygame.mixer.Sound('data/sfx/ambience.wav'),
            'beat': None,
        }

        self.sfx['ambiance'].set_volume(0.1)
        self.movement = [False, False, False, False]
        self.action = False
        self.screen_shake = 0
        self.transition = -30
        self.dead = False
        # print(self.assets['player'].get_at((8, 8)))

        self.tilemap = Tilemap(self, tile_size=16)
        self.level = Level(self.tilemap)

        self.player = Player(self, [0, 0], 'player') 
        self.load_level(self.level.get_current_level())

    def load_level(self, map_id: str):
        self.tilemap.load(map_id)

        self.bells = []
        self.buttons = []
        for spawner in self.tilemap.extract([('player', 0), ('bell', 0), ('button', 0)], False):
            if spawner['type'] == 'player' and spawner['variant'] == 0:
                self.player.pos = [spawner['pos'][0], spawner['pos'][1]]
            if spawner['type'] == 'button' and spawner['variant'] == 0:
                self.buttons.append(Button(self, spawner['pos']))
            if spawner['type'] == 'bell' and spawner['variant'] == 0:
                self.bells.append(Bell(self, (spawner['pos'][0], spawner['pos'][1])))

        self.text = []
        for text_img in self.tilemap.extract([('text_img', i) for i in range(5)]):
            self.text.append(TextObj(self, text_img['pos'], text_img['variant']))

        self.text[3].effect = True

        self.dead = False
        self.transition = -30


    def select_level(self, level_id: str):
        self.tilemap.load(level_id)

    def check_win(self):
        if all(button.pressed for button in self.buttons):
            if self.level.won():
                self.dead = True
                return
            # no more levels, quit
            pygame.quit()
            sys.exit()

    def run(self):
        while self.running:
            self.sfx['ambiance'].play(-1)
            self.display.fill((10, 10, 10))

            if not self.dead:
                self.check_win()

            if self.dead:
                self.transition = min(40, self.transition + 1)
                if self.transition == 30:
                    self.load_level(self.level.get_current_level())

            if self.transition < 0:
                self.transition += 1

            self.player.update(self.bells, [self.movement[1] - self.movement[0], self.movement[3] - self.movement[2]])
            self.player.render(self.display)

            for button in self.buttons:
                button.update([self.movement[1] - self.movement[0], self.movement[3] - self.movement[2]])
                button.render(self.display)


            for bell in self.bells:
                bell.update()
                bell.render(self.display)


            self.tilemap.render(self.display)

            for text in self.text:
                text.update()
                text.render(self.display)

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
                    if event.key == pygame.K_c:
                        self.player.cycle_types()
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
                    
            render_offset = [0, 0]
            if self.screen_shake:
                self.screen_shake -= 1
                
                render_offset[0] = random.randint(0, 8) - 4
                render_offset[1] = random.randint(0, 8) - 4

            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                # transition_surf.fill((99, 155, 255)) blue transiton too overwhelming
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))

            self.screen.blit(pygame.transform.scale(self.display, self.screen_size), render_offset)
            pygame.display.update()
            self.clock.tick(60)

Game().run()