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
class PalettesState:
  def __init__(self, *args):
    if len(args) == 3:
      self.palettes = args[0]
      self.weight = args[1]
      self.orientation = args[2]
    if len(args) == 1:
      self.palettes = copy.deepcopy(args[0].palettes)
      self.weight = args[0].weight
      self.orientation = copy.deepcopy(args[0].orientation)
    
    
class PalettesStackingSolver:
  def __init__(self, palettes_dim):  
    self.truck_width = 240
    self.palettes_dim = palettes_dim
    self.palettes_num = len(palettes_dim)
  
    # simulated annealing params
    random.seed(datetime.now().timestamp())
    
    # Algorithm params
    self.init_temp = 50.0
    self.final_temp = 0.05
    self.iter_num = self.palettes_num * 90 # force
    self.cool_factor = 0.95
    
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
    new_state = PalettesState(state)
    
    # with small chance of full permutation
    if (random.random() < 0.1):
      new_state.palettes = random.sample(new_state.palettes, k=len(new_state.palettes))
      new_state.weight = self.get_weight(new_state)
      return new_state
    
    # chose two palletes to swap 
    f_palette_i = random.randint(0, len(state.palettes) - 1)
    f_palette = new_state.palettes[f_palette_i]
    
    s_palette_i = random.randint(0, len(state.palettes) - 1)
    while f_palette_i == s_palette_i:
      s_palette_i = random.randint(0, len(state.palettes) - 1)
    s_palette = new_state.palettes[s_palette_i]
    
    #swap
    new_state.palettes[f_palette_i] = s_palette
    new_state.palettes[s_palette_i] = f_palette
    
    # rotate randomly - in future - depends on how well the unrotated will perform
    rand_i = random.randint(0, len(state.orientation) - 1)
    new_state.orientation[rand_i] = (new_state.orientation[rand_i] + 1) % 2
    
    new_state.weight = self.get_weight(new_state)
    return new_state
    
  """
      Method returns the total length of the palletes
  """
  def get_weight(self, state):
    total_length = 0
    curr_palette = 0
    while curr_palette != len(state.palettes):
      width_1 = state.orientation[state.palettes[curr_palette]]
      length_1 = (width_1 + 1) % 2
      
      if curr_palette == (len(state.palettes) - 1):
        # if it's the last one
        total_length += self.palettes_dim[state.palettes[curr_palette]][length_1]
        break
      
      width_sum   = self.palettes_dim[state.palettes[curr_palette]][width_1]
      curr_length = self.palettes_dim[state.palettes[curr_palette]][length_1]
      next_palette = curr_palette + 1
      while next_palette < len(state.palettes):
        width_j = state.orientation[state.palettes[next_palette]]
        length_j = (width_j + 1) % 2
        
        width_sum += self.palettes_dim[state.palettes[next_palette]][width_j]
        
        if width_sum > self.truck_width:
          # if they are too wide, sum their length
          break
        else:
          curr_length = max(curr_length, self.palettes_dim[state.palettes[next_palette]][length_j])
        next_palette += 1
          
      curr_palette = next_palette
      total_length += curr_length
    
    return total_length
    
  def accept_worse(self, curr_state_weight, old_state_weight, temp):
    if temp == 0:
      return False
    
    # delta = abs(old_state_weight - curr_state_weight)
    # accept_prob = 1 / (1 + math.exp( delta / temp))
    
    # normalise the weights
    eps =  old_state_weight - curr_state_weight
    
    try: 
      return random.uniform(0, 1) < 1 / (1 + math.exp(abs(eps) / temp))
    except:
      return False
    # return random.uniform(0, 1) < accept_prob
    
  def sim_ann(self):    
    # Initialize the order of palettes [0, 1 .. n]
    top_palettes = list(range(self.palettes_num))
    top_state = PalettesState(
      top_palettes, 
      0,
      [0] * self.palettes_num
      )
    top_state.weight = self.get_weight(top_state)

    # Prepare the temperature
    steps_count = 0
    res_num = 0
    temp = self.get_weights_standard_deviation(self.get_n_weights(666, top_state))
    
    # Initialize the current state
    curr_state = PalettesState(top_state)
    
    # start the annealing
    while temp > self.final_temp:
      
      # repeat the selection for this temperature
      for _ in range(0, self.iter_num):
        new_state = self.get_random_neighbour(curr_state)
        
        # update the best state
        if top_state.weight > new_state.weight:
          top_state = new_state
        
        # Decide wheter to accept or not
        if new_state.weight <= curr_state.weight or self.accept_worse(new_state.weight, curr_state.weight, temp):
          # increase the number of results
          res_num += 1
          # store the new state
          curr_state = new_state
        
          # self.log.critical("{} {} {} {}".format(res_num, steps_count, temp, curr_state.weight))

      # decreas the temperature
      temp *= self.cool_factor
      
      steps_count += 1
    
    return top_state
    
    
  def to_string(self, state):
    output = "length: {}\n[".format(state.weight)
    curr_length = 0
    for i in range(0, len(state.palettes)):
      p_id = state.palettes[i]
      p_rot = state.orientation[p_id]
      rot_sym = 'r' if p_rot == 1 else ''
      if curr_length + self.palettes_dim[p_id][p_rot] >= self.truck_width:
        curr_length = self.palettes_dim[p_id][p_rot]
        output = '{} ]\n[ {}{}'.format(output, p_id + 1, rot_sym)
      else:
        curr_length += self.palettes_dim[p_id][p_rot]
        output = '{} {}{}'.format(output, p_id + 1, rot_sym)
    output = '{} ]\n'.format(output)
    
    return output
    
  def run(self):
    if (self.palettes_num == 1):
      return 'One palette'
    return self.to_string(self.sim_ann())
    # print("{} {} {}".format(
    #   top_state.weight, steps_count, duration))
    # print(top_state.palettes)
    # print(top_state.orientation)
    

if __name__ == "__main__":
  pssol = PalettesStackingSolver(main_palettes_dim)
  pssol.run()