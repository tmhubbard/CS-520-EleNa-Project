
# This script was written by Trevor Hubbard; its purpose is to do some manipulation of
# points within an ellipse to figure out math

# =========================
#        * SETUP *
# =========================

from math import sin, cos, pi, atan
import numpy as np
import matplotlib.pyplot as plt
import googlemaps

# Setting up the Google Maps instance
apiKey = "AIzaSyC0_EhM25ltUK20oJPH4k4Ni6jqiU4bS2Q"
gmaps = googlemaps.Client(key=apiKey)

# =========================
#        * CLASSES *
# =========================

class Node:
    """
    Node class represets a node in a Graph
    """
    def __init__(
            self, 
            id: int, 
            latitude: float = None, longitude: float = None, 
            elevation: float = None,
            neighbors: list = None):
        self._id = id
        self._latitude = latitude
        self._longitude = longitude
        self._elevation = elevation
        self._neighbors = neighbors # [(neighborID, distance), (,), ...]
    
    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, id: int):
        self._id = id
    
    @property
    def latitude(self) -> float:
        return self._latitude
    
    @latitude.setter 
    def latitude(self, latitude: float):
        self._latitude = latitude
    
    @property
    def longitude(self) -> float:
        return self._longitude
    
    @longitude.setter 
    def longitude(self, longitude: float):
        self._longitude = longitude

    @property
    def elevation(self) -> float:
        return self._elevation
    
    @elevation.setter 
    def elevation(self, elevation: float):
        self._elevation = elevation

    @property
    def neighbors(self) -> list:
        return self._neighbors
    
    @neighbors.setter 
    def neighbors(self, neighbors: list):
        self._neighbors = neighbors
    
    def as_json(self) -> dict:
        return {
            "id": self._id,
            "latitude": self._latitude,
            "longitude": self._longitude,
            "elevation": self._elevation
        }
    
    def get_content(self) -> dict:
        return {
            "id": self._id,
            "latitude": self._latitude,
            "longitude": self._longitude,
            "elevation": self._elevation,
            "neighbors": self._neighbors,
        }

# =========================
#       * METHODS *
# =========================

# This method will return the distance between the origin and 
# destination points (in meters). Pass the points as lat/long tuples
def distanceBetween(origin, destination):
	distanceMatrix = gmaps.distance_matrix(origin, destination)
	return distanceMatrix["rows"][0]["elements"][0]["distance"]["value"]

# This will calculate the midpoint between point A and point B
def midpoint(pointA, pointB):
	midpointX = (pointA[0] + pointB[0])/2
	midpointY = (pointA[1] + pointB[1])/2
	return [midpointX, midpointY]

# This method will return True / False depending on whether 
# the given point is in the ellipse defined by h, k, rx, and ry
def inEllipse(point, h, k, rx, ry):
	curX, curY = point
	firstFraction = ((curX-h)**2)/(rx**2)
	secondFraction = ((curY-k)**2)/(ry**2)
	result = firstFraction+secondFraction
	if (result <= 1): return True
	else: return False

# This will give the coordinates for a given point when its coordinate system
# is rotated counter-clockwise by the provided angle
def rotatePoint(point, angle):
	x_old, y_old = point
	x_new = x_old * cos(angle) - y_old * sin(angle)
	y_new = x_old * sin(angle) + y_old * cos(angle)
	return [x_new, y_new]

# This will return a new (lat, long) coordinate pair representing
# the (lat, long) at origin offset by offset[0] meters north and offset[1] meters west
def offsetCoordinates(origin, offset):
	originLat, originLong = origin
	xOffset, yOffset = offset

	# print("The rotated point has coords %s" % offset)

	magic = 111111
	latChagne = yOffset/magic
	midLat = originLat
	longChange = xOffset/(magic*cos((pi * midLat)/180))
	newLat = originLat + latChagne
	newLong = originLong + longChange
	return (newLat, newLong)

# This method, when given (lat, long) pairs origin and destination, will
# return a list of (lat, long) pairs corresponding to a boundary box around them.
def boundaryBoxPoints(origin, destination, c, spacing):

	# Figure out if the origin or the destination is on the left
	if (origin[1] == destination[1]):
		destination[1] += 0.000001

	# Add the start and end nodes
	nodeList = []
	nodeList.append(Node(0, latitude=origin[0], longitude=origin[1]))
	nodeList.append(Node(-1, latitude=destination[0], longitude=destination[1]))

	# Switching the points if the destination is to the left of the origin
	switched = False
	if (destination[1] < origin[1]):
		temp = origin
		origin = destination
		destination = temp
		switched = True

	pointDistance = distanceBetween(origin, destination)
	longDiff = distanceBetween(origin, (origin[0], destination[1]))
	latDiff = distanceBetween(origin, (destination[0], origin[1]))
	angleRad = (atan(latDiff/longDiff))

	# Setting up some of the important calculations for the boundary box
	pointA = [0, 0]
	pointB = [pointDistance, 0]
	rotatedDestination = np.array(rotatePoint(pointB, angleRad))
	rotatedMidpoint = rotatePoint([pointDistance/2, 0], angleRad)
	midpointLatLong = offsetCoordinates(origin, rotatedMidpoint)
	c = 1.5
	x = np.linalg.norm(np.array(pointA)-np.array(pointB))
	z = (x/2) * np.sqrt((c**2 - 1))

	# Declaring some of the points for the boundary box
	cOffset = (x * (c-1)/2)
	topLeft = ([(pointA[0] - cOffset), z])
	topRight = ([pointB[0] + cOffset, z])
	bottomLeft = ([(pointA[0] - cOffset), -z])
	bottomRight = ([pointB[0] + cOffset, -z])

	# Declaring some of the x values used to draw the boundary box line
	top_x = [topLeft[0], topRight[0]]
	bottom_x = top_x
	left_x = [topLeft[0], topLeft[0]]
	right_x = [topRight[0], topRight[0]]

	# Declaring some of the y vlaues used to draw the boundary box line
	top_y = [topLeft[1], topLeft[1]]
	bottom_y = [bottomLeft[1], bottomLeft[1]]
	left_y = [bottomLeft[1], topLeft[1]]
	right_y = left_y

	# This is an important ratio
	widthHeightRatio = 1.15

	# Set desired number of points
	vertPointAmt = (z*2/spacing)
	horizPointAmt = (x/spacing)
	vertPointAmt = (round(vertPointAmt))
	horizPointAmt = (round(horizPointAmt))

	spaceX = x/(horizPointAmt+1)
	spaceY = (2*z)/(vertPointAmt+1)
	horizPoints = []
	vertPoints = []

	horizPoints = list(np.linspace(topLeft[0]+spaceX, topRight[0]-spaceX, horizPointAmt))
	vertPoints = list(np.linspace(topLeft[1]-spaceY/2, bottomLeft[1]+spaceY/2, vertPointAmt))

	allPoints = []
	nodeIDDict = {}
	nodeIDToAllPoints = {}
	nodeIDToAllPoints_opposite = {} 
	for vertNum, vertCoord in enumerate(vertPoints):
		for horizNum, horizCoord in enumerate(horizPoints):
			curNodeID = (vertNum * len(horizPoints)) + (horizNum + 1)
			if (curNodeID not in nodeIDDict):
				nodeIDDict[curNodeID] = []
			allPoints.append([horizCoord, vertCoord])
			nodeIDToAllPoints[len(allPoints)-1] = curNodeID
			nodeIDToAllPoints_opposite[curNodeID] = len(allPoints)-1

			# Top row of neighbors
			if (vertNum > 0):
				if (horizNum > 0):	# left
					neighborID = ((vertNum-1) * len(horizPoints)) + (horizNum)
					nodeIDDict[curNodeID].append(neighborID)

				# middle
				neighborID = (vertNum-1) * len(horizPoints) + (horizNum+1)
				nodeIDDict[curNodeID].append(neighborID)

				# right
				if (horizNum < len(horizPoints)-1):
					neighborID = (vertNum-1) * len(horizPoints) + (horizNum+2)
					nodeIDDict[curNodeID].append(neighborID)

			# Middle row of neighbors
			if (horizNum > 0): 		# left
				neighborID = ((vertNum) * len(horizPoints)) + (horizNum)
				nodeIDDict[curNodeID].append(neighborID)

			if (horizNum < len(horizPoints)-1):		# right
				neighborID = (vertNum) * len(horizPoints) + (horizNum+2)
				nodeIDDict[curNodeID].append(neighborID)

			# Bottom row of neighbors
			if (vertNum < (len(vertPoints)-1)):

				if (horizNum > 0):	# left
					neighborID = ((vertNum+1) * len(horizPoints)) + (horizNum)
					nodeIDDict[curNodeID].append(neighborID)

				# middle
				neighborID = (vertNum+1) * len(horizPoints) + (horizNum+1)
				nodeIDDict[curNodeID].append(neighborID)

				# right
				if (horizNum < len(horizPoints)-1):
					neighborID = (vertNum+1) * len(horizPoints) + (horizNum+2)
					nodeIDDict[curNodeID].append(neighborID)

	goodPoints = []
	badPoints = []
	badNodeIDs = []
	goodNodeIDs = []
	ellipseMidpoint = (midpoint(pointA, pointB))
	for pointNum, point in enumerate(allPoints):
		h, k = ellipseMidpoint
		rx = x/2 + cOffset
		ry = z
		if (inEllipse(point, h, k, rx, ry)):
			goodPoints.append(point)
			goodNodeIDs.append(nodeIDToAllPoints[pointNum])
		else:
			badPoints.append(point)
			badNodeIDs.append(nodeIDToAllPoints[pointNum])



	rotatedPoints = [rotatePoint(point, angleRad) for point in allPoints]
	newPoints = [offsetCoordinates(origin, point) for point in rotatedPoints]


	# Make the nodes
	startNeighbors = {}
	endNeighbors = {}
	for pointNum, newPoint in enumerate(newPoints):

		# Skip this node if it's a badNode
		curNodeID = nodeIDToAllPoints[pointNum]
		if (curNodeID in badNodeIDs):
			continue

		# Figure out the distance between this node and the start node
		curPointOffset = np.array(rotatedPoints[pointNum])
		startNeighbors[curNodeID] = np.linalg.norm(curPointOffset)
		endNeighbors[curNodeID] = np.linalg.norm(curPointOffset - rotatedDestination)

		# Put together the list of neighbors 
		neighborList = []
		for neighborID in nodeIDDict[curNodeID]:
			if (neighborID in badNodeIDs): continue

			# Calculate the distance between the two points
			neighborPointOffset = np.array(rotatedPoints[nodeIDToAllPoints_opposite[neighborID]])
			pointDist = np.linalg.norm(curPointOffset-neighborPointOffset)
			neighborList.append((neighborID, pointDist))

		nodeList.append(Node(curNodeID, latitude=newPoints[pointNum][0], longitude=newPoints[pointNum][1], neighbors = neighborList))

	sortedStart = {k: v for k, v in sorted(startNeighbors.items(), key=lambda item: item[1])}
	sortedEnd = {k: v for k, v in sorted(endNeighbors.items(), key=lambda item: item[1])}

	startNeighborList = ([(nodeID, distance) for nodeID, distance in sortedStart.items()][:8])
	endNeighborList = ([(nodeID, distance) for nodeID, distance in sortedEnd.items()][:8])

	# Edit the start and end nodes of the nodelist 
	if (not switched):
		nodeList[0].neighbors = startNeighborList
		nodeList[1].neighbors = endNeighborList
	else:
		nodeList[0].neighbors = endNeighborList
		nodeList[1].neighbors = startNeighborList

	# Uncomment this for visual aids
	# plt.plot(pointA[0], pointA[1], "go", markersize=15)
	# plt.plot(pointB[0], pointB[1], "ro", markersize=15)
	# plt.plot(longDiff, latDiff, "r+", markersize=20)
	# for pointNum, point in enumerate(rotatedPoints):
	# 	plt.plot(point[0], point[1], "go", markersize=2)
	# 	plt.text(point[0], point[1], nodeIDToAllPoints[pointNum])
	# plt.show()

	return nodeList, (midpointLatLong, (pointDistance/2)+cOffset)

# =========================
#        * MAIN * 
# =========================

# Get the coordinates from the front-end
origin = (42.372391, -72.516950)
# destination = (42.372268, -72.511058)
#
# nodes, center = boundaryBoxPoints(origin, destination, 1.5, 30)
# print(center)