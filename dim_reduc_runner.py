import logging
from typing import List
import numpy as np
from pulp import LpStatus

import utils
from hierarchy import Hierarchy
from linear_program import LinearProgram

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
logging.info('Entered debug mode.')


def run(S: List, save_file_name: str, c: float = 1, d: int = 1):
    distances = utils.calc_euclidean_distances(np.array(S))
    delta = utils.get_delta(distances)
    t = int(np.ceil(np.log2(1 / delta)))

    logging.info('Points:\n{}'.format(str(S)))
    # logging.info('Distances:\n{}'.format(str(distances)))
    # logging.info('Minimal distance (delta): {}'.format(str(delta)))
    logging.info('t: {}'.format(str(t)))
    # print(str(arr_scaler(distances)))

    logging.info('Building hierarchy.')
    h = Hierarchy(S, distances, c, t)
    logging.info('Done.')

    logging.info('Building LP.')
    lp = LinearProgram(h, d, delta, save_file_name)
    logging.info('Done.')

    logging.info('Solving.')
    lp.solve()
    logging.info('Done.')

    w_hierarchy = []
    for var in [var for var in lp.model.variables() if var.name.startswith('z')]:
        split = var.name.split('_')
        i = int(split[1][1:])
        j = int(split[2][1:])
        if var.value() == 1:
            while len(w_hierarchy) <= i:
                w_hierarchy.append([])
            w_hierarchy[i].append(j)

    w_hierarchy = [sorted(w) for w in w_hierarchy]

    W = [S[w] for w in w_hierarchy[-1]]

    print(f"W hierarchy: {w_hierarchy}")
    print(f"Recall S: {S}")
    print(f"W: {W}")
    if W == S:
        print("(W == S)")

    return W
