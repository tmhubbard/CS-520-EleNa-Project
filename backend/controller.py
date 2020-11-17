
# This script was written by Ritwik Bagga; its purpose is to check validity of points ( using OSMnx nodes) and add elevations

# =========================
#        * SETUP *
# =========================
import requests
import osmnx as ox
from model.graph.node import Node
from model.graph.make_graph import make_graph
import requests
import os



#generate osmnx graph for node validation with center as (cx, cy)
def get_osmnx_graph(cx , cy):
    center = (cx, cy)
    graph_orig = ox.graph_from_point(center, dist = 1000, network_type='drive')
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

def get_validNodes(sample_points ):
    # hard coding the cx , cy for osmnx graph
    cx , cy =42.389555, -72.528127 # location of DU BOYS Library
    osmnx_graph = get_osmnx_graph(cx,cy)
    ox.plot.plot_graph(osmnx_graph)
    Nodes = []

    for index, point in enumerate(sample_points):  #point is (lat, lng)

        node_dst = ox.distance.get_nearest_node(osmnx_graph, point, method='haversine', return_dist= True)[1]
        #check for valid range ( 10m>node_dst > 100m)
        if node_dst<10 or node_dst>100 :#need to tune this

            node = Node(id= index,latitude= point[0], longitude = point[1], elevation = get_elevation(point) , neighbors = None )
            print(node.get_content())
            Nodes.append(node)

    return Nodes

#testing
# sp =  [[42.386690, -72.525936] ,  [42.385544, -72.525861]]
# valid_nodes = get_validNodes(sp)
# graph = make_graph(valid_nodes)
# print(type(graph))




def get_Graph(Nodes):
    return make_graph(Nodes)









