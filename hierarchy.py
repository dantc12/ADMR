import logging
from copy import copy
from typing import List

import numpy as np

import utils

class Hierarchy:
    S: List  # 1-dimensional list
    scaled_distances: np.ndarray  # 2-dimensional list of distances
    hierarchy: List[List[int]]  # list of lists, the hierarchy
    c: float  # covering property

    def __init__(self, S: List, distances: np.ndarray, c: float):
        if len(distances.shape) != 2:
            raise Exception("Need a 2D list of distances.")
        self.S = S
        self.scaled_distances = utils.arr_scaler(distances)
        self.c = c
        self._build_hierarchy()

    def _build_hierarchy(self):
        for i in range(len(self.S)):
            try:
                self._build_hierarchy_starting_at(i)
                break
            except Exception:
                logging.info('Failed {}\'th try at building hierarchy, got {}'.format(str(i + 1), str(self)))
                self.hierarchy = []
        if len(self) == 0:  # Couldn't build any hierarchies
            logging.info("Failed to create a hierarchy.")
        else:
            logging.info("Created hierarchy successfully: {}".format(str(self)))

    def _build_hierarchy_starting_at(self, point_i: int):
        self.hierarchy = []
        p_index_options = [i for i in range(len(self.S))]

        self.hierarchy.append([point_i])  # Starts with the i'th point
        _ = p_index_options.pop(p_index_options.index(point_i))

        i = 1
        while len(p_index_options) > 0:
            self.hierarchy.append(copy(self.hierarchy[i-1]))
            # Fill in points to add to the layer
            p_index_options_copy = copy(p_index_options)
            for p_index in p_index_options_copy:
                #  verifying the c-covering property and the packing property
                if self._get_min_distance_from(p_index, self.hierarchy[i - 1]) <= self.c * 2 ** -(i-1)\
                        and self._get_min_distance_from(p_index, self.hierarchy[i]) > 2 ** -i:
                    self.hierarchy[i].append(p_index)
                    _ = p_index_options.pop(p_index_options.index(p_index))
            if len(self.hierarchy[i]) == len(self.hierarchy[i-1]):  # Didn't find anything to add to hierarchy
                raise Exception("Failed to create a hierarchy, got this far: {}".format(str(self.hierarchy)))
            i += 1

    def __str__(self):
        return str(self.hierarchy)
        # return str([[self.S[p_i] for p_i in lvl] for lvl in self.hierarchy])

    def __len__(self):
        return len(self.hierarchy)

    def get_points_hier(self) -> List:
        return [[self.S[p_i] for p_i in lvl] for lvl in self.hierarchy]

    def _get_min_distance_from(self, p_index, other_points_index: List) -> float:
        t = np.min([self.scaled_distances[p_index, j] for j in other_points_index])
        return t
