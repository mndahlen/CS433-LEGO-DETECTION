"""
Two classes for calculation of coordinates for brick placement:
- UniformBrickPlacer: Places brick in a uniform, non-overlapping manner(as far as possible).
- RandomBrickPlacer: Gives a random coordinate from a uniform distribution over the background size.

Both classes use the get_brick_placement(brick_width, brick_height) for calculating placement coordinate.
"""

import random

class UniformBrickPlacer(object):
    """
    Calculates coordinate for placement of brick for a uniform and sparse placement.
    
    Explanation:
    Contains two containers: Ready and Timeout. Grids are in Ready if they can be used for brick placement and in Timeout if they are not ready for brick placement.
    For a start all grids are ready. But grids are placed in timeout when they have been used. Once Ready is empty it will be refilled with all grids in timeout.
    """
    def __init__(self, width, height, n_grids_width, n_grids_height):
        self.grid_width = width/n_grids_width
        self.grid_height = height/n_grids_height
        self.grids = {}
        self.timeout = []
        self.ready = []
        self.init_grid(n_grids_width,n_grids_height)

    def init_grid(self,n_grids_width,n_grids_height):
        grid_num = 0
        for i in range(n_grids_width):
            for j in range(n_grids_height):
                self.grids[grid_num] = {"x":i,"y":j,"num_bricks":0}
                self.ready.append(grid_num)
                grid_num += 1
        self.num_grids = grid_num + 1

    def get_brick_placement(self, brick_width, brick_height):
        # Select random from ready
        grid_idx = random.choice(self.ready)
        grid = self.grids[grid_idx]

        # Remove grid from ready and add to timeout
        self.ready.remove(grid_idx)
        self.timeout.append(grid_idx)
        
        # Set x and y coord randomly within grid 
        grid_low_x = grid["x"]*self.grid_width
        grid_low_y = grid["y"]*self.grid_height
        brick_x = grid_low_x + random.randint(0, self.grid_width - brick_width)
        brick_y = grid_low_y + random.randint(0, self.grid_height - brick_height)

        # if ready is now empty, reset ready with timeout
        if not self.ready:
            self.ready = self.timeout
            self.timeout = []
                
        return (int(brick_x), int(brick_y))

class RandomBrickPlacer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def get_brick_placement(self, brick_width, brick_height):
        """
            Note that brick_width, brick_height are in this method to be compatible with the usage 
            of the corresponding method in UniformBrickPlacer.
        """
        return (random.randint(0,self.width),random.randint(0,self.height))