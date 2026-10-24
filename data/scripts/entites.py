from pygame import Surface
from .utils import lerp

import pygame

class SpecialPlayerTargets:
    # for more complex target movers
    def __init__(self, player_pos, variants=0):
        self.layers_avail = variants
        self.offset_layer = [
            [-1, 0], [0, 1], [1, 0], [0, -1], # first
            [-2, 0], [0, 2], [2, 0], [0, -2], # second
        ]

        self.pos = player_pos

    def generate_target_pos(self):
        self.target_pos = []
        for i in len(range(self.layers_avail)):
            for target in self.offset_layer[i]:
                target: list[int, int]
                self.offset_pos.append(target)

    def update(self, movement, list_of_entities):
        self.generate_target_pos()


    def find_adjacent_target(self, pos):
        pass

class Entity:
    def __init__(self, game, pos, e_type):
        self.game = game
        self.pos = list(pos)
        self.type = e_type
        self.timer = 0
        self.offsets = [[-1, 0], [0, 1], [1, 0], [0, -1], # first layer
                        [-2, 0], [0, 2], [2, 0], [0, -2]] # second layer

    def rect(self, pos=None):
        if pos:
            return pygame.Rect(pos[0], pos[1], 16, 16)
        return pygame.Rect(self.pos[0], self.pos[1], 16, 16)

    def wall_check(self, pos):
        tiles: dict = self.game.tilemap.get_type('wall')
        if f"{pos[0]};{pos[1]}" in tiles:
            return True

    def update(self, movement=(0,0)):
        self.timer = max(0, self.timer - 1)

        if movement[0] and self.timer == 0:
            self.pos[0] += movement[0] * 16
            self.timer += 5
        if movement[1] and self.timer == 0:
            self.pos[1] += movement[1] * 16
            self.timer += 5

    def render(self, surf: Surface):
        surf.blit(self.game.assets[self.type], self.pos)   

class Bell(Entity):
    def __init__(self, game, pos):
        super().__init__(game, pos, 'bell')
        self.action = False
        self.target_index = None
        self.timer = 0
        self.max_timer = 20

    def can_move(self, targets):
        self.timer = max(0, self.timer - 1)
    
        # from 0 to 3
        if self.target_index <= 3:
            if self.target_index == 3:
                next_pos = targets[0]
            else:
                next_pos = targets[self.target_index + 1]

        # from 4 to 7
        if self.target_index >= 4:
            if self.target_index == 7:
                next_pos = targets [4]
            else:
                next_pos = targets[self.target_index + 1]

        if self.game.action and self.timer == 0:
            self.pos = next_pos
            self.timer = self.max_timer
        

class Player(Entity):
    def __init__(self, game, pos, e_type):
        super().__init__(game, pos, 'player')
        self.moving = False

    def update(self, entities: list[Bell], movement=(0, 0)):
        super().update(movement)
        entity_rect = self.rect()
        for rects in entities:
            if entity_rect.colliderect(rects):
                self.pos[0] -= movement[0] * 16
                self.pos[1] -= movement[1] * 16
            
        self.targets = []
        bells_to_move = []
        for i, offset in enumerate(self.offsets):
            offset_pos = [self.pos[0] + offset[0] * 16, self.pos[1] + offset[1] * 16]
            self.targets.append(offset_pos.copy())
            for rect in entities:
                if self.rect(offset_pos).colliderect(rect):
                    rect.target_index = i
                    bells_to_move.append(rect)
        for bell in bells_to_move:
            bell.can_move(self.targets)
        

    def render(self, surf):
        super().render(surf)
        for offset_pos in self.targets:
            surf.blit(self.game.assets['target'], offset_pos)




    