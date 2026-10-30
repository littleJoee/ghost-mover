import sys

import pygame

from data.scripts.utils import load_images, load_image
from data.scripts.tilemap import Tilemap
from data.scripts.levels import Level

RENDER_SCALE = 2.0      # for fixing mouse position to fit the resized display

class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("editor")
        self.screen = pygame.display.set_mode((960, 620))
        self.display = pygame.Surface((460, 310))

        self.clock = pygame.time.Clock() 

        self.assets = {
            'player': [load_image('ghost.png')],
            'target': [load_image('target.png')],
            'bell': [load_image('bell.png')],
            'button': [load_image('button.png')],
            'wall': load_images('tiles'),
           }
        
        self.movement = [False, False, False, False]


        self.tilemap = Tilemap(self, tile_size=16)
        self.level = Level(self.tilemap)

        # bit for the tilemap load [2:58]
        try:
            self.tilemap.load(self.level.get_current_level())
            print('loaded ' + self.level.get_current_level())
        except FileNotFoundError:
            print("No levels to load")

        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ctrl = False
        self.ongrid = True

        self.stack = []
        self.temp = None

    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            # camera movement
            # self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            # self.scroll[1] += (self.movement[3] - self.movement[2]) * 2

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            mpos = pygame.mouse.get_pos()

            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE) # fixs
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size), int((mpos[1] + self.scroll[1] )) // self.tilemap.tile_size)

            if self.ongrid:
                # preview or  tile indicator [2:40 - 2:47]
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[(str(tile_pos[0]) + ';' + str(tile_pos[1]))] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            
            # erase tile
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap: # if loc has tile
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)
 

            self.display.blit(current_tile_img, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid: #[2:50:00]
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift: # not properly implemented: to be fixed
                        if event.button == 4:
                            self.tile_variant = (self.tile_group - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.button == 5:
                            self.tile_variant = (self.tile_group + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                        self.stack.append(self.tilemap.tilemap.copy())
                    if event.button == 3:
                        self.right_clicking = False
                
                if event.type == pygame.KEYDOWN:
                    # camera movement
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                        print('autotiled')
                    if event.key == pygame.K_r:
                        pass

                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                    if event.key == pygame.K_LCTRL:
                        self.ctrl = True

                    # mouse substitutes and level changing buttons
                    if self.shift: # [2:36]
                        if event.key == pygame.K_LEFT:
                            self.level.change_level('-')
                        if event.key == pygame.K_RIGHT:
                            self.level.change_level('+')
                        if event.key == pygame.K_UP:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        if event.key == pygame.K_DOWN:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.key == pygame.K_UP:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                            self.tile_variant = 0
                        if event.key == pygame.K_DOWN:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0

                    if self.ctrl:
                        if event.key == pygame.K_s:
                            self.tilemap.save(self.level.get_current_level())
                            print('Saved File ' + str(self.level.current_level) + '.JSON')

                        if event.key == pygame.K_BACKSPACE:
                            self.tilemap.tilemap = {}

                        if event.key == pygame.K_z:
                            self.tilemap.tilemap = self.stack.pop().copy()
                        


                    if event.key == pygame.K_g: # grid toggle
                        self.ongrid = not self.ongrid

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
                    if event.key == pygame.K_LCTRL:
                        self.ctrl = False

            pygame.display.set_caption(self.level.get_current_level())
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()