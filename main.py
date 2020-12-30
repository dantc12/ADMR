import HierarchyFinder as hf

import matlab.engine

import LPSolving as lps

eng = matlab.engine.start_matlab()
eng.sqrt(4.0)
eng.exit()

hrf = hf.HierarchyFinder()



# inputSet can be part of the input from the user. Right now, [10,11],12 means 12 random points, represented by vectors with 2 entrances:
# the first taken randomly from 0-10, and the second from 0-11. All the coefficients are integers, due to convenience reasons,
# but it can be easily changed, as described in the function buildInputSet
inputSet = hrf.buildInputSet([10, 11], 12)

# # test: @inputSet is a straight line in R^10 and @noiseSet consists of 9 points very close to points on the line,
# #   but their union is a 10 dimensional set
# inputSet = []
# for i in range(100):
#     inputSet.append([float(i), 0., 0., 0., 0., 0., 0., 0., 0., 0.])
# noiseSet = []
# for i in range(1, 10):
#     noiseSet.append([i * 10., 0., 0., 0., 0., 0., 0., 0., 0., 0.])
# for i in range(len(noiseSet)):
#     noiseSet[i][i+1] += 0.0001
# inputSet.extend(noiseSet)


# printing the generated set
for i in range(len(inputSet)):
    print(inputSet[i])

pNorm = 1 # as defualt, the program calculates the distances with p-norm

inputFunction = hrf.buildInputFunction(inputSet, pNorm)  # this is the table of distances between the inputSet's points
                                                            # if a specific metric space is given by a table of distances,
                                                            # then the table should be given here.
hrrc = hrf.findHierarchy(inputSet, inputFunction)           # a hierarchy for the set of points
hrrcIndices = hrf.findHrrcIndices(inputSet, hrrc[-1])       # hrrc[-1] has all the points according their entrance to the
                                                            # hierarchy. hrrcIndices has the indices of the points according
                                                            # the order in the original set



# # printing a hierarchy for inputSet according the distances that are in inputFunction
# for i in range(len(hrrc)):
#     print(hrrc[i])
# print(hrrc[-1])



delta = inputFunction[0][1]         # delta = the minimal distance between two of the points (starts from [0][1] because [0][0] always equals 0 --
                                    # it's on the diagonal of the distances' matrix
diameter = inputFunction[0][1]      # diameter = the diameter of the set
for i in range(len(inputFunction)):
    for j in range(len(inputFunction)):
        if(diameter < inputFunction[i][j]):
            diameter = inputFunction[i][j]
        if (i !=j and delta > inputFunction[i][j]):
            delta = inputFunction[i][j]
diameter = float(diameter)
delta = float(delta) / diameter

# d is the target dimension
# d is part of the input from the user
d = 1

lpsolver = lps.LPSolving(hrrc, hrrcIndices, d, delta, diameter, inputFunction)
lpSolution = lpsolver.solve()
