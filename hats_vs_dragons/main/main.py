#! /usr/bin/env python

from components.core import Colors
from components.core import GameConfig
from components.core import GameLoop
from components.core import GameLoopEvents
from components.core import GameScreen

from game_model import GameModel
from game_model import Dragon
from game_model import HatGeek
from game_model import GunGeek

from helpers.grid import QuadraticGrid

import os
import pygame
import random

class MainScreen(GameScreen):
    
    def __init__(self, screen_size, grid_size):
        """
        grid_size is a sequence, at least 2, (width, height)
        """
        super(MainScreen, self).__init__(screen_size)
        self.gamegrid = QuadraticGrid(grid_size[0], grid_size[1])
        self.grid_width = grid_size[0]
        self.grid_height = grid_size[1]
        self.block_width = screen_size[0] / grid_size[0]
        self.block_height = screen_size[1] / grid_size[1]
        print str(self.block_width) + " " + str(self.block_height)
        
        self.game_model = GameModel(grid_size)
        self.dragon_group = pygame.sprite.Group()
        self.gun_group = pygame.sprite.Group()
        self.hat_group = pygame.sprite.Group()

    def setup(self):
        self.add_dragons()
        self.add_guns()
        
        hatguy = HatGeek(50, (0, 0))
        self.hat_group.add(hatguy)

    def __make_dragon_path(self, dragon_image):
        return os.path.join("hats_vs_dragons", "sprites", "dragons", dragon_image)

    def __make_gun_path(self, gun_image):
        return os.path.join("hats_vs_dragons", "sprites", "other_geeks", gun_image)

    def add_dragons(self, count = 20):
        # FIXME check that randomly generated cell contains None
        available_dragons = (self.__make_dragon_path("Cruel_Dragon.gif"), self.__make_dragon_path("Doom_Dragon_OW.gif"), self.__make_dragon_path("Bombander.gif"))

        for i in range(count):
            dragon_image = random.choice(available_dragons)
            dragon_row = random.choice(range(self.grid_height)) * self.block_height
            dragon_col = random.choice(range(self.grid_width)) * self.block_width
            dragon = Dragon(50, 50, dragon_image, (dragon_row, dragon_col))
            print "Dragon at: " + str((dragon_row, dragon_col))
            self.dragon_group.add(dragon)
            self.game_model.dragons.append(dragon)

    def add_guns(self, count = 10):
        available_guns = (self.__make_gun_path("apocalypse_mini.jpg"),)

        for i in range(count):
            gun_image = random.choice(available_guns)
            gun_row = random.choice(range(self.grid_height)) * self.block_height
            gun_col = random.choice(range(self.grid_width)) * self.block_width
            # FIXME GunGeek sprite hack
            gun = GunGeek(50, 50, gun_image, (gun_row, gun_col))
            print "Gun at: " + str((gun_row, gun_col))

            self.gun_group.add(gun)
            self.game_model.guns.append(gun)

    def get_rects(self):
        rect_list = []

        for i in range(self.grid_width):
            for j in range(self.grid_height):
                upper_left_x = j * self.block_width
                upper_left_y = i * self.block_height
                rect = (upper_left_x, upper_left_y, self.block_width, self.block_height)
                rect_list.append(rect)

        return rect_list

    def draw_screen(self, window):
        rects = self.get_rects()

        for r in rects:
            pygame.draw.rect(window, Colors.BLACK, r, 1)

        self.dragon_group.draw(window)
        self.gun_group.draw(window)
        self.hat_group.draw(window)

if __name__ == "__main__":
    config = GameConfig()
    config.clock_rate = 12
    config.window_size = (1357, 708)
    config.window_title = "Hats vs Dragons"

    screen = MainScreen(config.window_size, (10, 10))
    loop_events = GameLoopEvents(config, screen)
    loop = GameLoop(loop_events)
    loop.go()
