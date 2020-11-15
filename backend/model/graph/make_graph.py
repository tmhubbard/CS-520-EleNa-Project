from .node import Node
import networkx as nx
from logging import (
    error as log_error,
    info as log_info,
    basicConfig as log_basicConfig,
    DEBUG
)

log_basicConfig(format='%(levelname)s:%(message)s', level=DEBUG)

def get_edge_weight(elevation_a: float, elevation_b: float, distance: float) -> float:
    """Calculate the edge weight between node a and b by subtracting
       their elevations.
       Note: If delta elevation is negative, weight is 0
    """
    edge_weight = (elevation_b - elevation_a) / distance
    return edge_weight if edge_weight >= 0 else 0

def make_graph(nodes: list):
    """Use the list of nodes to create a NetworkX Directed Graph.
    """
    try:
        G = nx.MultiDiGraph()
        # Add nodes to the graph
        for node in nodes:
            G.add_node(node.id, **node.as_json())
        
        # Add edges to the graph
        for node in nodes:
            if node.neighbors:
                for neighbor_id, distance in node.neighbors:
                    current_node_elevation = node.elevation
                    neighbor_node_elevation = G.nodes.get(neighbor_id).get('elevation')
                    edge_weight = get_edge_weight(current_node_elevation, neighbor_node_elevation, distance)
                    G.add_edge(node.id, neighbor_id, weight=edge_weight)
    except Exception as e:
        log_error(e)
        raise

    return G