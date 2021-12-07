import copy, numpy as np, random

class Particle:

    def __init__(self, puti_error, N_At, L, Au_coord):
        dim = N_At
        self.position = np.array([ [ np.random.uniform(-L / 5, L / 5) for xi in range(3) ] for i in range(dim) ])
        self.velocity = np.array([ [ np.random.normal(0, L / 10) for xi in range(3) ] for i in range(dim) ])
        self.best_part_pos = np.array([ [ 0.0 for xi in range(3) ] for i in range(dim) ])
        self.fitness = puti_error(self.position, Au_coord)
        self.best_part_pos = np.array([ i for i in self.position ])
        self.best_part_fitnessVal = self.fitness

    def set_position(self, new_val, k):
        self.position[k] = new_val

    def set_velocity(self, new_val, k):
        self.velocity[k] = new_val

    def get_position(self, k):
        return self.position[k]

    def get_velocity(self, k):
        return self.velocity[k]
# okay decompiling particle.pyc
