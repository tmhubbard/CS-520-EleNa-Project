
# This script was written by Ritwik Bagga; its purpose is to check validity of points ( using OSMnx nodes) and add elevations

# =========================
#        * SETUP *
# =========================
import requests
import osmnx as ox
import numpy as np
import matplotlib.pyplot as plt
from model.graph.node import Node
from model.graph.make_graph import make_graph
from model.graph.calcBoundary import boundaryBoxPoints, midpoint
import requests
import os
import networkx as nx
from enums import ElevationType


#generate osmnx graph for node validation with center as (cx, cy)
def get_osmnx_graph(cx , cy, radius):
    center = (cx, cy)
    graph_orig = ox.graph_from_point(center, dist = radius, network_type='walk')
    return graph_orig

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
    # hard coding the cx , cy for osmnx graph
    cx , cy =center[0], center[1] # location of DU BOYS Library
    osmnx_graph = get_osmnx_graph(cx,cy, radius)
    #ox.plot.plot_graph(osmnx_graph)
    Nodes = []
    NodeIDToNodesIdx = {}
    nodes_ids = []
    reconnectThreshold = 3

    for index, point in enumerate(sample_points):  #point is (lat, lng)
        location = (point.latitude, point.longitude)
        node_dst = ox.distance.get_nearest_node(osmnx_graph, location, method='haversine', return_dist= True)[1]
        # nearest_point_ID = ox.distance.get_nearest_node(osmnx_graph, location, method='haversine', return_dist= True)[0]

        #check for valid range ( 10m>node_dst > 100m)
        if (node_dst<3 or node_dst>10) or (index==0 or index == 1): #need to tune this
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

#testing
# sp =  [[42.386690, -72.525936] ,  [42.385544, -72.525861]]
# valid_nodes = get_validNodes(sp)
# graph = make_graph(valid_nodes)
# print(type(graph))

# origin = (42.372391, -72.516950)
# destination = (42.372268, -72.511058)

# nodes, c = boundaryBoxPoints(origin, destination, 1.5, 30) # c =( (x,y) , radius )
# center = c[0]
# radius = c[1]


# valid_nodes = get_validNodes(nodes , center, radius)
# breakpoint()
# G = make_graph(valid_nodes)


def get_maximum_path_and_elevation(G, source: int, target: int):
    paths = nx.all_simple_paths(G, source=source, target=target)
    maximum_elevation_gain = float('-inf')
    for path in paths:
        elevation_gain_of_path = calcElevationGain(G, path)
        if elevation_gain_of_path > maximum_elevation_gain:
            maximum_elevation_gain = elevation_gain_of_path
            maximum_elevation_gain_path = path

    return maximum_elevation_gain_path, maximum_elevation_gain

def get_route_data(origin, destination, elevation_type, overhead):
    nodes, c, nodeOffsets = boundaryBoxPoints(origin, destination, overhead, 150) # c =( (x,y) , radius ) #1.5
    center = c[0]
    radius = c[1]
    valid_nodes, nodeIDsToValidNodesIdx = get_validNodes(nodes, center, radius, nodeOffsets)
    G = make_graph(valid_nodes)
    # breakpoint()

    if elevation_type == ElevationType.MINIMUM:
        path = nx.astar_path(G, source=0, target=-1)
        elevation_gain = calcElevationGain(G, path)
    else:
        path, elevation_gain = get_maximum_path_and_elevation(
            G,
            source=0, 
            target=-1
        )
    route_distance = calcRouteDistance(G, path)

    route = []
    for node in path:
        route.append(
            {
                "lat": G.nodes.get(node)['latitude'], 
                "lng": G.nodes.get(node)['longitude']
            }
        )
    # visualizePath(valid_nodes, nodeIDsToValidNodesIdx, path)

    return route, elevation_gain, route_distance

def calcElevationGain(graph, path):
    """This method will calculate the elevation gain for a given route
    """

    # Step through each node in the path and add its elevation gain to elevationGain
    elevationGain = 0
    for nodeNum, thisNode in enumerate(path):

        # Skip the last node
        if (nodeNum == len(path)-1): continue

        # Add the elevation change between thisNode and nextNode
        nextNode = path[nodeNum+1]
        edgeData = graph.get_edge_data(thisNode, nextNode)[0]
        if (not edgeData is None and "elevation_change" in edgeData):
            elevationGain += edgeData["elevation_change"]

    # Return the total elevation gain for the path
    return elevationGain

def calcRouteDistance(graph, path):
    """This method will calculate the distance for a given route
    """
    
    # Step through each node in the path and add its elevation gain to elevationGain
    distance = 0
    for nodeNum, thisNode in enumerate(path):

        # Skip the last node
        if (nodeNum == len(path)-1): continue

        # Add the elevation change between thisNode and nextNode
        nextNode = path[nodeNum+1]
        edgeData = graph.get_edge_data(thisNode, nextNode)[0]
        if (not edgeData is None and "distance" in edgeData):
            distance += edgeData["distance"]

    # Return the total elevation gain for the path
    return distance

# This method will help me visualize the path that the nodes give
def visualizePath(nodes, NodeIDToNodesIdx, path):
    for node in nodes:
        plt.plot(node.longitude, node.latitude, "go", markersize=10)
        plt.text(node.longitude, node.latitude, ("%s (%.2f)" % (str(node.id), node.elevation)))

    # Plot the lines between neighbors
    linesDrawn = {}
    for node in nodes: 
        # Step through each of the neighbors in node's neighborList
        for neighborNode in node.neighbors:

            neighborNodeID, neighborNodeDist = neighborNode

            # Draw the line between this node and neighborNode if it hasn't already been drawn
            if ((neighborNodeID, node.id) in linesDrawn): continue
            longitudes = (node.longitude, nodes[NodeIDToNodesIdx[neighborNodeID]].longitude)
            latitudes = (node.latitude, nodes[NodeIDToNodesIdx[neighborNodeID]].latitude)
            plt.plot(longitudes, latitudes, "g-")
            lineMidpoint = midpoint([node.longitude, node.latitude], [nodes[NodeIDToNodesIdx[neighborNodeID]].longitude, nodes[NodeIDToNodesIdx[neighborNodeID]].latitude])
            plt.text(lineMidpoint[0], lineMidpoint[1], ("%.2f" % float(neighborNodeDist)))

    # Draw a line for the path 
    for pathNodeNum, pathNodeID in enumerate(path):

        # Skip this node if it's the last one 
        if (pathNodeNum == len(path)-1): continue

        # Highlight the path in red
        thisNode = nodes[NodeIDToNodesIdx[pathNodeID]]
        nextNode = nodes[NodeIDToNodesIdx[path[pathNodeNum+1]]]
        longitudes = (thisNode.longitude, nextNode.longitude)
        latitudes = (thisNode.latitude, nextNode.latitude)
        plt.plot(longitudes, latitudes, "r-", linewidth=5)

    # Show the pyplot
    plt.show()


