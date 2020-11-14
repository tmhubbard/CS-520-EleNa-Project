import requests
#import osmnx as ox
import json
import urllib
import requests
# import osmnx as ox
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import os

class controller(object):

    def _init_(self):
        self.model = None
        self.view = None

    def set_model(self, model):
        self.model = model

    def set_view(self, view):
        self.view =view



    def A_Star(self, graph , start, goal, edge_list, mode= "minimize"):
#default value is minimize if nothing selected
#check for mode as min or max
#returns list of nodes
        pass

    def dijkstra(self, graph , start, goal, edge_list, mode= "minimize"):
        pass
#default value is minimize if nothing selected
#check for mode as min or max
#returns list of nodes







def get_map(address):
    apikey = "AIzaSyBmg_5waDYCtmUW3YCNJ75dUWc6_5_i8wE"
    url = "https://maps.googleapis.com/maps/api/staticmap?center=+"+str(address)+"&zoom=14&size=640x640&style=feature:landscape.man_made|element:labels|color:0xffffff&key="
    response = requests.get(url + apikey)
    imagex = response.content
    image_data = imagex  # byte values of the image
    open('Test_Buildings_map.png', 'wb').write(image_data)
    plt.imshow(mpimg.imread('Test_Buildings_map.png'))
    plt.show()
    os.remove('Test_Buildings_map.png')
get_map("UMass Amherst")

breakpoint()

def elevation(location):
    lat = location[0]
    lng = location[1]
    apikey = "AIzaSyBmg_5waDYCtmUW3YCNJ75dUWc6_5_i8wE"
    url = "https://maps.googleapis.com/maps/api/elevation/json"
    request = requests.get(url + "?locations=" + str(lat) + "," + str(lng) + "&key=" + apikey).json()
    return request['results'][0]['elevation']

    """
    this function will check the validity of a location ((lat, lng)) 
    return type: boolean 

    """


def valid_location(location):
    lat = location[0]
    lng = location[1]
    apikey = "AIzaSyBmg_5waDYCtmUW3YCNJ75dUWc6_5_i8wE"
    url = "https://roads.googleapis.com/v1/nearestRoads?" + str(lat) + "," + str(lng) + "&key=" + apikey
    print(url)
    # request = requests.get(url  + str(lat) + "," + str(lng) + "&key=" + apikey)
    # print(request)
    breakpoint()

    """
    this function would return different sampled nodes with their elevations which are valid
    :input type : List[(lat,long)]  
    :rtype: List[(lat,long,elevation)]  

    """


# locations = [(35.929673, -78.948237), (38.889510, -77.032000), (38.032120, -78.477510)]
# locations2 = (35.929673, -78.948237)
# print(valid_location(locations2))
#
#
# def elevations(locations):
#     Nodes = []
#     for location in locations:
#         # check valid here
#         node = (location[0], location[1], elevation(location))
#         Nodes.append(node)
#     return Nodes
#
#
# print(elevations(locations=locations))

# #place_query = {'city':'Amherst', 'state':'Massachusetts', 'country':'USA'}
# address = "139 Starling way, Hercules CA"
# graph_orig = ox.graph_from_address(address, dist = 1000, network_type='drive') #drive and bike
# graph_orig = ox.add_node_elevations(graph_orig, api_key= "AIzaSyBmg_5waDYCtmUW3YCNJ75dUWc6_5_i8wE")
# graph_orig = ox.add_edge_grades(graph_orig)
# route_nodes= []
# for i in range(10):
#     node_id = list(graph_orig.nodes())[]
#     print(node_id)
#     route_nodes.append(node_id)
# breakpoint()
# origin_lat , origin_long =38.003560 , -122.268830
# node1 =57785756
# node2 = 57791348
# #bbox = ox.bbox_from_point((float(origin_lat), float(origin_long)), distance=1500, project_utm=True)
# ox.plot_graph_route(graph_orig, route= route_nodes,  route_color = 'r',  route_linewidth=4, route_alpha=0.5, orig_dest_size=100, ax=None)
# # #ox.plot_graph(graph_orig)









