
# This script was written by Trevor Hubbard; its purpose is to figure out an 
# ellipse boundary around an origin and destination, and figure out (lat, long)
# points within this ellipse to use as sample points for the EleNa graph 

from math import sin, cos, pi, atan
import numpy as np
import googlemaps
from model.graph.node import Node


# Setting up the Google Maps instance
apiKey = input("\nPlease enter your Google Maps API key: ")
gmaps = googlemaps.Client(key=apiKey)

def distanceBetween(origin, destination):
	"""This method will return the distance between the origin and 
	   destination points (in meters). Pass the points as lat/long tuples
	"""
	distanceMatrix = gmaps.distance_matrix(origin, destination)
	return distanceMatrix["rows"][0]["elements"][0]["distance"]["value"]

def distanceBetweenDict(origin, destinationList):
	"""This method will return the distance between the origin and the 
	   list of destinations
	"""
	
	# Generate distDict (which is a dict of destNum (idx of destinationList) --> distance from origin)
	# This has some pagination so that we don't query more than Google Maps's max element amount 
	distDict = {} 
	maxElements = 100
	destLists = [destinationList[i * maxElements:(i + 1) * maxElements] for i in range((len(destinationList) + maxElements - 1) // maxElements )]
	for destListNum, destList in enumerate(destLists):
		for destNum, dest in enumerate((gmaps.distance_matrix(origin, destList))["rows"][0]["elements"]):
			destNum = destNum + (maxElements * destListNum)
			distDict[destNum] = dest["distance"]["value"]

	# Sort the destination dict by distance, and return it
	distDict = {k: v for k, v in sorted(distDict.items(), key=lambda item: item[1])}
	return distDict

def midpoint(pointA, pointB):
	"""This will calculate the midpoint between point A and point B
	"""
	midpointX = (pointA[0] + pointB[0])/2
	midpointY = (pointA[1] + pointB[1])/2
	return [midpointX, midpointY]

def inEllipse(point, h, k, rx, ry):
	"""This method will return True / False depending on whether 
       the given point is in the ellipse defined by h, k, rx, and ry
	"""
	curX, curY = point
	firstFraction = ((curX-h)**2)/(rx**2)
	secondFraction = ((curY-k)**2)/(ry**2)
	result = firstFraction+secondFraction
	if (result <= 1): return True
	else: return False

def rotatePoint(point, angle):
	"""This will give the coordinates for a given point when its coordinate system
   	   is rotated counter-clockwise by the provided angle
	"""
	x_old, y_old = point
	x_new = x_old * cos(angle) - y_old * sin(angle)
	y_new = x_old * sin(angle) + y_old * cos(angle)
	return [x_new, y_new]

def offsetCoordinates(origin, offset):
	"""This will return a new (lat, long) coordinate pair representing
	   the (lat, long) at origin offset by offset[0] meters north and offset[1] meters west
	"""
	originLat, originLong = origin
	xOffset, yOffset = offset
	magic = 111111
	latChange = yOffset/magic
	midLat = originLat + latChange/2
	longChange = xOffset/(magic*cos((pi * midLat)/180))
	newLat = originLat + latChange
	newLong = originLong + longChange
	return (newLat, newLong)

def boundaryBoxPoints(origin, destination, c, spacing):

	"""This method, when given (lat, long) pairs origin and destination, will
	   return a list of (lat, long) pairs corresponding to a boundary box around them.
    """

	# If the destination is immediately above the origin, nudge it *very slightly* 
	# to the east (a bit hacky, but it works fine) 
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

	# Calculating the angle between the two points
	pointDistance = distanceBetween(origin, destination)
	longDiff = distanceBetween(origin, (origin[0], destination[1]))
	latDiff = distanceBetween(origin, (destination[0], origin[1]))
	angleRad = (atan(latDiff/longDiff))
	if (destination[0] < origin[0]):
		angleRad *= -1
		latDiff *= -1

	# Setting up some of the important calculations for the boundary box
	pointA = [0, 0]
	pointB = [pointDistance, 0]
	rotatedDestination = np.array((longDiff, latDiff))
	rotatedMidpoint = rotatePoint([pointDistance/2, 0], angleRad)
	midpointLatLong = offsetCoordinates(origin, rotatedMidpoint)
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

	# This ratio defines how many more points the width will have than
	# the height of the rectangle that's generated
	widthHeightRatio = 1.15

	# Set desired number of points
	vertPointAmt = (z*2/spacing)
	horizPointAmt = (x/spacing)
	vertPointAmt = (round(vertPointAmt))
	horizPointAmt = (round(horizPointAmt))

	# Create a horizontal and vertical point range w/ np.linspace
	spaceX = x/(horizPointAmt+1)
	spaceY = (2*z)/(vertPointAmt+1)
	horizPoints = []
	vertPoints = []
	horizPoints = list(np.linspace(topLeft[0]+spaceX, topRight[0]-spaceX, horizPointAmt))
	vertPoints = list(np.linspace(topLeft[1]-spaceY/2, bottomLeft[1]+spaceY/2, vertPointAmt))

	# Create all of the sample nodes and keep track of how they ought
	# to be connected to eachother in the eventual graph structure 
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

				# left
				if (horizNum > 0):	
					neighborID = ((vertNum+1) * len(horizPoints)) + (horizNum)
					nodeIDDict[curNodeID].append(neighborID)

				# middle
				neighborID = (vertNum+1) * len(horizPoints) + (horizNum+1)
				nodeIDDict[curNodeID].append(neighborID)

				# right
				if (horizNum < len(horizPoints)-1):
					neighborID = (vertNum+1) * len(horizPoints) + (horizNum+2)
					nodeIDDict[curNodeID].append(neighborID)

	# Figure out which points are inside of the ellipse, and add them to goodPoints
	# Add the other points to badPoints
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

	# Rotate the points, and then create their lat, long analogues in newPoints
	rotatedPoints = [rotatePoint(point, angleRad) for point in allPoints]
	newPoints = [offsetCoordinates(origin, point) for point in rotatedPoints]

	# Declare various dicts that I'll use to keep track of info during Node cretion
	startNeighbors = {}
	endNeighbors = {}
	nodeIDToNodeListIdx = {}
	nodeListIdxToID = {}
	nodeOffsetDict = {} 

	# Make the Node objects
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

		# Append this Node to the nodeLis, and store information about it 
		nodeList.append(Node(curNodeID, latitude=newPoints[pointNum][0], longitude=newPoints[pointNum][1], neighbors = neighborList))
		nodeListIdxToID[len(nodeList)-1] = curNodeID
		nodeOffsetDict[curNodeID] = curPointOffset
		nodeIDToNodeListIdx[curNodeID] = len(nodeList)-1

	# Figure out which nodes ought to be the neighbors of the start node
	latLongNodeList = [(x.latitude, x.longitude) for x in nodeList[2:]]
	distBetweenStartDict = distanceBetweenDict(origin, latLongNodeList)
	sortedLatLongIdxList_start = [(y+2) for y in distBetweenStartDict]
	distBetweenStart = [int(nodeListIdxToID[x]) for x in sortedLatLongIdxList_start]
	startNeighborList = [(x, distBetweenStartDict[nodeIDToNodeListIdx[x]-2]) for x in distBetweenStart][:8]

	# Figure out which nodes ought to be the neighbors of the end node
	distBetweenEndDict = distanceBetweenDict(destination, latLongNodeList)
	sortedLatLongIdxList_end = [(y+2) for y in distBetweenEndDict]
	distBetweenEnd = [nodeListIdxToID[x] for x in sortedLatLongIdxList_end]
	endNeighborList = [(x, distBetweenEndDict[int(nodeIDToNodeListIdx[x]-2)]) for x in distBetweenEnd][:8]

	# Add the start and end point offsets to the nodeOffsetDict
	if (not switched):
		nodeOffsetDict[0] = np.array((0, 0))
		nodeOffsetDict[-1] = np.array(rotatePoint((pointDistance, 0), angleRad))
	else:
		nodeOffsetDict[-1] = np.array((0, 0))
		nodeOffsetDict[0] = np.array(rotatePoint((pointDistance, 0), angleRad))

	# Add the neighbors from startNeighborList and endNeighborList to the respective neighborLists
	# of the neighbouring nodes
	for startNeighborPair in startNeighborList:
		idToAppend = 0
		if (switched): idToAppend = -1
		neighborID, dist = startNeighborPair
		nodeList[nodeIDToNodeListIdx[neighborID]].neighbors.append((idToAppend, dist))
	for endNeighborPair in endNeighborList:
		idToAppend = -1
		if (switched): idToAppend = 0
		neighborID, dist = endNeighborPair
		nodeList[nodeIDToNodeListIdx[neighborID]].neighbors.append((idToAppend, dist))

	# Edit the start and end nodes of the nodelist 
	if (not switched):
		nodeList[0].neighbors = startNeighborList
		nodeList[1].neighbors = endNeighborList
	else:
		nodeList[0].neighbors = endNeighborList
		nodeList[1].neighbors = startNeighborList

	return nodeList, (midpointLatLong, (pointDistance/2)+cOffset), nodeOffsetDict
