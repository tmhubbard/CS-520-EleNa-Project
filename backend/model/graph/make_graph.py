from .node import Node
import networkx as nx
import numpy as np
import requests
from logging import (
    error as log_error,
    info as log_info,
    basicConfig as log_basicConfig,
    DEBUG
)
from model.graph.calcBoundary import boundaryBoxPoints, midpoint

log_basicConfig(format='%(levelname)s:%(message)s', level=DEBUG)
nodeOffsets = {}
SOURCE = 0
TARGET = -1

def get_graph(origin, destination, overhead):
    global nodeOffsets
    nodes, c, nodeOffsets = boundaryBoxPoints(origin, destination, overhead, 150) # c =( (x,y) , radius ) #1.5
    center = c[0]
    radius = c[1]
    valid_nodes, _ = get_validNodes(nodes, center, radius, nodeOffsets)
    G = make_graph(valid_nodes)
    return G

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
                    elevation_change = neighbor_node_elevation - current_node_elevation
                    if elevation_change < 0: 
                        elevation_change = 0
                    if (distance == 0): 
                        edge_weight = 0
                    else:
                        edge_weight = elevation_change
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

#returns the elevation of a lat,lng location
def get_elevation(location:(float, float))-> float:
    lat = location[0]
    lng = location[1]
    apikey = "AIzaSyBmg_5waDYCtmUW3YCNJ75dUWc6_5_i8wE"
    apikey = "AIzaSyC0_EhM25ltUK20oJPH4k4Ni6jqiU4bS2Q" # Trevor's API key
    url = "https://maps.googleapis.com/maps/api/elevation/json"
    request = requests.get(url + "?locations=" + str(lat) + "," + str(lng) + "&key=" + apikey).json()
    return request['results'][0]['elevation']


#from the list of sample_points validates and adds elevation for each location
#return type is valid points list( (lat, lng , elevation) )
def get_validNodes(sample_points , center, radius, nodeOffsets):
    Nodes = []
    NodeIDToNodesIdx = {}
    nodes_ids = []
    reconnectThreshold = 3

    for _data, point in enumerate(sample_points):  #point is (lat, lng)
        location = (point.latitude, point.longitude)
        point.elevation = get_elevation(location) #add elevation
        Nodes.append(point)
        NodeIDToNodesIdx[point.id] = len(Nodes)-1
        nodes_ids.append(point.id)
    
    newBackEdges = [] # This will be helpful for reconnecting "islanded" nodes 

    for node in Nodes:
        valid_neighbors = []
        for neighbor in node.neighbors:
            neighbor_id = neighbor[0]
            neighbor_dist = neighbor[1]
            if neighbor_id in nodes_ids:
                valid_neighbors.append((neighbor_id, neighbor_dist))

        # Prevent this node from being "islanded" by reconnecting it w/ closer nodes
        if (len(valid_neighbors) < reconnectThreshold):
            
            # Calculate the distance between this node and all other valid nodes
            neighborDists = {}
            for otherPointID in nodes_ids:
                curNodeOffset = nodeOffsets[node.id]
                neighborOffset = nodeOffsets[otherPointID]
                dist = np.linalg.norm(curNodeOffset - neighborOffset)
                neighborDists[otherPointID] = dist

            # Sort the distances, and reconnect the closest couple
            sortedNeighborDists = {k: v for k, v in sorted(neighborDists.items(), key=lambda item: item[1])}
            toReconnect = [(nodeID, distance) for nodeID, distance in list(sortedNeighborDists.items())[:reconnectThreshold]]
            currentConnected = [nodeID for nodeID, neighDist in valid_neighbors]
            for neighborPair in toReconnect:
                neighborID, neighborDist = neighborPair
                if (neighborID not in currentConnected):
                    valid_neighbors.append((neighborID, neighborDist))
                    newBackEdges.append((neighborID, node.id, neighborDist))

        node.neighbors = valid_neighbors      

    # Make the new back edges for the nodes that you reconnected 
    for backEdge in newBackEdges:
        sourceNodeID = backEdge[0]
        targetNodeID = backEdge[1]
        backEdgeDist = backEdge[2]
        Nodes[NodeIDToNodesIdx[sourceNodeID]].neighbors.append((targetNodeID, backEdgeDist))    

    return Nodes, NodeIDToNodesIdx

def nodeDistance(source, target):
    global nodeOffsets

    sourceNodeOffset = nodeOffsets[source]
    targetNodeOffset = nodeOffsets[target]
    distance = np.linalg.norm(np.array(sourceNodeOffset)-np.array(targetNodeOffset))
    return distance

def nodes_to_lat_lng_coordinates(G, path):
    route = []
    for node in path:
        route.append(
            {
                "lat": G.nodes.get(node)['latitude'], 
                "lng": G.nodes.get(node)['longitude']
            }
        )
    return route


