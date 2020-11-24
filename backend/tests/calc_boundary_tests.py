import unittest

from math import pi
from model.graph.calcBoundary import midpoint
from model.graph.calcBoundary import inEllipse
from model.graph.calcBoundary import offsetCoordinates
from model.graph.calcBoundary import rotatePoint

class CalcBoundaryTests(unittest.TestCase):
    
    def test_midpoint(self):
        """Test to see if the midpoint function is working correctly
        """
        pointA = [1, 5]
        pointB = [3, 5]
        middlePoint = midpoint(pointA, pointB)
        assert middlePoint==[2, 5], ("middlePoint was %s when it should have been [2, 5]" % str(middlePoint))

    def test_inEllipse(self):
        """Test to see if the inEllipse function is working correctly
        """
        pointA = [-2, 2]
        pointB = [2, 2]
        ellipseH = 3
        ellipseK = 3
        ellipseRX = 3.5
        ellipseRY = 10

        inEllipse_A = inEllipse(pointA, ellipseH, ellipseK, ellipseRX, ellipseRY)
        inEllipse_B = inEllipse(pointB, ellipseH, ellipseK, ellipseRX, ellipseRY)

        assert inEllipse_A==False, "This point is outside of the ellipse specified by these parameters"
        assert inEllipse_B==True, "This point *is* inside of the ellipse specified by these parameters"

    def test_offsetCoordinates(self):
        """Test to see if the offsetCoordinates function is working correctly
        """
        originPoint = (42.360806, -72.510809)
        pointOffset = (0, 222222)
        newPoint = offsetCoordinates(originPoint, pointOffset)
        assert newPoint == (44.360806, -72.510809), "The new point ought to have been at (44.360806, -72.510809)"

    def test_rotatePoint(self):
        """Test to see if the rotatePoint function is working correctly
        """
        pointA = [5, 3]
        angle = pi/2
        rotatedA = [round(x) for x in rotatePoint(pointA, angle)]
        assert rotatedA==[-3, 5], "The rotated point (%s) ought to have been [-3, 5] " % rotatedA
