
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

	pointDistance = distanceBetween(origin, destination)
	longDiff = distanceBetween(origin, (origin[0], destination[1]))
	latDiff = distanceBetween(origin, (destination[0], origin[1]))
	angleRad = (atan(latDiff/longDiff))

	# Setting up some of the important calculations for the boundary box
	pointA = [0, 0]
	pointB = [pointDistance, 0]
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
	for horizCoord in horizPoints:
		for vertCoord in vertPoints:
			allPoints.append([horizCoord, vertCoord])

	goodPoints = []
	badPoints = []
	ellipseMidpoint = (midpoint(pointA, pointB))
	for point in allPoints:
		h, k = ellipseMidpoint
		rx = x/2 + cOffset
		ry = z
		if (inEllipse(point, h, k, rx, ry)):
			goodPoints.append(point)
		else:
			badPoints.append(point)

	rotatedPoints = [rotatePoint(point, angleRad) for point in goodPoints]
	newPoints = [offsetCoordinates(origin, point) for point in rotatedPoints]

	# # Uncomment this for visual aids
	# plt.plot(pointA[0], pointA[1], "go", markersize=15)
	# plt.plot(pointB[0], pointB[1], "ro", markersize=15)
	# plt.plot(longDiff, latDiff, "r+", markersize=20)
	# for point in rotatedPoints:
	# 	plt.plot(point[0], point[1], "go", markersize=2)
	# plt.show()


	return newPoints

# =========================
#        * MAIN * 
# =========================

# Get the coordinates from the front-end
origin = (42.372391, -72.516950)
destination = (42.372268, -72.511058)

points = boundaryBoxPoints(origin, destination, 1.5, 30)
