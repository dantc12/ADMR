import logging
from typing import List
import numpy as np

import utils
from hierarchy import Hierarchy
from linear_program import LinearProgram


def run(S: List, save_file_name: str, c: float = 1, d: int = 1):
    logging.basicConfig(filename='run_logs/' + save_file_name + '.log',
                        format='%(asctime)s - %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    logging.info('Entered debug mode.')
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
    for var in [var for var in lp.model.variables() if var.name.startswith('z') and var.value() == 1]:
        split = var.name.split('_')
        i = int(split[1][1:])
        j = int(split[2][1:])
        while len(w_hierarchy) <= i:
            w_hierarchy.append([])
        w_hierarchy[i].append(j)
    w_hierarchy = [sorted(w) for w in w_hierarchy]

    W = [S[w] for w in w_hierarchy[-1]]

    logging.info(f"W hierarchy: {w_hierarchy}")
    logging.info(f"Recall S: {S}")
    S_np = np.array(S)
    logging.info(f"W: {W}")
    W_np = np.array(W)
    if W == S:
        print("(W == S)")

    return W
