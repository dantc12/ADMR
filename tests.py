import logging

import numpy as np

from hierarchy import Hierarchy
from utils import calc_euclidean_distances, arr_scaler, get_min_non_zero

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
logging.info('Entered debug mode.')

S = [(1, 1), (1, -1), (2, 1), (3, 0), (4, 1), (0, -2), (-1, -1)]
distances = arr_scaler(calc_euclidean_distances(np.array(S)))
delta = get_min_non_zero(distances)
t = int(np.ceil(np.log2(1 / delta)))

logging.info('Points:\n{}'.format(str(S)))
logging.info('Scaled distances:\n{}'.format(str(distances)))
logging.info('Minimal distance (delta): {}'.format(str(delta)))
logging.info('t: {}'.format(str(t)))
# print(str(arr_scaler(distances)))

c = 1
h = Hierarchy(S, distances, c)

d = 1
