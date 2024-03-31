#!/usr/bin/python3

# Palettes stacking solver
# ---
# by David Omrai
# ---
# some description

import random
from datetime import datetime
import math
import copy
import time
import logging

# Change the dimentions and number of palettes
main_palettes_dim = [
  [150, 110],
  [125, 85],
  [125, 105],
  [125, 115],
  [125, 120],
  [165, 145],
  [145, 145],
  [90, 90],
  [115, 115],
  [140, 125]
]

# The palettes stacting solver - simulated annealing
class PalettesStackingSolver:
  def __init__(self, palettes_dim):  
    self.truck_width = 240
    self.palettes_dim = palettes_dim
    self.palettes_num = len(palettes_dim)
    self.palettes_rotation = [0] * self.palettes_num
  
    # simulated annealing params
    random.seed(datetime.now().timestamp())
    
    # Algorithm params
    self.init_temp = 50.0
    self.final_temp = 0.05
    self.iter_num = 1000
    self.cool_factor = 0.98
    
    self.log = logging.getLogger(__name__)
    self.log.setLevel(logging.INFO)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    self.log.addHandler(ch)

    
  # Setters
  def set_init_temp(self, init_temp):
    self.init_temp = init_temp
    
  def set_final_temp(self, final_temp):
    self.final_temp = final_temp
    
  def set_iter_num(self, iter_num):
    self.iter_num = iter_num
    
  def set_cool_factor(self, cool_factor):
    self.cool_factor = cool_factor
    
  # - - - - - - - - - - - - - - - - - - - -
  
  def get_n_weights(self, n_weights, state):
    weights = list()
    
    for _ in range(0, n_weights):
      weights.append(self.get_weight(self.get_random_neighbour(state)))
      
    return sorted(weights)
  
  
  """
      sx = ( Sum_[i=1, n]((x_i - mean_x)^2) / (n - 1) )^0.5
  """
  def get_weights_standard_deviation(self, weights):
    mean_w = sum(weights) / len(weights)
    numerator = 0
    denominator = len(weights) - 1
    
    for weight in weights:
      numerator += math.pow(weight - mean_w, 2)
    
    return math.sqrt(numerator / denominator)
    
    
    
  # - - - - - - - - - - - - - - - - - - - -
  
  def get_random_neighbour(self, state):
    new_state = copy.deepcopy(state)
    
    # with small chance of full permutation
    if (random.random() < 0.1):
      return random.sample(new_state, k=len(new_state))
    
    # chose two palletes to swap 
    f_palette_i = random.randint(0, len(state) - 1)
    f_palette = new_state[f_palette_i]
    
    s_palette_i = random.randint(0, len(state) - 1)
    while f_palette_i == s_palette_i:
      s_palette_i = random.randint(0, len(state) - 1)
    s_palette = new_state[s_palette_i]
    
    #swap
    new_state[f_palette_i] = s_palette
    new_state[s_palette_i] = f_palette
    
    # rotate randomly - in future - depends on how well the unrotated will perform
    
    return new_state
    
  """
      Method returns the total length of the palletes
  """
  def get_weight(self, state):
    total_length = 0
    for i in range(0, len(state), 2):
      # par_length_1 = self.palettes_rotation[i]
      # par_length_2 = self.palettes_rotation[i + 1]
      
      if i == (len(state) - 1):
        # if it's the last one
        total_length += self.palettes_dim[state[i]][1]
      elif (self.palettes_dim[state[i]][0] + self.palettes_dim[state[i + 1]][0] > self.truck_width):
        # if they are too wide, sum their length
        total_length += self.palettes_dim[state[i]][1] + self.palettes_dim[state[i + 1]][1]
      else:
        total_length += max(self.palettes_dim[state[i]][1], self.palettes_dim[state[i + 1]][1])
    
    return total_length
    
  def accept_worse(self, curr_state_weight, old_state_weight, temp):
    if temp == 0:
      return False
    
    # delta = abs(old_state_weight - curr_state_weight)
    # accept_prob = 1 / (1 + math.exp( delta / temp))
    
    # normalise the weights
    eps =  old_state_weight - curr_state_weight
    return random.uniform(0, 1) < math.exp(- (eps) / temp)
    # return random.uniform(0, 1) < accept_prob
    
  def sim_ann(self):    
    # Initialize the order of palettes [0, 1 .. n]
    top_state = list(range(self.palettes_num))
    top_state_weight = self.get_weight(top_state)
    
    # Prepare the temperature
    steps_count = 0
    res_num = 0
    temp = self.get_weights_standard_deviation(self.get_n_weights(666, top_state))
    
    # Initialize the current state
    curr_state = copy.deepcopy(top_state)
    curr_state_weight = top_state_weight
    
    # start the annealing
    while temp > self.final_temp:
      
      # repeat the selection for this temperature
      for _ in range(0, self.iter_num):
        new_state = self.get_random_neighbour(curr_state)
        new_state_weight = self.get_weight(new_state)
        
        # update the best state
        if top_state_weight < new_state_weight:
          top_state = new_state
          top_state_weight = new_state_weight
        
        # Decide wheter to accept or not
        if new_state_weight <= curr_state_weight or self.accept_worse(new_state_weight, curr_state_weight, temp):
          # increase the number of results
          res_num += 1
          # store the new state
          curr_state = new_state
          curr_state_weight = new_state_weight
        
          self.log.critical("{} {} {} {}".format(res_num, steps_count, temp, curr_state_weight))

      # decreas the temperature
      temp *= self.cool_factor
      
      steps_count += 1
    
    return top_state, top_state_weight, steps_count    
    
  def run(self):
    start_time = time.time()
    top_state, top_state_weight, steps_count = self.sim_ann()
    duration = time.time() - start_time
    
    print("{} {} {}".format(
      top_state_weight, steps_count, duration))
    print(top_state)
    

if __name__ == "__main__":
  pssol = PalettesStackingSolver(main_palettes_dim)
  pssol.run()