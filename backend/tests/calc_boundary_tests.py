import unittest

from model.graph.node import Node
from model.graph.make_graph import make_graph

class CalcBoundaryTests(unittest.TestCase):
    
    def test_rotate_point(self):
        """Test astar search on a directed graph to get the minimum path.
        """
        