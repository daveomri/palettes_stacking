import unittest
from code.solver import PalletsStackingSolver, PalletsState
import numpy as np

pal1: list[list[int]] = [
  [100, 90],
  [150, 110],
  [130, 80],
  [120, 60],
  [110, 120],
  [110, 90]
]

pal2: list[list[int]] = [
  [100, 90],
  [150, 110],
  [130, 80],
  [120, 60],
  [110, 120]
]

truck_width: int = 240

class TestPalletsStackingSolver(unittest.TestCase):
  
  def test_get_random_neighbour1(self):
    state: PalletsState = PalletsState(
      list(range(len(pal1))),
      0,
      [0] * len(pal1)
    )
    PalletsState.truck_width = truck_width
    # set dimensions of pallets
    PalletsState.pallets_dimensions = pal1
    PalletsState.pallets_num = len(pal1)
    
    state.weight = state.get_weight()
    neigh_state = state.get_random_neighbour()
    
    self.assertIsNotNone(neigh_state)
    self.assertEqual(len(state.pallets), len(neigh_state.pallets))
    self.assertTrue(np.any(np.not_equal(state.pallets, neigh_state.pallets)))
    
  def test_get_random_neighbour2(self):
    state: PalletsState = PalletsState(
      list(range(len(pal2))),
      0,
      [0] * len(pal2)
    )
    
    PalletsState.truck_width = truck_width
    # set dimensions of pallets
    PalletsState.pallets_dimensions = pal2
    PalletsState.pallets_num = len(pal2)
    
    state.weight = state.get_weight()
    neigh_state = state.get_random_neighbour()
    
    self.assertIsNotNone(neigh_state)
    self.assertEqual(len(state.pallets), len(neigh_state.pallets))
    self.assertTrue(np.any(np.not_equal(state.pallets, neigh_state.pallets)))
  
  def test_get_weight1(self):
    state: PalletsState = PalletsState(
      list(range(len(pal1))),
      0,
      [0] * len(pal1)
    )
    PalletsState.truck_width = truck_width
    # set dimensions of pallets
    PalletsState.pallets_dimensions = pal1
    PalletsState.pallets_num = len(pal1)
    
    state.weight = state.get_weight()
    
    self.assertEqual(430, state.weight)
    
  def test_get_weight2(self):
    state: PalletsState = PalletsState(
      list(range(len(pal2))),
      0,
      [0] * len(pal2)
    )
    PalletsState.truck_width = truck_width
    # set dimensions of pallets
    PalletsState.pallets_dimensions = pal2
    PalletsState.pallets_num = len(pal2)
    
    state.weight = state.get_weight()
    
    self.assertEqual(400, state.weight)
    
  def test_get_n_weights1(self):
    state: PalletsState = PalletsState(
      list(range(len(pal1))),
      0,
      [0] * len(pal1)
    )
    PalletsState.truck_width = truck_width
    # set dimensions of pallets
    PalletsState.pallets_dimensions = pal1
    PalletsState.pallets_num = len(pal1)
    
    state.weight = state.get_weight()
    
    weights = state.get_n_weights(20)
    
    self.assertEqual(20, len(weights), 'It is wrong')
    
  def test_get_n_weights2(self):
    state: PalletsState = PalletsState(
      list(range(len(pal2))),
      0,
      [0] * len(pal2)
    )
    PalletsState.truck_width = truck_width
    # set dimensions of pallets
    PalletsState.pallets_dimensions = pal2
    PalletsState.pallets_num = len(pal2)
    
    state.weight = state.get_weight()
    
    weights = state.get_n_weights(20)
    
    self.assertEqual(20, len(weights), 'It is wrong')
    
  def test_get_weights_standard_deviation(self):
    state: PalletsState = PalletsState(
      list(range(len(pal2))),
      0,
      [0] * len(pal2)
    )
    PalletsState.truck_width = truck_width
    # set dimensions of pallets
    PalletsState.pallets_dimensions = pal2
    PalletsState.pallets_num = len(pal2)
    
    state.weight = state.get_weight()
    
    weights = state.get_n_weights(200)
    w_std_dev = PalletsStackingSolver.get_weights_standard_deviation(weights)

    self.assertIsNotNone(w_std_dev)
    
    
if __name__ == '__main__':
  unittest.main()