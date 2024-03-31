import unittest
from code.solver import PalettesStackingSolver, PalettesState
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
    state = PalettesState(
      list(range(len(pal1))),
      0,
      [0] * len(pal1)
    )
    state.weight = solver.get_weight(state)
    
    neigh_state = solver.get_random_neighbour(state)
    
    self.assertIsNotNone(neigh_state)
    self.assertEqual(len(state.palettes), len(neigh_state.palettes))
    self.assertTrue(np.any(np.not_equal(state.palettes, neigh_state.palettes)))
    
  def test_get_random_neighbour2(self):
    solver = PalettesStackingSolver(pal2)
    state = PalettesState(
      list(range(len(pal2))),
      0,
      [0] * len(pal2)
    )
    state.weight = solver.get_weight(state)
    
    neigh_state = solver.get_random_neighbour(state)
    
    self.assertIsNotNone(neigh_state)
    self.assertEqual(len(state.palettes), len(neigh_state.palettes))
    self.assertTrue(np.any(np.not_equal(state.palettes, neigh_state.palettes)))
  
  def test_get_weight1(self):
    solver = PalettesStackingSolver(pal1)
    state = PalettesState(
      list(range(len(pal1))),
      0,
      [0] * len(pal1)
    )
    state.weight = solver.get_weight(state)
    
    self.assertEqual(460, state.weight)
    
  def test_get_weight2(self):
    solver = PalettesStackingSolver(pal2)
    state = PalettesState(
      list(range(len(pal2))),
      0,
      [0] * len(pal2)
    )
    state.weight = solver.get_weight(state)
    
    self.assertEqual(460, state.weight)
    
  def test_get_n_weights1(self):
    solver = PalettesStackingSolver(pal1)
    state = PalettesState(
      list(range(len(pal1))),
      0,
      [0] * len(pal1)
    )
    state.weight = solver.get_weight(state)
    
    weights = solver.get_n_weights(20, state)
    
    self.assertEqual(20, len(weights), 'It is wrong')
    
  def test_get_n_weights2(self):
    solver = PalettesStackingSolver(pal2)
    state = PalettesState(
      list(range(len(pal2))),
      0,
      [0] * len(pal2)
    )
    state.weight = solver.get_weight(state)
    
    weights = solver.get_n_weights(20, state)
    
    self.assertEqual(20, len(weights), 'It is wrong')
    
  def test_get_weights_standard_deviation(self):
    solver = PalettesStackingSolver(pal2)
    state = PalettesState(
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