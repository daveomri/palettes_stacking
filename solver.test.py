import unittest
from code.solver import PalettesStackingSolver
import numpy as np

pal1 = [
  [100, 90],
  [150, 110],
  [130, 80],
  [120, 60],
  [110, 120],
  [110, 90]
]

pal2 = [
  [100, 90],
  [150, 110],
  [130, 80],
  [120, 60],
  [110, 120]
]

class TestPalettesStackingSolver(unittest.TestCase):
  
  def test_get_random_neighbour1(self):
    solver = PalettesStackingSolver(pal1)
    state = list(range(len(pal1)))
    
    neigh_state = solver.get_random_neighbour(state)
    
    self.assertIsNotNone(neigh_state)
    self.assertEqual(len(state), len(neigh_state))
    self.assertTrue(np.any(np.not_equal(state, neigh_state)))
    
  def test_get_random_neighbour2(self):
    solver = PalettesStackingSolver(pal2)
    state = list(range(len(pal2)))
    
    neigh_state = solver.get_random_neighbour(state)
    
    self.assertIsNotNone(neigh_state)
    self.assertEqual(len(state), len(neigh_state))
    self.assertTrue(np.any(np.not_equal(state, neigh_state)))
  
  def test_get_weight1(self):
    solver = PalettesStackingSolver(pal1)
    state = list(range(len(pal1)))
    
    self.assertEqual(460, solver.get_weight(state))
    
  def test_get_weight2(self):
    solver = PalettesStackingSolver(pal2)
    state = list(range(len(pal2)))
    
    self.assertEqual(460, solver.get_weight(state))
    
  def test_get_n_weights1(self):
    solver = PalettesStackingSolver(pal1)
    state = list(range(len(pal1)))
    
    weights = solver.get_n_weights(20, state)
    
    self.assertEqual(20, len(weights), 'It is wrong')
    
  def test_get_n_weights2(self):
    solver = PalettesStackingSolver(pal2)
    state = list(range(len(pal2)))
    
    weights = solver.get_n_weights(20, state)
    
    self.assertEqual(20, len(weights), 'It is wrong')
    
  def test_get_weights_standard_deviation(self):
    solver = PalettesStackingSolver(pal2)
    state = list(range(len(pal2)))
    
    weights = solver.get_n_weights(200, state)
    w_std_dev = solver.get_weights_standard_deviation(weights)

    self.assertIsNotNone(w_std_dev)
    
    
if __name__ == '__main__':
  unittest.main()