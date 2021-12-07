import random

class UniformBrickPlacer(object):
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
                self.grids[0] = {"x":i,"y":j,"num_bricks":0}
                self.ready.append(grid_num)
                grid_num += 1
        self.num_grids = grid_num + 1

    def get_brick_placement(self):
        # Select random from ready
        grid_idx = random.choice(self.ready)
        grid = self.grids[grid_idx]

        # Remove grid from ready and add to timeout
        self.ready.remove(grid_idx)
        self.timeout.append(grid_idx)
        
        # Set x and y coord randomly within grid 
        grid_low_x = grid["x"]*self.grid_width
        grid_low_y = grid["y"]*self.grid_width
        rand_x_frac = random.uniform(0, 1)
        rand_y_frac = random.uniform(0, 1)
        brick_x = grid_low_x + rand_x_frac*self.grid_width
        brick_y = grid_low_y + rand_y_frac*self.grid_height

        # if ready is now empty, reset ready with timeout
        if not self.ready:
            self.ready = self.timeout
            self.timeout = []
                
        return (brick_x, brick_y)