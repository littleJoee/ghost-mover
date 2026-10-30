import pygame
import json
import os

from data.scripts.tilemap import Tilemap

BASE_LEVEL_PATH = 'data/maps/'

class Level:
    def __init__(self, tilemap: Tilemap):
        self.current_level = 0
        self.tilemap = tilemap
        self.editor_special_case = False
        self.no_of_levels = self.get_level_len()

    def get_current_level(self):
        return str(self.current_level) + '.json'

    def get_level_len(self):
        return len(os.listdir(BASE_LEVEL_PATH))

    def won(self):
        print(self.current_level, self.no_of_levels - 2)
        if self.current_level <= self.no_of_levels - 2:
            self.current_level += 1
            return True
        print('Finished Game')
        # self.current_level = 'game_over' TODO gameover level with text spawner and total 
        # time spent under that
        return False
    

    def save_level(self, custom=None):
        if custom:
            self.tilemap.save(str(custom) + '.json')
            return
        self.tilemap.save(str(self.current_level) + '.json')

    def change_level(self, change):
        self.tilemap.save(str(self.current_level) + '.json')

        if change == '+':
            if self.current_level != self.get_level_len() + 1:
                self.current_level += 1
            try:
                self.tilemap.load(str(self.current_level) + '.json')
            except FileNotFoundError:
                self.tilemap.save(str(self.current_level) + '.json')
                self.tilemap.load(str(self.current_level) + '.json')
        if change == '-':
            self.current_level = max(0, self.current_level - 1)
            self.tilemap.load(str(self.current_level) + '.json')
