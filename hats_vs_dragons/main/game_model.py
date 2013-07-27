import pygame
import random

"""
The internal behavior of Hat vs Dragons.
"""

# FIXME Hahaha....dragons can't hit dragons, geeks can't hit geeks.

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

    def turn_trigger(self, board_state, location):
        """
        What happens when this piece is triggered for this turn.
        Called after the piece has changed location.

        board_state is an instance of grid.
        location is new coordinates.
        """
        pass

    def hit(self, damage):
        self.hp -= damage

class Geek(GameChar):
    
    def __init__(self, hp, damage, image, location):
        super(Geek, self).__init__(hp, damage, image, location)

class  HatGeek(Geek):
    def __init__(self, hp, location):
        """
        Hat can have variable HP, and location but fixed 0 damage and
        fixed image.
        """
        image = os.path.join("hats_vs_dragons", "sprites", "blackhat", "blackhat.png")
        super(HatGeek, self).__init__(hp, 0, image, location)

class GunGeek(Geek):
    """
    We can have many guns. But for now we'll just use the LHC for our gun.
    """

    def __init__(self, hp, damage, image, location):
        # Whatever happens, we'll load the LHC image.
        lhc_image = os.path.join("hats_vs_dragons", "sprites", "other_geeks", "apocalypse.jpg")
        super(GunGeek, self).__init__(hp, damage, lhc_image, location)
    
    def turn_trigger(self, board_state, location):
        """
        Note: Only HatGeek can trigger gun geeks.

        Hit one, and only one, geek in range.
        """
        grid = board_state.grid
        row = self.location[0]

        for col in range(len(grid[row])):
            if isinstance(grid[row][col], Dragon):
                dragon = grid[row][col]
                dragon.hit(damage)
                return

        col = self.location[1]

        for row in range(len(grid)):    
            if isinstance(grid[row][col], Dragon):
                dragon = grid[row][col]
                dragon.hit(damage)
                return


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

    def turn_trigger(self, board_state, location):
        self.hit_geek(board_state.grid)
        self.location = location

class GameModel(object):
    """
    Note that we consider our guns as geeks.
    """

    def __init__(self, grid_size):
        """
        Where grid_size is (width, height)
        """
        self.board = [[None for i in range(width)] for i in range(height)]
        # Location list of all dragons in the game
        self.dragons = []
        # Location list of all geeks 
        self.geeks = []

    def ai_turn(self):
        """
        For the AI's turn, just trigger all dragons in the board.
        """
        for dragon in self.dragons:
            dragon_location = dragon.location
            neighbors = self.board.neighbors(dragon_location[0], dragon_location[1])
            dragon.turn_trigger(self.board, random.choice(neighbors))
