#!/usr/bin/python3

# Pallets stacking solver
# ---
# by David Omrai
# ---
# some description - todo

import random
from datetime import datetime
import math
import copy

# Change the dimentions and number of pallets
main_pallets_dim: list[list[int]] = [
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
      self.pallets: list[list[int]] = args[0]
      self.weight: int = args[1]
      self.orientation: list[int] = args[2]
    if len(args) == 1:
      self.pallets: list[list[int]] = copy.deepcopy(args[0].pallets)
      self.weight: int = args[0].weight
      self.orientation: list[int] = copy.deepcopy(args[0].orientation)
    
class PalletsStackingSolver:
  """ Class represents the pallets stacking solver
  """
  def __init__(self, pallets_dim: int, truck_width: int) -> None:  
    self.truck_width: int = truck_width
    self.pallets_dim: int = pallets_dim
    self.pallets_num: int = len(pallets_dim)
  
    # simulated annealing params
    random.seed(datetime.now().timestamp())
    
    # Algorithm params
    self.init_temp: float = 50.0
    self.final_temp: float = 0.05
    self.iter_num: int = self.pallets_num * 90 # force
    self.cool_factor: float = 0.95
    
    # old code
    # self.log = logging.getLogger(__name__)
    # self.log.setLevel(logging.INFO)
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.INFO)
    # self.log.addHandler(ch)
    
  # Setters
  def set_init_temp(self, init_temp: float):
    self.init_temp = init_temp
    
  def set_final_temp(self, final_temp: float):
    self.final_temp = final_temp
    
  def set_iter_num(self, iter_num: int):
    self.iter_num = iter_num
    
  def set_cool_factor(self, cool_factor: float):
    self.cool_factor = cool_factor
    
  # - - - - - - - - - - - - - - - - - - - -
  
  def get_n_weights(self, n_weights: int, state: PalletsState) -> list[int]:
    """ Method returns N weights of random neighbour states.

    Args:
        n_weights (int): Number of weights to return.
        state (PalletsState): Current state for which to find neighbour weights.

    Returns:
        [int]: N neighbour weights.
    """
    weights: list[int] = list()
    
    for _ in range(0, n_weights):
      weights.append(self.get_weight(self.get_random_neighbour(state)))
      
    return sorted(weights)
  
  def get_weights_standard_deviation(self, weights: list[int]) -> float:
    """ sx = ( Sum_[i=1, n]((x_i - mean_x)^2) / (n - 1) )^0.5

    Args:
        weights ([int]): List of state weights.

    Returns:
        float: _description_
    """
    mean_w: float = sum(weights) / len(weights)
    numerator: int = 0
    denominator: int = len(weights) - 1
    
    for weight in weights:
      numerator += math.pow(weight - mean_w, 2)
    
    return math.sqrt(numerator / denominator)    
    
  # - - - - - - - - - - - - - - - - - - - -
  
  def get_random_neighbour(self, state: PalletsState) -> PalletsState:
    """ Method returns a neighbour state of given state.

    Args:
        state (PalletsState): State for which to find a neighbour.

    Returns:
        PalletsState: A neighbour state.
    """
    new_state: PalletsState = PalletsState(state)
    
    # with small chance of full permutation
    if (random.random() < 0.1):
      new_state.pallets = random.sample(new_state.pallets, k=len(new_state.pallets))
      new_state.weight = self.get_weight(new_state)
      return new_state
    
    # chose two palletes to swap 
    f_pallet_i: int = random.randint(0, len(state.pallets) - 1)
    f_pallet: int = new_state.pallets[f_pallet_i]
    s_pallet_i: int = random.randint(0, len(state.pallets) - 1)
    
    while f_pallet_i == s_pallet_i:
      s_pallet_i = random.randint(0, len(state.pallets) - 1)
    
    s_pallet: int = new_state.pallets[s_pallet_i]
    
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
    
  def get_weight(self, state: PalletsState) -> int:
    """
      Method returns the total length of the palletes
      -- doens't consider variable orderring of the palletes (each row is final, no next pallete can
      -- fit to the possible openings left behind by previous ones)
    """
    total_length: int = 0
    curr_pallet: int = 0
    while curr_pallet != len(state.pallets):
      width_1: int = state.orientation[state.pallets[curr_pallet]]
      length_1: int = (width_1 + 1) % 2
      
      if curr_pallet == (len(state.pallets) - 1):
        # if it's the last one
        total_length += self.pallets_dim[state.pallets[curr_pallet]][length_1]
        break
      
      width_sum: int   = self.pallets_dim[state.pallets[curr_pallet]][width_1]
      curr_length: int = self.pallets_dim[state.pallets[curr_pallet]][length_1]
      next_pallet: int = curr_pallet + 1
      while next_pallet < len(state.pallets):
        width_j: int = state.orientation[state.pallets[next_pallet]]
        length_j: int = (width_j + 1) % 2
        
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
  
  def repair_state(self, state: PalletsState) -> PalletsState:
    """
        Repair palletes, where the dimension of palletes
        cannot fit into a truck. In this case rotate the pallete.

    Args:
        state ([[int]]): current state of palletes

    Returns:
        [[int]]: repaired state
    """
    for i in range(0, len(state.pallets)):
      rotation: int = state.orientation[i]
      
      if self.pallets_dim[i][rotation] > self.truck_width:
        if self.pallets_dim[i][(rotation + 1) % 2] > self.truck_width:
          # if none dimension of pallete is able to fit, return null
          raise ValueError('Given state is invalid.')
        state.orientation[i] = (rotation + 1) % 2
        
    return state
    
  def accept_worse(self, curr_state_weight: int, old_state_weight: int, temp: float) -> bool:
    """
        Function decides whether to accept the worse solution
        based on the probability and temperature.

    Args:
        curr_state_weight (int): Weight of the current state
        old_state_weight (int): Weight of the previous state
        temp (float): Temperature of SA

    Returns:
        bool: True if to accept, False otherwise
    """
    if temp == 0:
      return False
    
    # old code
    # delta = abs(old_state_weight - curr_state_weight)
    # accept_prob = 1 / (1 + math.exp( delta / temp))
    # return random.uniform(0, 1) < accept_prob
    
    # normalise the weights
    eps: int =  old_state_weight - curr_state_weight
    
    try: 
      return random.uniform(0, 1) < 1 / (1 + math.exp(abs(eps) / temp))
    except OverflowError:
      return False
    
  def sim_ann(self) -> PalletsState:  
    """
        Method represents the simulated annealing heuristics for 
        finding the best state for palletes organisation as possible

    Returns:
        PalletsState: Returns best found state
    """
    # Initialize the order of pallets [0, 1 .. n]
    top_pallets: list[int] = list(range(self.pallets_num))
    top_state: PalletsState = PalletsState(
      top_pallets, 
      0,
      [0] * self.pallets_num
      )
    
    # Repair state - or return None if cannot be repaired
    try:
      top_state: PalletsState = self.repair_state(top_state)
    except ValueError as value_error:
      raise ValueError(repr(value_error))
    
    top_state.weight = self.get_weight(top_state)
    
    # If only one pallet, return its best orientation
    if self.pallets_num == 1:
      if self.pallets_dim[0][0] < self.pallets_dim[0][1]:
        top_state.orientation[0] = 1
        
      top_state = self.repair_state(top_state)
      top_state.weight = self.get_weight(top_state)
      
      return top_state

    # steps_count = 0
    # res_num = 0
    # Prepare the temperature
    temp: float = self.get_weights_standard_deviation(self.get_n_weights(666, top_state))
    
    # Initialize the current state
    curr_state: PalletsState = PalletsState(top_state)
    
    # start the annealing
    while temp > self.final_temp:
      
      # repeat the selection for this temperature
      for _ in range(0, self.iter_num):
        new_state: PalletsState = self.get_random_neighbour(curr_state)
        
        # update the best state
        if top_state.weight > new_state.weight:
          top_state = new_state
        
        # Decide wheter to accept or not
        if new_state.weight <= curr_state.weight or self.accept_worse(new_state.weight, curr_state.weight, temp):
          # increase the number of results
          # res_num += 1
          # store the new state
          curr_state = new_state
        
          # self.log.critical("{} {} {} {}".format(res_num, steps_count, temp, curr_state.weight))

      # decreas the temperature
      temp *= self.cool_factor
      
      # old code
      # steps_count += 1
    
    return top_state
    
    
  def to_arr(self, state: PalletsState) -> list[list[int]]:
    """Method turns the given state into an array representation

    Args:
        state (PalletsState): todo

    Returns:
        [[int]]: _description_
    """
    out_arr: list[list[int]] = list()
    curr_length: int = 0
    curr_arr: list[int] = list()
    
    for i in range(0, len(state.pallets)):
      p_id: int = state.pallets[i]
      p_rot: int = state.orientation[p_id]
      
      pal_width: int = self.pallets_dim[p_id][p_rot]
      pal_height: int = self.pallets_dim[p_id][(p_rot + 1) % 2]
      
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
    
  def run(self) -> tuple[[[int]], int]:
    try:
      top_state: PalletsState = self.sim_ann()
      return self.to_arr(top_state), top_state.weight
    except ValueError:
      return None, None
    

if __name__ == "__main__":
  pssol = PalletsStackingSolver(main_pallets_dim, 240)
  pssol.run()