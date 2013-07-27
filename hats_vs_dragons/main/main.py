#! /usr/bin/env python

from components.core import Colors
from components.core import GameConfig
from components.core import GameLoop
from components.core import GameLoopEvents
from components.core import GameScreen

from helpers.grid import QuadraticGrid

import pygame

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

    def get_rects(self):
        rect_list = []

        for i in range(self.grid_width):
            for j in range(self.grid_height):
                upper_left_x = j * self.block_width
                upper_left_y = i * self.block_height
                rect = (upper_left_x, upper_left_y, self.block_width, self.block_height)
                rect_list.append(rect)
                
                if raw_grid[i][j] == ColorBlocksModel.UNTAKEN:
                    self.color_list.append(Colors.WHITE)
                else:
                    color_index = int(raw_grid[i][j])
                    self.color_list.append(ColorBlocksScreen.COLOR_MAPPING[color_index])

        return rect_list

    def draw_screen(self, window):
        """
        """
        pass

if __name__ == "__main__":
    config = GameConfig()
    config.clock_rate = 12
    config.window_size = (1000, 1000)
    config.window_title = "Hats vs Dragons"

    screen = GameScreen(config.window_size, (10, 10))
    loop_events = GameLoopEvents(config, screen)
    loop = GameLoop(loop_events)
    loop.go()
