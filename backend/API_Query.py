import json
import urllib
import requests
import osmnx as ox

place_query = {'city':'Amherst', 'state':'Massachusetts', 'country':'USA'}
pq2 = "154 Hicks Way, Amherst, MA 01003"
graph_orig = ox.graph_from_address(pq2, dist = 1000, network_type='walk')
ox.plot_graph(graph_orig)
breakpoint()

def elevation(location):
    lat = location[0]
    lng = location[1]
    apikey = "AIzaSyBmg_5waDYCtmUW3YCNJ75dUWc6_5_i8wE"
    url = "https://maps.googleapis.com/maps/api/elevation/json"
    request = requests.get(url+"?locations="+str(lat)+","+str(lng)+"&key="+apikey).json()
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
    #request = requests.get(url  + str(lat) + "," + str(lng) + "&key=" + apikey)
    #print(request)
    #return request




    """
    this function would return different sampled nodes with their elevations which are valid
    :input type : List[(lat,long)]  
    :rtype: List[(lat,long,elevation)]  
    
    """

locations = [(35.929673, -78.948237), (38.889510, -77.032000), (38.032120, -78.477510)]
locations2=(35.929673, -78.948237)
print(valid_location(locations2))
def elevations(locations):
    Nodes = []
    for location in locations:
        #check valid here
        node = (location[0], location[1], elevation(location))
        Nodes.append(node)
    return Nodes

print(elevations(locations=locations))



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






