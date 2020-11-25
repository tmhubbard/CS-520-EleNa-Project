import networkx as nx
from model.graph.make_graph import nodeDistance

def get_minimum_path_and_elevation(G, source, target, overhead):
    path = nx.astar_path(G, source=0, target=-1)
    elevation_gain = calcElevationGain(G, path)
    return path, elevation_gain

def get_maximum_path_and_elevation(G, source: int, target: int, overhead):
    maxDistance = overhead * nodeDistance(0, -1)
    sourceTargetDistance = nodeDistance(source, target)
    cutoffAmt = int(sourceTargetDistance/150)
    paths = nx.all_simple_paths(G, source=source, target=target, cutoff=cutoffAmt)
    maximum_elevation_gain = float('-inf')
    with open("results.txt", "a") as resultFile:
        for path in paths:
            elevation_gain_of_path = calcElevationGain(G, path)
            pathDistance = calcRouteDistance(G, path)
            if (pathDistance > maxDistance): 
                continue
            resultFile.write("%s\n" % elevation_gain_of_path)
            if elevation_gain_of_path > maximum_elevation_gain:
                maximum_elevation_gain = elevation_gain_of_path
                maximum_elevation_gain_path = path

    return maximum_elevation_gain_path, maximum_elevation_gain

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
