
# This script was written by Ritwik Bagga; its purpose is to check validity of points ( using OSMnx nodes) and add elevations

# =========================
#        * SETUP *
# =========================
import requests
import osmnx as ox
from model.graph.node import Node
from model.graph.make_graph import make_graph
from calcBoundary import boundaryBoxPoints
import requests
import os



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
    url = "https://maps.googleapis.com/maps/api/elevation/json"
    request = requests.get(url + "?locations=" + str(lat) + "," + str(lng) + "&key=" + apikey).json()
    return request['results'][0]['elevation']

#from the list of sample_points validates and adds elevation for each location
#return type is valid points list( (lat, lng , elevation) )

def get_validNodes(sample_points , center, radius):
    # hard coding the cx , cy for osmnx graph
    cx , cy =center[0], center[1] # location of DU BOYS Library
    osmnx_graph = get_osmnx_graph(cx,cy, radius)
    #ox.plot.plot_graph(osmnx_graph)
    Nodes = []
    nodes_ids = []

    for index, point in enumerate(sample_points):  #point is (lat, lng)
        location = (point.latitude, point.longitude)
        node_dst = ox.distance.get_nearest_node(osmnx_graph, location, method='haversine', return_dist= True)[1]
        # nearest_point_ID = ox.distance.get_nearest_node(osmnx_graph, location, method='haversine', return_dist= True)[0]

        #check for valid range ( 10m>node_dst > 100m)
        if node_dst<5 or node_dst>50 :#need to tune this
            point.elevation = get_elevation(location) #add elevation
            Nodes.append(point)
            nodes_ids.append(point.id)
    
    for node in Nodes:
        valid_neighbors = []
        for neighbor in node.neighbors:
            neighbor_id = neighbor[0]
            neighbor_dist = neighbor[1]
            if neighbor_id in nodes_ids:
                valid_neighbors.append((neighbor_id, neighbor_dist))      
        node.neighbors = valid_neighbors          
    return Nodes

#testing
# sp =  [[42.386690, -72.525936] ,  [42.385544, -72.525861]]
# valid_nodes = get_validNodes(sp)
# graph = make_graph(valid_nodes)
# print(type(graph))

origin = (42.372391, -72.516950)
destination = (42.372268, -72.511058)

nodes, c = boundaryBoxPoints(origin, destination, 1.5, 30) # c =( (x,y) , radius )
center = c[0]
radius = c[1]


def get_Graph(Nodes):
    return make_graph(Nodes)

valid_nodes = get_validNodes(nodes , center, radius)
# for point in valid_nodes:
#     print(str(point.latitude) + "," +  str(point.longitude))











