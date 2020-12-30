import matlab.engine

class LPSolving:

    def __init__(self, hrrc, hrrcIndices, d, delta, diameter, func):
        '''hrrc - a hierarchy for a set s, hrrcIndices - original indices of hrrc with compatiblity to the points in the
           original set, d - the target double dimension, delta - the minimal distance between two points in s, func - a matrix
           which contains the distances between the points in s'''
        self.hrrc = hrrc
        self.hrrcIndices = hrrcIndices
        self.d = d
        self.delta = delta
        self.diameter = diameter
        self.func = func

    def solve(self):
        alpha = [7, 24, 75] # originally, 588,612 were included, but they implicate very large numbers, and the linprog of
                            # matlab can't deal with them (the smallest of them is (588*2)^5 in the case of d=1)
        t = len(self.hrrc) - 1
        dTag = 4 * self.d + 1
        n = len(self.hrrc[t])  # size of the points set s

        # given hierarchy hrrc, hrrcLenAcc holds in the i-th cell, the accumulated number of elements in hrrc[0] to hrrc[i]
        hrrcLenAcc = [len(self.hrrc[0])]
        for i in range(t):
            hrrcLenAcc.append(hrrcLenAcc[i] + len(self.hrrc[i+1]))

        sumIndicatorVars = hrrcLenAcc[-1]  # the number of Zij indicators

        # c is the vector that the LP will minimize
        c = [1] * n + [0] * sumIndicatorVars

        # initializing the matrix A and the vector b for the LP minimization

        A = []
        b = []

        # constraint #9
        variablesZij = [0,1] * sumIndicatorVars

        # constraint #10
        helpList = [0] * n

        firstConstraint = [0] * sumIndicatorVars
        firstConstraint[0] = 1
        firstConstraint[1] = -1
        firstConstraint = helpList + firstConstraint
        A.append(firstConstraint)
        b.append(0)
        for i in range (1, t, 1):
            for j in range(len(self.hrrc[i])):
                nextVector = [0] * sumIndicatorVars
                nextVector[hrrcLenAcc[i-1] + j] = 1
                nextVector[hrrcLenAcc[i] + j] = -1
                nextVector = helpList + nextVector
                A.append(nextVector)
                b.append(0)

        # constraint #11
        for a in alpha:
            for i in range(t + 1):
                for p in self.hrrc[-1]:
                    indices = self.findNeighborhood(a, p, self.hrrc[i], i)
                    myVector = [0] * (n + sumIndicatorVars)
                    for j in indices:
                        myVector[n + hrrcLenAcc[i] - len(self.hrrc[i]) + j] = 1
                    A.append(myVector)
                    b.append(pow(2 * a, dTag))

        # constraint # 12
        for i in range(t + 1):
            for p in self.hrrc[-1]:
                indices = self.findNeighborhood(7, p, self.hrrc[i], i)
                myVector = [0] * (n + sumIndicatorVars)
                for j in indices:
                    myVector[n + hrrcLenAcc[i] - len(self.hrrc[i]) + j] = -1
                myVector[n + hrrcLenAcc[t] - len(self.hrrc[t]) + self.hrrc[-1].index(p)] += 1
                A.append(myVector)
                b.append(0)

        # constraint # 13
        helpConst = pow(48, -dTag)
        for i in range(t + 1):
            for k in range(i+1, t+1, 1):
                for p in self.hrrc[-1]:
                    indices = self.findNeighborhood(24, p, self.hrrc[i], i)
                    myVector = [0] * (n + sumIndicatorVars)
                    for j in indices:
                        myVector[n + hrrcLenAcc[i] - len(self.hrrc[i]) + j] = -1
                    indices = self.findNeighborhood(24, p, self.hrrc[k], k)
                    for j in indices:
                        myVector[n + hrrcLenAcc[k] - len(self.hrrc[k]) + j] += helpConst
                    A.append(myVector)
                    b.append(0)

        # constraint # 14
        variablesCj = [0,"Inf"] * n

        variables = variablesCj + variablesZij

        # constraint # 15

        helpVector = [0] * (n + sumIndicatorVars)
        for i in range(n):
            nextVector = helpVector + []
            nextVector[i] = -1 / self.delta
            nextVector[n + hrrcLenAcc[-2] + i] = -1
            A.append(nextVector)
            b.append(-1)

        # constraint # 16
        for i in range(t + 1):
            for p in self.hrrc[-1]:
                indices = self.findNeighborhood(12, p, self.hrrc[i], i)
                myVector = [0] * (n + sumIndicatorVars)
                for j in indices:
                    myVector[n + hrrcLenAcc[i] - len(self.hrrc[i]) + j] = -1
                myVector[n + hrrcLenAcc[-1] - len(self.hrrc[-1]) + self.hrrc[-1].index(p)] -= 1
                myVector[self.hrrc[-1].index(p)] -= pow(2, i)
                A.append(myVector)
                b.append(-1)

        # we save all vectors which are needed for the linear programming, to run a solver in Matlab
        file = open('input_hrrc', 'w')
        file.write(''.join(str(e) for e in self.hrrc))
        file.close()

        print "num of vars: ", n+ sumIndicatorVars, " and num of equations is: ", len(A)

        # saving the needed parameters for linear programming
        file = open('input_A', 'w')
        file.write(''.join(str(A)))
        file.close()

        file = open('input_b', 'w')
        file.write(''.join(str(b)))
        file.close()

        file = open('input_c', 'w')
        file.write(''.join(str(c)))
        file.close()

        file = open('input_bounds', 'w')
        file.write(''.join(str(variables)))
        file.close()

        file = open('hrrc', 'w')
        file.write(''.join(str(self.hrrc)))
        file.close()

        eng = matlab.engine.start_matlab()
        eng.edit('linprogMatlab', nargout=0)
        x = eng.linprogMatlab()
        print x


        # # rounding the answers
        #
        # print(res.x) # ****************************************
        # print(res.x[10:])  # ****************************************
        #
        # # rounding - part 3
        # roundedVector = [0] * sumIndicatorVars
        #
        # # rounding - part 1
        # for i in range(sumIndicatorVars - n, sumIndicatorVars, 1):
        #     if res.x[i] >= 0.5:
        #         roundedVector[i] = 1
        #
        # print(roundedVector)
        #
        # # helper matrix which contains true in [i][j]'th cell if there is a k>=i such that sigma(N-k-j) >= 0.25,
        # # when N-k-j is the neighborhood of vertex j in the k-th set in the hierarchy, and the sum is on the values of
        # # the indicator variables which were received from the LP
        # largerThanQuarter = []
        #
        # # print ("t=", t) # **************************************
        #
        # for i in range (t, -1, -1):
        #     newRow = []
        #     for p in self.hrrc[-1]:
        #
        #         # print(i) # **************************************
        #         # if i!=t:
        #         #     print (largerThanQuarter[0])
        #
        #         if i != t and largerThanQuarter[0][self.hrrc[-1].index(p)] == True:
        #             newRow.append(True)
        #         else:
        #             pNeighborhoodIndices = self.findNeighborhood(24, p, self.hrrc[i], i)
        #             sum = 0
        #             for j in pNeighborhoodIndices:
        #                 sum += res.x[n + hrrcLenAcc[i] - len(self.hrrc[i]) + j]
        #             if sum >= 0.25:
        #                 newRow.append(True)
        #             else:
        #                 newRow.append(False)
        #     largerThanQuarter = [newRow] + largerThanQuarter
        #
        # # rounding - part 2
        # for i in range (t+1):
        #     allIndices = []
        #     for p in self.hrrc[-1]:
        #         currentIndices = self.findNeighborhood(24, p, self.hrrc[i], i)
        #
        #         # checking conditions (i) and (ii)
        #         if(not self.checkIntersection(allIndices, currentIndices) and largerThanQuarter[i][self.hrrc[-1].index(p)]):
        #             allIndices = self.unionSets(allIndices, currentIndices)
        #             closest = self.findClosest(p, self.hrrc[i])
        #             closestIndex = self.hrrc[-1].index(closest)
        #             for k in range (i, t+1, 1):
        #                 roundedVector[hrrcLenAcc[i] - len(self.hrrc[i]) + closestIndex] = 1
        #
        # #extracting the set W
        # returnedSet = []
        # for i in range(sumIndicatorVars - n, sumIndicatorVars, 1):
        #     if roundedVector[i] == 1:
        #         returnedSet.append(self.hrrc[-1][i - (sumIndicatorVars - n)])
        #
        # return returnedSet


    def findClosest(self, point ,set):
        'find the closest point in the set to given point'
        pointIndex = self.hrrcIndices[self.hrrc[-1].index(point)]
        startIndex = self.hrrcIndices[self.hrrc[-1].index(set[0])]
        minimum = self.func[pointIndex][startIndex]
        closest = set[0]
        for p in set:
            pIndex = self.hrrcIndices[self.hrrc[-1].index(p)]
            if minimum > self.func[pointIndex][pIndex]:
                minimum = self.func[pointIndex][pIndex]
                closest = p
        return closest

    def findNeighborhood(self, alpha, point, set, i):
        'given a point and a set, returns a sorted list of all points in the set, in the i-level neighborhood (size of alpha) of the point'
        closest = self.findClosest(point, set)
        neighbors = []
        closestIndex = self.hrrcIndices[self.hrrc[-1].index(closest)]
        for p in set:
            pIndex = self.hrrcIndices[self.hrrc[-1].index(p)]
            if self.func[closestIndex][pIndex] / self.diameter <= alpha * pow(2, -i):
                neighbors.append(set.index(p))

        return neighbors

    def checkIntersection(self, list1, list2):
        'checks intersection between two sorted lists'
        index1 = 0
        index2 = 0
        while index1 < list1.__len__() and index2 < list2.__len__():
            if list1[index1] == list2[index2]:
                return True
            elif list1[index1] < list2[index2]:
                index1 += 1
            else:
                index2 += 1
        return False

    def unionSets(self, list1, list2):
        'returns a sorted union list of two sorted lists'
        unionSet = []
        index1 = 0
        index2 = 0
        i = 0
        while index1 < list1.__len__() and index2 < list2.__len__():
            if list1[index1] == list2[index2]:
                unionSet.append(list1[index1])
                index1 += 1
                index2 += 1
            elif list1[index1] <= list2[index2]:
                unionSet.append(list1[index1])
                index1 += 1
            else:
                unionSet.append(list2[index2])
                index2 += 1
            i += 1
        if index1 < list1.__len__():
            for i in range(index1, list1.__len__(), 1):
                unionSet.append(list1[i])
        elif index2 < list2.__len__():
            for i in range(index2, list2.__len__(), 1):
                unionSet.append(list2[i])
        return unionSet