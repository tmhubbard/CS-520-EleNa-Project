# import matplotlib.pyplot as plt
# from model.graph.calcBoundary import midpoint

# # This method will help me visualize the path that the nodes give
# def visualizePath(nodes, NodeIDToNodesIdx, path):
#     for node in nodes:
#         plt.plot(node.longitude, node.latitude, "go", markersize=10)
#         plt.text(node.longitude, node.latitude, ("%s (%.2f)" % (str(node.id), node.elevation)))

#     # Plot the lines between neighbors
#     linesDrawn = {}
#     for node in nodes: 
#         # Step through each of the neighbors in node's neighborList
#         for neighborNode in node.neighbors:

#             neighborNodeID, neighborNodeDist = neighborNode

#             # Draw the line between this node and neighborNode if it hasn't already been drawn
#             if ((neighborNodeID, node.id) in linesDrawn): continue
#             longitudes = (node.longitude, nodes[NodeIDToNodesIdx[neighborNodeID]].longitude)
#             latitudes = (node.latitude, nodes[NodeIDToNodesIdx[neighborNodeID]].latitude)
#             plt.plot(longitudes, latitudes, "g-")
#             lineMidpoint = midpoint([node.longitude, node.latitude], [nodes[NodeIDToNodesIdx[neighborNodeID]].longitude, nodes[NodeIDToNodesIdx[neighborNodeID]].latitude])
#             plt.text(lineMidpoint[0], lineMidpoint[1], ("%.2f" % float(neighborNodeDist)))

#     # Draw a line for the path 
#     for pathNodeNum, pathNodeID in enumerate(path):

#         # Skip this node if it's the last one 
#         if (pathNodeNum == len(path)-1): continue

#         # Highlight the path in red
#         thisNode = nodes[NodeIDToNodesIdx[pathNodeID]]
#         nextNode = nodes[NodeIDToNodesIdx[path[pathNodeNum+1]]]
#         longitudes = (thisNode.longitude, nextNode.longitude)
#         latitudes = (thisNode.latitude, nextNode.latitude)
#         plt.plot(longitudes, latitudes, "r-", linewidth=5)

#     # Show the pyplot
#     plt.show()