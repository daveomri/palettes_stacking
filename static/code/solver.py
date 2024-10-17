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
  truck_size: int = 240
  pallets_dimensions: list[int] = []
  pallets_num: int = 0
  
  def __init__(self, *args):
    if len(args) == 3:
      self._pallets: list[list[int]] = args[0]
      self._weight: int = args[1]
      self._orientation: list[int] = args[2]
    if len(args) == 1:
      self._pallets: list[list[int]] = copy.deepcopy(args[0].pallets)
      self._weight: int = args[0].weight
      self._orientation: list[int] = copy.deepcopy(args[0].orientation)
      
  @property
  def pallets(self):
    return self._pallets
  
  @property
  def weight(self):
    return self._weight
  
  @property
  def orientation(self):
    return self._orientation
  
  @pallets.setter
  def pallets(self, value):
    self._pallets = value
    
  @weight.setter
  def weight(self, value):
    self._weight = value
  
  @orientation.setter
  def orientation(self, value):
    self._orientation = value
    
  def set_pallet_orientation(self, p_id, value) -> None:
    self.orientation[p_id] = value
    
  def get_pallet_orientation(self, p_id):
    return self.orientation[p_id]
    
  def get_pallet_dim(self, p_id, dim_id) -> int:
    return self.pallets_dimensions[p_id][dim_id]
  
  def get_pallet_dims(self, p_id) -> (int, int):
    width_id: int = self.orientation[self._pallets[p_id]]
    length_id: int = (width_id + 1) % 2
    
    p_width: int   = self.pallets_dimensions[self._pallets[p_id]][width_id]
    p_length: int = self.pallets_dimensions[self._pallets[p_id]][length_id]
  
    return p_width, p_length
  
  def repair_state(self) -> None:
    """
        Repair palletes, where the dimension of palletes
        cannot fit into a truck. In this case rotate the pallete.

    Returns:
        [[int]]: repaired state
    """
    for i in range(0, len(self._pallets)):
      rotation: int = self.get_pallet_orientation(i)
      
      if self.get_pallet_dim(i, rotation) > self.truck_width:
        if self.get_pallet_dim(i, rotation(rotation + 1) % 2) > self.truck_width:
          # if none dimension of pallete is able to fit, return null
          raise ValueError('Given state is invalid.')
        self.set_pallet_orientation(i, (rotation + 1) % 2)
      
  def get_old_weight(self) -> int:
    """
      Method returns the total length of the palletes
      -- doens't consider variable orderring of the palletes (each row is final, no next pallete can
      -- fit to the possible openings left behind by previous ones)
    """
    total_length: int = 0
    curr_pallet: int = 0
    prev_pallets: list(list(int)) = []
    while curr_pallet != len(self.pallets):
      curr_p_width, curr_p_length = self.get_pallet_dims(curr_pallet)
      curr_pallets: list(list(int)) = [[curr_p_width, curr_p_length]]
      
      width_sum = curr_p_width
      
      next_pallet: int = curr_pallet + 1
      
      if curr_pallet == (len(self.pallets) - 1):
        # if it's the last one
        total_length += curr_p_length
        break
      
      while next_pallet < len(self.pallets):        
        next_p_width, next_p_length = self.get_pallet_dims(next_pallet)
        
        width_sum += next_p_width
        
        if width_sum > self.truck_width:
          # if they are too wide, sum their length
          break
        else:
          curr_pallets.append(next_pallet)
          curr_p_length = max(curr_p_length, next_p_length)
        next_pallet += 1
          
          
      # todo shift the pallets
      
      curr_pallet = next_pallet
      total_length += curr_p_length
    
    return total_length
  
  def get_weight(self) -> int:
    prev_row_widths: list[list[int]] = []
    prev_row_lengths: list[list[int]] = []
    
    curr_row_widths: list[int] = []
    curr_row_lengths: list[int] = []
    row_width: int = 0
    
    for pal_id in range(len(self.pallets)):
      curr_width, curr_length = self.get_pallet_dims(pal_id)
      
      if (row_width + curr_width > self.truck_size):
        if (row_width != self.truck_size):
          # tohle vyplni prazdno jednim blokem, ale volne misto by se dalo
          # rozdelit podle palet pred
          # todo, koukni na lengths predchozich v gapu a podle toho gap rozdel
          gap_width = self.truck_size - row_width
          curr_row_widths.append(gap_width)
          curr_row_lengths.append(self.get_prev_row_length(
            prev_row_widths, prev_row_lengths, row_width, gap_width
          ))
        
        prev_row_widths = curr_row_widths
        prev_row_lengths = curr_row_lengths
        
        row_width = 0
        curr_row_lengths = []
        curr_row_widths = []
        
      
      curr_row_widths.append(curr_width)
      curr_length =  curr_length + self.get_prev_row_length(
        prev_row_widths, prev_row_lengths, row_width, curr_width
      )
      curr_row_lengths.append(curr_length)
      
      row_width += curr_width
      
    # muze se to nerovnat?
    if row_width != 0:
      gap_width = self.truck_size - row_width
      curr_row_widths.append(gap_width)
      curr_row_lengths.append(self.get_prev_row_length(
        prev_row_widths, prev_row_lengths, row_width, gap_width
      ))
    
    
    return max(curr_row_lengths)
    
  def get_prev_row_length(self, prev_row_widths, prev_row_lengths, pal_left_pos, pallet_width):
    if len(prev_row_lengths) == 0:
      return 0
    
    top_length = 0
    cur_left_marg = 0
    
    for pal_id in range(len(prev_row_widths)):
      if cur_left_marg < pal_left_pos + pallet_width and cur_left_marg + prev_row_widths[pal_id] > pal_left_pos:
        top_length = max(top_length, prev_row_lengths[pal_id])
        
      cur_left_marg += prev_row_widths[pal_id]
        
    return top_length
  
  def get_load_length(self, pall_rows_width, pall_row_length):
      
      # zacni od prvniho a vzdy koukni na predchozi
      # predchozi si bude pamatovat predesly a delku kterou soucasny nabyva
      # a asi by to slo udelat uz v tom predchozim cyklu, aby se predeslo dalsimu opakovani
      # i dkyz by slo o konstantu pro big O()
      # pro kazdy radek si pamatujeme predesly radek, sirku delku
      # pak koukneme pro kazddou novou paletu, a to vyresi i pripad
      # kdyz na konci se propadne az dolu, musim si pamatovat predchozi gap, proste do sirky nakladaku
      # slozitost vzroste o konstantu jen, teda drobne tim ze v kazdem radku prohledame predchozi, jo asi jo
      # plus opadne nutnost si pamatovat tolik dat, coz urychly beh programu tim, ze tahle funkce musi byt fast
      # na konci vezmu posledni info a row a doplnim do soucasneho row, gap info, jak velky je atd 
      pass
    
  
  def get_random_neighbour(self):
    """ Method returns a neighbour state of given state.

    Returns:
        PalletsState: A neighbour state.
    """
    new_state: PalletsState = PalletsState(self)
    
    # with small chance of full permutation
    if (random.random() < 0.1):
      new_state.pallets = random.sample(new_state.pallets, k=len(new_state.pallets))
      new_state.weight = new_state.get_weight()
      return new_state
    
    # chose two palletes to swap 
    f_pallet_i: int = random.randint(0, len(self.pallets) - 1)
    f_pallet: int = new_state.pallets[f_pallet_i]
    s_pallet_i: int = random.randint(0, len(self.pallets) - 1)
    
    while f_pallet_i == s_pallet_i:
      s_pallet_i = random.randint(0, len(self.pallets) - 1)
    
    s_pallet: int = new_state.pallets[s_pallet_i]
    
    #swap
    new_state.pallets[f_pallet_i] = s_pallet
    new_state.pallets[s_pallet_i] = f_pallet
    
    # rotate randomly - in future - depends on how well the unrotated will perform
    rand_i = random.randint(0, len(self.orientation) - 1)
    new_state.set_pallet_orientation(rand_i, (new_state.get_pallet_orientation(rand_i) + 1) % 2)
    
    # Repair state
    new_state.repair_state()
    
    # Set weight
    new_state.weight = new_state.get_weight()
    
    return new_state
  
  def get_n_weights(self, n_weights: int) -> list[int]:
    """ Method returns N weights of random neighbour states.

    Args:
        n_weights (int): Number of weights to return.
        state (PalletsState): Current state for which to find neighbour weights.

    Returns:
        [int]: N neighbour weights.
    """
    weights: list[int] = list()
    
    for _ in range(0, n_weights):
      weights.append(self.get_random_neighbour().get_weight())
      
    return sorted(weights)
  
  def to_arr(self) -> list[list[int]]:
    """Method turns the given state into an array representation

    Returns:
        [[int]]: _description_
    """
    out_arr: list[list[int]] = list()
    curr_length: int = 0
    curr_arr: list[int] = list()
    
    for i in range(0, len(self.pallets)):
      p_id: int = self.pallets[i]
      p_rot: int = self.get_pallet_orientation(p_id)
      
      pal_width: int = self.get_pallet_dim(p_id, p_rot)
      pal_height: int = self.get_pallet_dim(p_id, (p_rot + 1) % 2)
      
      if curr_length + pal_width > self.truck_width:
        curr_length = pal_width
        out_arr.append(curr_arr)
        curr_arr = list()
        curr_arr.append([pal_width, pal_height])
      else:
        curr_arr.append([pal_width, pal_height])
        curr_length += pal_width
    
    if len(curr_arr) != 0:
      out_arr.append(curr_arr)
      
    return out_arr
  
class PalletsStackingSolver:
  """ Class represents the pallets stacking solver
  """
  def __init__(self, pallets_dim: int, truck_width: int) -> None:  
    PalletsState.truck_width = truck_width
    # set dimensions of pallets
    PalletsState.pallets_dimensions = pallets_dim
    PalletsState.pallets_num = len(pallets_dim)
  
    # simulated annealing params
    random.seed(datetime.now().timestamp())
    
    # Algorithm params
    self.init_temp: float = 50.0
    self.final_temp: float = 0.05
    self.iter_num: int = PalletsState.pallets_num * 90 # force
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
  
  @staticmethod
  def get_weights_standard_deviation(weights: list[int]) -> float:
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
    top_pallets: list[int] = list(range(PalletsState.pallets_num))
    top_state: PalletsState = PalletsState(
      top_pallets, 
      0,
      [0] * PalletsState.pallets_num
      )
    
    # Repair state - or return None if cannot be repaired
    try:
      top_state.repair_state()
    except ValueError as value_error:
      raise ValueError(repr(value_error))
    
    top_state.weight = top_state.get_weight()
    
    # If only one pallet, return its best orientation
    if PalletsState.pallets_num == 1:
      if top_state.get_pallet_dim(0, 0) < top_state.get_pallet_dim(0, 1):
        top_state.set_pallet_orientation(0, 1)
        
      top_state.repair_state()
      top_state.weight = top_state.get_weight()
      
      return top_state

    # steps_count = 0
    # res_num = 0
    # Prepare the temperature
    temp: float = self.get_weights_standard_deviation(top_state.get_n_weights(666))
    
    # Initialize the current state
    curr_state: PalletsState = PalletsState(top_state)
    
    # start the annealing
    while temp > self.final_temp:
      
      # repeat the selection for this temperature
      for _ in range(0, self.iter_num):
        new_state: PalletsState = curr_state.get_random_neighbour()
        
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
    
    
  def run(self) -> tuple[[[int]], int]:
    try:
      top_state: PalletsState = self.sim_ann()
      return top_state.to_arr(), top_state.weight
    except ValueError:
      return None, None
    

if __name__ == "__main__":
  pssol = PalletsStackingSolver(main_pallets_dim, 240)
  print(pssol.run())