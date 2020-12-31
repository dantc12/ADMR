import numpy as np

from Hierarchy import Hierarchy
from utils import calc_euclidean_distances, arr_scaler

S = [(0, 0), (1, 0), (2, 0), (3, 0)]
distances = calc_euclidean_distances(np.array(S))
print(str(arr_scaler(distances)))
c = 1

h = Hierarchy(S, distances, c)

print(str(h))
