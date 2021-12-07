import os
import sys
import numpy as np
import random
import copy
import utils
import matplotlib
matplotlib.use("AGG")
from pylab import plot, savefig
#from pylab import *
from particle import Particle
# Import the error function

from sim import fitness_function

def main():

   out_file_name = "../test/results_error.out"
   fo = open(out_file_name, "w")
   fo.write(" Starting new calculation \n")

   # Load Au coordinates
   Au_file = open('../test/coords_r5.xyz', 'r')
   lines = Au_file.readlines()
   Au_coord = []
   for line in lines:
     if 'Au ' in line:
       Au_coord.append([float(xi) for xi in line.split()[1:]])
   Au_file.close()
   Au_coord = np.array(Au_coord)

   best = []
   #--------------------------------------- Particle swarm optimization ---------------------
   # Parameters
   L = 500
   N_At = 10
   # hyper parameters
   w = 0.729    # inertia
   c1 = 1.49445 # cognitive (particle)
   c2 = 1.49445 # social (swarm)
   n = 20	# number of particles
   max_iter = 100000
   rnd = random.Random(0)
   # create n random particles
   swarm = [Particle(fitness_function,N_At, L, Au_coord) for i in range(n)]
  
   # compute the value of best_position and best_fitness in swarm
   dim = N_At
   best_swarm_pos = [0 for i in range(dim)]
   best_swarm_fitnessVal = sys.float_info.max # swarm best
  
   # computer best particle of swarm and it's fitness
   for i in range(n): # check each particle
     if swarm[i].fitness < best_swarm_fitnessVal:
       cp_best_swarm_pos = copy.deepcopy(swarm[i])
       best_swarm_fitnessVal = cp_best_swarm_pos.fitness
       best_swarm_pos = cp_best_swarm_pos.position
       best.append(best_swarm_fitnessVal)
  
   # main loop of pso
   Iter = 0
   while Iter < max_iter:
      
     if Iter % 2 == 0:
       fo.write("\n\n <<<<<<<<<<<<<<<< Beginning of a new iteration %d out of %d >>>>>>>>>>>>>>>>>>>\n\n"%((Iter),max_iter))
       fo.flush()
       fo.write("Iter = " + str(Iter) + " best fitness = %f" % best_swarm_fitnessVal)
     if Iter % 100 == 0:
       utils.write_coord(best_swarm_pos, Iter, Au_coord)

     for i in range(n): # process each particle
        
       # compute new velocity of curr particle
       for k in range(dim):
         r1 = rnd.random()    # randomizations
         r2 = rnd.random()
      
         swarm[i].velocity[k] = (
                                  (w * swarm[i].get_velocity(k)) +
                                  (c1 * r1 * (swarm[i].best_part_pos[k] - swarm[i].get_position(k))) + 
                                  (c2 * r2 * (best_swarm_pos[k] -swarm[i].get_position(k)))
                                ) 
  
       # compute new position using new velocity
       for k in range(dim):
         val = swarm[i].get_position(k) + swarm[i].get_velocity(k)
         aux = []
         for ri in val:
           if ri > L/2:
             ri = -L/2 + (ri-L/2)%L
           if ri < -L/2:
             ri = L/2 - (-ri-L/2)%L
           aux.append(ri)
         aux = np.array(aux)
         swarm[i].set_position(aux,k)
       #swarm[i].int_parameters() # Make sure that the parameters excepting lr are int values 
       # compute fitness of new position
       swarm[i].fitness = fitness_function(swarm[i].position, Au_coord)
       #print(swarm[i].fitness)
  
       # is new position a new best for the particle?
       if swarm[i].fitness < swarm[i].best_part_fitnessVal:
         cp_best_part_pos = copy.deepcopy(swarm[i])
         swarm[i].best_part_fitnessVal = cp_best_part_pos.fitness
         swarm[i].best_part_pos = cp_best_part_pos.position
       # is new position a new best overall?
       if swarm[i].fitness < best_swarm_fitnessVal:
         cp_best_swarm_pos = copy.deepcopy(swarm[i])
         best_swarm_fitnessVal = cp_best_swarm_pos.fitness
         best_swarm_pos = cp_best_swarm_pos.position
         # best vector
         best.append(best_swarm_fitnessVal)

     # for-each particle
     Iter += 1


   fo.close()
   plot(best)
   savefig('../test/error.png')	
if __name__ == "__main__":
   main()
