import numpy as np
import graph
import coloring

def test_simple_case():
    G = np.array([[1, 1, 1, 0, 0],
                  [1, 0, 0, 1, 0],
                  [0, 1, 0, 0, 1],
                  [0, 0, 1, 1, 1]])
    assert {0: 0, 1: 2, 2: 2, 3: 1} == coloring.welsh_powell(G)
