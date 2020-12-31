from copy import deepcopy
from typing import List, Any

import numpy as np

from utils import arr_scaler


class Hierarchy:
    S: np.ndarray  # 1-dimensional list
    distances: np.ndarray  # 2-dimensional list of distances
    hierarchy: List[Any]  # list of lists, the hierarchy
    c: float  # covering property

    def __init__(self, S: np.ndarray, distances: np.ndarray, c: float):
        if not len(S.shape) != 1:
            raise Exception("Need a 1D list of points for S.")
        if not len(distances.shape) != 2:
            raise Exception("Need a 2D list of distances.")
        self.S = S
        self.distances = arr_scaler(distances)
        self.c = c
        self._build_hierarchy()

    def _build_hierarchy(self):
        self.hierarchy = []
        n = len(self.S)
        p_index_options = [i for i in range(n)]

        # start_index = np.random.choice(p_index_options)
        # self.hierarchy.append([self.S[start_index]])
        i = 0
        while len(p_index_options) > 0:
            self.hierarchy.append([])
            for p_index in p_index_options:
                if i > 0:
                    #  checking for the c-covering property: in prev layer it should have a "close" point
                    if np.min(self._get_distances_from_other_points(p_index, self.hierarchy[i-1])) >= self.c * 2 ** -i:
                        continue
                # TODO Should be a random choice
                if len(self.hierarchy[i]) == 0 or \
                        np.min(self._get_distances_from_other_points(p_index, self.hierarchy[i])) >= 2 ** -i:
                    self.hierarchy[i].append(p_index)
                    _ = p_index_options.pop(p_index_options.index(p_index))
            if len(self.hierarchy[i]) == 0:  # Didn't find anything to add to hierarchy
                raise Exception("Failed to create a hierarchy.")
            i += 1

    def __str__(self):
        return str(self.hierarchy)

    def _get_distances_from_other_points(self, p_index, other_points_index: List) -> List:
        return [self.distances[p_index, j] for j in other_points_index]

