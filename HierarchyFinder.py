import random
import copy
import math
import numpy as np


class HierarchyFinder:
    """This class finds a hierarchy.
    The input is a set S of points (represented as list) and a distance function (represented as matrix)."""

    def findHierarchy(self, points, distances):
        # scaling the distances function s.t. the biggest distance will be 1 and the relations between the distances are preserved
        scaledFunction = self.inputScaler(copy.deepcopy(distances))

        # diameter = the diameter of the set
        diameter = distances[0][0]
        for i in range(len(distances)):
            for j in range(len(distances)):
                if(diameter < distances[i][j]):
                    diameter = distances[i][j]
        diameter = float(diameter)

        # a boolean array to indicate which points are still not in the hierarchy
        remainedPoints = np.ones(len(points))

        # choose a random point for the first set in the hierarchy (the first is as good as any)
        pointsHierarchy = [[points[0]]]
        # marking that the first point is in the first set (this will stay right in the next sets because Vi is a subset
        # of Vi+1 for any i from 0 to t-1)
        remainedPoints[0] = 0

        # build the next set in the hierarchy according to the previous set
        # the condition means that the last set in the hierarchy contains all the points in points
        # the condition will stop after t iterations, when t = ceil(log(1/delta)), when delta is the smallest distance
        j = 1
        while (len(pointsHierarchy[len(pointsHierarchy) - 1]) < len(points)):
            pointsHierarchy.append(copy.deepcopy(pointsHierarchy[len(pointsHierarchy) - 1])) # first, we add all the points of the last set to the new set
            for i in range(len(points)):                                                       # and then building the next set according the proper limits
                if (remainedPoints[i] == 1 and self.distanceBetweenPointAndSet(points[i], pointsHierarchy[
                        len(pointsHierarchy) - 1], distances, points) / diameter >= math.pow(2, -j)):
                    pointsHierarchy[len(pointsHierarchy) - 1].append(points[i])
                    remainedPoints[i] = 0
            j += 1
        return pointsHierarchy

    def buildInputSet(self, dimensionSizes, numOfPoints):
        points = []
        i = 0
        while i< numOfPoints:
            newPoint = []
            for dimSize in dimensionSizes:
                rand = int(random.random() * dimSize) # if fractional coefficients are required, the casting should be removed
                newPoint.append(rand)
            if not newPoint in points:
                points.append(newPoint)
                i += 1
        return points

    def buildInputFunction(self, set, pNorm):
        "given a @set, generates table of distances according the given @pNorm"
        distancesMatrix = []
        for i in range(len(set)):
            row = []
            for j in range(len(set)):
                row.append(self.distanceBetweenTwoPoints(set[i], set[j], pNorm))
            distancesMatrix.append(row)
        return distancesMatrix

    def distanceBetweenTwoPoints(self, p1, p2, pNorm):
        distance = 0
        for i in range(len(p1)):
            distance += pow(abs(p1[i]-p2[i]), pNorm)
        distance = pow(distance, 1.0/pNorm)
        return distance

    def distanceBetweenPointAndSet(self, point, set, distances, allPoints):
        pointIndex = allPoints.index(point)
        firstPointIndex = allPoints.index(set[0])
        minimum = distances[pointIndex][firstPointIndex]
        i = 1
        while(i < len(set)):
            minimum = min(minimum, distances[pointIndex][allPoints.index(set[i])])
            i += 1
        return minimum

    def findHrrcIndices(self, inputSet, hrrcLastSet):
        """gets the original set of points -@inputSet- and the last hierarchy -@hrrcLastSet, where all the points also exist but in different
        order, and returns their order according the @inputSet"""
        indices = []
        for i in range (len(inputSet)):
            indices.append(inputSet.index(hrrcLastSet[i]))
        return indices

    # scales the input distances function, which is a matrix of integer
    # the scaling make the biggest distance to be 1, and preserve the ratio between the distances
    # this function is not used because actually we don't need to scale for the computations, but in the article it
    # mentioned, so we added the option
    def inputScaler(self, func):
        # find the biggest distance in the function (a.k.a. diameter)
        diameter = 0
        for i in range(len(func)):
            for j in range(len(func)):
                if(diameter < func[i][j]):
                    diameter = func[i][j]
        # divides all the values in the value of the biggest distance
        for i in range(len(func)):
            for j in range(len(func)):
                func[i][j] = float(func[i][j]) / diameter
        return func

