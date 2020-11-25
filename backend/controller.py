
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



def get_route_data(origin, destination, elevation_type, overhead):
    # GENERATE GRAPH
    G = get_graph(origin, destination, overhead)

    # GET PATH AND ELEVATION
    if elevation_type == MINIMUM:
        path, elevation_gain = get_minimum_path_and_elevation(
            G, 
            source=SOURCE, target=TARGET, 
            overhead=overhead
        )
    else: # MAXIMUM
        path, elevation_gain = get_maximum_path_and_elevation(
            G, 
            source=SOURCE, target=TARGET, 
            overhead=overhead
        )
    
    # GET PATH/ROUTE DISTANCE
    route_distance = calcRouteDistance(G, path)

    # CONVERT PATH TO LATITUDE, LONGITUDE List to pass to the front end
    route = nodes_to_lat_lng_coordinates(G, path)

    # Elevation gain and route distance to 3 decimal places
    elevation_gain = round(elevation_gain, 3)
    route_distance = round(route_distance, 3)
    
    return route, elevation_gain, route_distance