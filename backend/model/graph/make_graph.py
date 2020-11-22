from .node import Node
import networkx as nx
from logging import (
    error as log_error,
    info as log_info,
    basicConfig as log_basicConfig,
    DEBUG
)

log_basicConfig(format='%(levelname)s:%(message)s', level=DEBUG)


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
                    print("When looking at Node %d --> Node %d, we found a distance of %.3f" % (node.id, neighbor_id, distance))
                    current_node_elevation = node.elevation
                    neighbor_node_elevation = G.nodes.get(neighbor_id).get('elevation')
                    elevation_change = neighbor_node_elevation - current_node_elevation
                    if elevation_change < 0: 
                        elevation_change = 0
                    if (distance == 0): 
                        edge_weight = 0
                    else:
                        edge_weight = elevation_change / distance
                    G.add_edge(
                        node.id, 
                        neighbor_id, 
                        weight=edge_weight,
                        distance=distance,
                        elevation_change=elevation_change
                    )

    except Exception as e:
        log_error(e)
        raise
        
    return G