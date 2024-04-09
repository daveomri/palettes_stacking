#!/usr/bin/python3

# Pallets stacking solver
# ---
# by David Omrai
# ---
# some description

import random
from datetime import datetime
import math
import copy
# import time
# import logging

# Change the dimentions and number of pallets
main_pallets_dim = [
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

# The pallets stacting solver - simulated annealing
class PalletsState:
  def __init__(self, *args):
    if len(args) == 3:
      self.pallets = args[0]
      self.weight = args[1]
      self.orientation = args[2]
    if len(args) == 1:
      self.pallets = copy.deepcopy(args[0].pallets)
      self.weight = args[0].weight
      self.orientation = copy.deepcopy(args[0].orientation)
    
    
class PalletsStackingSolver:
  def __init__(self, pallets_dim):  
    self.truck_width = 240
    self.pallets_dim = pallets_dim
    self.pallets_num = len(pallets_dim)
  
    # simulated annealing params
    random.seed(datetime.now().timestamp())
    
    # Algorithm params
    self.init_temp = 50.0
    self.final_temp = 0.05
    self.iter_num = self.pallets_num * 90 # force
    self.cool_factor = 0.95
    
    # self.log = logging.getLogger(__name__)
    # self.log.setLevel(logging.INFO)
    
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.INFO)
    
    # self.log.addHandler(ch)

    
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
    new_state = PalletsState(state)
    
    # with small chance of full permutation
    if (random.random() < 0.1):
      new_state.pallets = random.sample(new_state.pallets, k=len(new_state.pallets))
      new_state.weight = self.get_weight(new_state)
      return new_state
    
    # chose two palletes to swap 
    f_pallet_i = random.randint(0, len(state.pallets) - 1)
    f_pallet = new_state.pallets[f_pallet_i]
    
    s_pallet_i = random.randint(0, len(state.pallets) - 1)
    while f_pallet_i == s_pallet_i:
      s_pallet_i = random.randint(0, len(state.pallets) - 1)
    s_pallet = new_state.pallets[s_pallet_i]
    
    #swap
    new_state.pallets[f_pallet_i] = s_pallet
    new_state.pallets[s_pallet_i] = f_pallet
    
    # rotate randomly - in future - depends on how well the unrotated will perform
    rand_i = random.randint(0, len(state.orientation) - 1)
    new_state.orientation[rand_i] = (new_state.orientation[rand_i] + 1) % 2
    
    # Repair state
    new_state = self.repair_state(new_state)
    
    # Set weight
    new_state.weight = self.get_weight(new_state)
    
    return new_state
    
  """
      Method returns the total length of the palletes
  """
  def get_weight(self, state):
    total_length = 0
    curr_pallet = 0
    while curr_pallet != len(state.pallets):
      width_1 = state.orientation[state.pallets[curr_pallet]]
      length_1 = (width_1 + 1) % 2
      
      if curr_pallet == (len(state.pallets) - 1):
        # if it's the last one
        total_length += self.pallets_dim[state.pallets[curr_pallet]][length_1]
        break
      
      width_sum   = self.pallets_dim[state.pallets[curr_pallet]][width_1]
      curr_length = self.pallets_dim[state.pallets[curr_pallet]][length_1]
      next_pallet = curr_pallet + 1
      while next_pallet < len(state.pallets):
        width_j = state.orientation[state.pallets[next_pallet]]
        length_j = (width_j + 1) % 2
        
        width_sum += self.pallets_dim[state.pallets[next_pallet]][width_j]
        
        if width_sum > self.truck_width:
          # if they are too wide, sum their length
          break
        else:
          curr_length = max(curr_length, self.pallets_dim[state.pallets[next_pallet]][length_j])
        next_pallet += 1
          
      curr_pallet = next_pallet
      total_length += curr_length
    
    return total_length
  
  def repair_state(self, state):
    for i in range(0, len(state.pallets)):
      rotation = state.orientation[i]
      
      if self.pallets_dim[i][rotation] > self.truck_width:
        if self.pallets_dim[i][(rotation + 1) % 2] > self.truck_width:
          return None
        state.orientation[i] = (rotation + 1) % 2
        
    return state
    
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
    # Initialize the order of pallets [0, 1 .. n]
    top_pallets = list(range(self.pallets_num))
    top_state = PalletsState(
      top_pallets, 
      0,
      [0] * self.pallets_num
      )
    
    # Repair state - or return None if cannot be repaired
    top_state = self.repair_state(top_state)
    
    if top_state == None:
      return None
    
    top_state.weight = self.get_weight(top_state)
    
    # If only one pallet, return its best orientation
    if self.pallets_num == 1:
      if self.pallets_dim[0][0] < self.pallets_dim[0][1]:
        top_state.orientation[0] = 1
        
      top_state = self.repair_state(top_state)
      top_state.weight = self.get_weight(top_state)
      
      return top_state

    # Prepare the temperature
    steps_count = 0
    res_num = 0
    temp = self.get_weights_standard_deviation(self.get_n_weights(666, top_state))
    
    # Initialize the current state
    curr_state = PalletsState(top_state)
    
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
    
    
  def to_arr(self, state):
    out_arr = list()
    curr_length = 0
    curr_arr = list()
    for i in range(0, len(state.pallets)):
      p_id = state.pallets[i]
      p_rot = state.orientation[p_id]
      
      pal_width = self.pallets_dim[p_id][p_rot]
      pal_height = self.pallets_dim[p_id][(p_rot + 1) % 2]
      
      if curr_length + self.pallets_dim[p_id][p_rot] > self.truck_width:
        curr_length = self.pallets_dim[p_id][p_rot]
        out_arr.append(curr_arr)
        curr_arr = list()
        curr_arr.append([pal_width, pal_height])
      else:
        curr_arr.append([pal_width, pal_height])
        curr_length += self.pallets_dim[p_id][p_rot]
    
    if len(curr_arr) != 0:
      out_arr.append(curr_arr)
      
    return out_arr
    
  def run(self):
    top_state = self.sim_ann()
    if top_state == None:
      return None, None
    return self.to_arr(top_state), top_state.weight
    

if __name__ == "__main__":
  pssol = PalletsStackingSolver(main_pallets_dim)
  pssol.run()