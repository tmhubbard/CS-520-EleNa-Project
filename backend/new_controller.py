import osmnx as ox
import pickle as pkl
from enums import MINIMUM
from model.graph.make_graph import (
    get_graph,
    SOURCE, TARGET,
    nodes_to_lat_lng_coordinates
)
from algorithm import (
    get_minimum_path_and_elevation,
    get_maximum_path_and_elevation,
    calcRouteDistance
)

"""
input: origin(lt, lng), destination(lt, lng), 
"""

def get_map():
    place = 'Amherst'
    place_query = {'city': 'Amherst', 'state': 'Massachusetts', 'country': 'USA'}
    graph_orig = ox.graph_from_place(place_query, network_type='drive')

    # adding elevation data from GoogleMaps
    # Enter the API key here
    key = "AIzaSyBmg_5waDYCtmUW3YCNJ75dUWc6_5_i8wE"
    graph_orig = ox.add_node_elevations(graph_orig, api_key=key)
    graph_orig = ox.add_edge_grades(graph_orig)
    pkl.dump(graph_orig, open("graph.pkl", "wb"))

    # projecting map on to 2D space
    graph_projection = ox.project_graph(graph_orig)
    pkl.dump(graph_projection, open("graph_projected.pkl", "wb"))
    return  graph_projection, graph_orig


def get_path(came_from, origin, destination):
        route_by_length_minele = []
        p = destination
        route_by_length_minele.append(p)
        while p != origin:
           p = came_from[p]
           route_by_length_minele.append(p)
        route_by_length_minele = route_by_length_minele[::-1]
        return route_by_length_minele



def get_cost(graph_projection, a, b):
    return graph_projection.edges[a, b, 0]['length']



def get_elevation_cost(self, graph_projection, a, b):
    return (graph_projection.nodes[a]['elevation'] - graph_projection.nodes[b]['elevation'])



def get_total_elevation(self, graph_projection, route):
    if not route:
        return 0
    elevation_cost = 0
    for i in range(len(route)-1):
         elevation_data = self.get_elevation_cost(graph_projection, route[i], route[i+1])
         if elevation_data > 0:
             elevation_cost += elevation_data
    return elevation_cost


def get_total_length(self, graph_projection, route):
    if not route:
        return 0
    cost = 0
    for i in range(len(route)-1):
         cost += self.get_cost(graph_projection, route[i], route[i+1])
    return cost


def get_route_data(origin, destination, elevation_type, overhead):
    # GENERATE GRAPH
    graph_projection, graph_orig = get_map()
    origin = ox.get_nearest_node(graph_orig,(float(origin[0]), float(origin[1])))
    destination =  ox.get_nearest_node(graph_orig,(float(destination[0]), float(destination[1])))
    bbox = ox.bbox_from_point((float(origin[0]), float(origin[1])), distance=1500, project_utm=True)

    '''
    We have to implement the get_min/max(graph, origin, dest, overheard) -> return min route , and even elevation ,
     route distance, (either in same function or different functions )
    '''
    # GET PATH, ELEVATION AND ROUTE_DISTANCE
    if elevation_type == MINIMUM:
       pass
    else: # MAXIMUM
        pass






    return route, elevation_gain, route_distance  #retun Route (list of lt lng) , elevation gain (number) , route_distance (float)