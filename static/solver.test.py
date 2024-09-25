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
    solver: PalletsStackingSolver = PalletsStackingSolver(pal1, truck_width)
    state: PalletsState = PalletsState(
      list(range(len(pal1))),
      0,
      [0] * len(pal1)
    )
    state.weight = solver.get_weight(state)
    
    neigh_state = solver.get_random_neighbour(state)
    
    self.assertIsNotNone(neigh_state)
    self.assertEqual(len(state.pallets), len(neigh_state.pallets))
    self.assertTrue(np.any(np.not_equal(state.pallets, neigh_state.pallets)))
    
  def test_get_random_neighbour2(self):
    solver: PalletsStackingSolver = PalletsStackingSolver(pal2, truck_width)
    state: PalletsState = PalletsState(
      list(range(len(pal2))),
      0,
      [0] * len(pal2)
    )
    state.weight = solver.get_weight(state)
    
    neigh_state = solver.get_random_neighbour(state)
    
    self.assertIsNotNone(neigh_state)
    self.assertEqual(len(state.pallets), len(neigh_state.pallets))
    self.assertTrue(np.any(np.not_equal(state.pallets, neigh_state.pallets)))
  
  def test_get_weight1(self):
    solver: PalletsStackingSolver = PalletsStackingSolver(pal1, truck_width)
    state: PalletsState = PalletsState(
      list(range(len(pal1))),
      0,
      [0] * len(pal1)
    )
    state.weight = solver.get_weight(state)
    
    self.assertEqual(490, state.weight)
    
  def test_get_weight2(self):
    solver: PalletsStackingSolver = PalletsStackingSolver(pal2, truck_width)
    state: PalletsState = PalletsState(
      list(range(len(pal2))),
      0,
      [0] * len(pal2)
    )
    state.weight = solver.get_weight(state)
    
    self.assertEqual(400, state.weight)
    
  def test_get_n_weights1(self):
    solver: PalletsStackingSolver = PalletsStackingSolver(pal1, truck_width)
    state: PalletsState = PalletsState(
      list(range(len(pal1))),
      0,
      [0] * len(pal1)
    )
    state.weight = solver.get_weight(state)
    
    weights = solver.get_n_weights(20, state)
    
    self.assertEqual(20, len(weights), 'It is wrong')
    
  def test_get_n_weights2(self):
    solver: PalletsStackingSolver = PalletsStackingSolver(pal2, truck_width)
    state: PalletsState = PalletsState(
      list(range(len(pal2))),
      0,
      [0] * len(pal2)
    )
    state.weight = solver.get_weight(state)
    
    weights = solver.get_n_weights(20, state)
    
    self.assertEqual(20, len(weights), 'It is wrong')
    
  def test_get_weights_standard_deviation(self):
    solver: PalletsStackingSolver = PalletsStackingSolver(pal2, truck_width)
    state: PalletsState = PalletsState(
      list(range(len(pal2))),
      0,
      [0] * len(pal2)
    )
    state.weight = solver.get_weight(state)
    
    weights = solver.get_n_weights(200, state)
    w_std_dev = solver.get_weights_standard_deviation(weights)

    self.assertIsNotNone(w_std_dev)
    
    
if __name__ == '__main__':
  unittest.main()