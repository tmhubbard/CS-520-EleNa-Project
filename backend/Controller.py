import requests
import osmnx as ox

# class controller(obj):
#
#     def _init_(self):
#     #initialize model and view here

#place_query = {'city':'Amherst', 'state':'Massachusetts', 'country':'USA'}
pq2 = "139 Starling way, Hercules CA"
graph_orig = ox.graph_from_address(pq2, dist = 1000, network_type='drive') #drive and bike
#graph_orig = ox.graph_orig.add_node_elevations(graph_orig, api_key= "AIzaSyBmg_5waDYCtmUW3YCNJ75dUWc6_5_i8wE")
#graph_orig = ox.add_edge_grades(graph_orig)
route_nodes= []
for i in range(10):
    node_id = list(graph_orig.nodes())[i]
    route_nodes.append(node_id)
breakpoint()
origin_lat , origin_long =38.003560 , -122.268830
bbox = ox.bbox_from_point((float(origin_lat), float(origin_long)), distance=1500, project_utm=True)
ox.plot_graph_route(graph_orig, route_nodes, bbox = bbox, node_size=0)
# #ox.plot_graph(graph_orig)
# breakpoint()