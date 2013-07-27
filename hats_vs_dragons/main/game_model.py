import pygame
import random

"""
The internal behavior of Hat vs Dragons.
"""

class GameChar(object):
    
    def __init__(self, hp, damage, image, location):
        self.hp = hp
        self.image = image
        self.location = location
        self.damage = damage

    def put_on_board(self):
        """
        Set-up stuff for when this character is put on board.
        """
        pass

    def turn_trigger(self, board_state):
        """
        What happens when this piece is triggered for this turn.
        Called after the piece has changed location.

        board_state is an instance of grid.
        """
        pass

    def hit(self, damage):
        self.hp -= damage

class Geek(GameChar):
    
    def __init__(self, hp, damage, image, location):
        super(Geek, self).__init__(hp, damage, image, location)

class Dragon(GameChar):
    
    def __init__(self, hp, damage, image, location):
        super(Dragon, self).__init__(hp, damage, image, location)

    def put_on_board(self):
        pass
    
    def hit_geek(self, board_state):
        """
        Hit one, and only one, geek currently in range.
        """
        # Check if there are Geeks in view
        # row check
        row = self.location[0]

        for col in range(len(board_state[row])):
            if isinstance(board_state[row][col], Geek):
                geek = board_state[row][col]
                geek.hit(damage)
                return

        # col check
        col = self.location[1]

        for row in range(len(board_state)):
            if isinstance(board_state[row][col], Geek):
                geek = board_state[row][col]
                geek.hit(damage)
                return

    def turn_trigger(self, board_state):
        self.hit_geek(board_state.grid)
        neighbors = board_state.get_adjacent()
        self.location = random.choice(neighbors)

class GameModel(object):

    def __init__(self, grid_size):
        """
        Where grid_size is (width, height)
        """
        self.grid = [[None for i in range(width)] for i in range(height)]
