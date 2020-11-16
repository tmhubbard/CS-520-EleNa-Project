
# This script was written by Ritwik Bagga; its purpose is to check validity of points ( using OSMnx nodes) and add elevations

# =========================
#        * SETUP *
# =========================
import requests
import osmnx as ox
import json
import urllib
#from calcBoundary import boundaryBoxPoints as bb_points
import requests
# import osmnx as ox
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
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
def make_nodes(sample_points: list ):
    # hard coding the cx , cy for osmnx graph
    cx , cy =42.389555, -72.528127 # location of DU BOYS Library
    osmnx_graph = get_osmnx_graph(cx,cy)
    ox.plot.plot_graph(osmnx_graph)
    Nodes = []

    for point in sample_points:  #point is (lat, lng)

        node_dst = ox.distance.get_nearest_node(osmnx_graph, point, method='haversine', return_dist= True)[1]

        #check for valid range ( 10m>node_dst > 100m)
        if node_dst<10 or node_dst>100 :#need to tune this
            point = (point[0], point[1], get_elevation(point)) #add the elevation
            Nodes.append(point)
    return Nodes

#testing for one invalid and one valid point
# sample_points = [(42.386690, -72.525936) , (42.385544, -72.525861)]
# print(make_nodes(sample_points))
















