import logging

import numpy as np

from hierarchy import Hierarchy
import utils

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
logging.info('Entered debug mode.')

S = [(1, 1), (1, -1), (2, 1), (3, 0), (4, 1), (0, -2), (-1, -1)]
distances = utils.calc_euclidean_distances(np.array(S))
delta = utils.get_min_interpoint_dist(distances)
t = int(np.ceil(np.log2(1 / delta)))

logging.info('Points:\n{}'.format(str(S)))
logging.info('Distances:\n{}'.format(str(distances)))
logging.info('Minimal distance (delta): {}'.format(str(delta)))
logging.info('t: {}'.format(str(t)))
# print(str(arr_scaler(distances)))

c = 1
h = Hierarchy(S, distances, c)

d = 1
