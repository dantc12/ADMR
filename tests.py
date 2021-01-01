import logging

import numpy as np

from Hierarchy import Hierarchy
from utils import calc_euclidean_distances, arr_scaler

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
logging.info('Entered debug mode.')

S = [(1, 1), (1, -1), (2, 1), (3, 0)]
distances = calc_euclidean_distances(np.array(S))
logging.info('Points:\n{}'.format(str(S)))
logging.info('Scaled distances:\n{}'.format(str(arr_scaler(distances))))
# print(str(arr_scaler(distances)))
c = 1

h = Hierarchy(S, distances, c)

# print(str(h))
