import unittest
import networkx as nx

from model.graph.node import Node
from model.graph.make_graph import make_graph

class MakeGraphTest(unittest.TestCase):
    
    def test_astar_search(self):
        """Test astar search on a directed graph to get the minimum path.
        """
        # neighbors = (neighborID, distance)
        list_of_node_objects = [
            Node(id=1, elevation=10, neighbors=[(2, 2)]),
            Node(id=2, elevation=11, neighbors=[(3, 2), (4, 4)]),
            Node(id=3, elevation=12, neighbors=[(4, 4)]),
            Node(id=4, elevation=14)
        ]

        G = make_graph(list_of_node_objects)
        expected_shortest_path = [1, 2, 4]
        expected_shortest_path_length = 1.25
        # 'astar_path' function gets the list of nodes in the 
        # shortest path between source and target using the A* (“A-star”) algorithm.
        shortest_path = nx.astar_path(G, source=1, target=4)
        shortest_path_length = nx.astar_path_length(G, source=1, target=4)
        assert shortest_path == expected_shortest_path, \
            f'Expected path = {expected_shortest_path}, got {shortest_path}'
        assert shortest_path_length == expected_shortest_path_length, \
            f'Expected length = {expected_shortest_path}, got {shortest_path}'