import osmnx as ox
import networkx as nx
import pickle as pkl
from enums import MINIMUM
import inspect, os
from max_search import maximize_elevation_gain
from min_search import minimize_elevation_gain
# from model.graph.make_graph import (
#     get_graph,
#     SOURCE, TARGET,
#     nodes_to_lat_lng_coordinates
# )
# from algorithm import (
#     get_minimum_path_and_elevation,
#     get_maximum_path_and_elevation,
#     calcRouteDistance
# )





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




def route_coordinates(Graph, route):
    geometry = nx.get_edge_attributes(Graph ,'geometry')
    route_coordinates = []
    for edge in route:
        src, tgt, edge_id = edge
        edge_data = Graph[src][tgt][edge_id]

        src_y, src_x = Graph.nodes[src]['y'], Graph.nodes[src]['x']
        tgt_y, tgt_x = Graph.nodes[tgt]['y'], Graph.nodes[tgt]['x']

        if 'geometry' not in edge_data:
            mid_y = (tgt_y + src_y) / 2
            mid_x = (tgt_x + src_x) / 2

        else:
            edge_linestring_coords = geometry[edge].coords
            mid_idx = int(len(edge_linestring_coords) / 2)
            mid_x, mid_y = list(edge_linestring_coords)[mid_idx]

        route_coordinates.extend(
            [{'Lat': src_y, 'Long': src_x}, {'Lat': mid_y, 'Long': mid_x}, {'Lat': tgt_y, 'Long': tgt_x}])

    route_cds = []

    if (len(route_coordinates) > 23):
        ll = int(len(route_coordinates) / 23 + 1)
        i = 0
        while (i < len(route_coordinates)):
            route_cds.extend([{'Lat': route_coordinates[i]['Lat'], 'Long': route_coordinates[i]['Long']}])
            i = i + ll

    # route_cds = route_cds[2:-2]

    return route_cds








def get_route_data(origin, destination, elevation_type, overhead):
    # GENERATE GRAPH

    #using pikle to read graph -> will see if this works
    G = nx.read_gpickle(os.path.dirname(os.path.abspath(inspect.stack()[0][1])) + "/amherst_graph.gpickle")


    graph_projection, graph_orig = get_map()

    source = ox.get_nearest_node(graph_orig,(float(origin[0]), float(origin[1])))
    target =  ox.get_nearest_node(graph_orig,(float(destination[0]), float(destination[1])))
    bbox = ox.bbox_from_point((float(origin[0]), float(origin[1])), distance=1500, project_utm=True)

    '''
 
    '''
    # GET PATH, ELEVATION AND ROUTE_DISTANCE
    if elevation_type == MINIMUM:
        min_elevation_route= minimize_elevation_gain( graph_orig, source, destination, overhead)
        route = route_coordinates(min_elevation_route)


    else: # MAXIMUM
        max_elevation_route = maximize_elevation_gain(graph_orig, source, target, overhead)
        route = route_coordinates(max_elevation_route)






    dummy_elevation = 45
    dummy_route_distance = 60
    return route, dummy_elevation, dummy_route_distance  #retun Route (list of lt lng) , elevation gain (number) , route_distance (float)