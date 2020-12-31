from copy import copy
from typing import List, Any

import numpy as np

from utils import arr_scaler


class Hierarchy:
    S: List  # 1-dimensional list
    distances: np.ndarray  # 2-dimensional list of distances
    hierarchy: List[Any]  # list of lists, the hierarchy
    c: float  # covering property

    def __init__(self, S: List, distances: np.ndarray, c: float):
        # if len(S.shape) != 1:
        #     raise Exception("Need a 1D list of points for S.")
        if len(distances.shape) != 2:
            raise Exception("Need a 2D list of distances.")
        self.S = S
        self.distances = arr_scaler(distances)
        self.c = c
        self._build_hierarchy()

    def _build_hierarchy(self):
        for i in range(len(self.S)):
            try:
                self._build_hierarchy_starting_at(i)
                break
            except Exception:
                self.hierarchy = []
        if len(self.hierarchy) == 0:  # Couldn't build any hierarchies
            raise Exception("Failed to create a hierarchy, got only {}".format(str(self.hierarchy)))

    def _build_hierarchy_starting_at(self, point_i: int):
        self.hierarchy = []
        p_index_options = [i for i in range(len(self.S))]

        self.hierarchy.append([point_i])  # Starts with the i'th point
        _ = p_index_options.pop(p_index_options.index(point_i))

        i = 1
        while len(p_index_options) > 0:
            self.hierarchy.append([])
            # Find first point in layer
            p_index_options_copy = copy(p_index_options)
            for p_index in p_index_options_copy:
                #  checking for the c-covering property: in prev layer it should have a "close" point
                if self._get_min_distance_from(p_index, self.hierarchy[i - 1]) < self.c * 2 ** -(i-1):
                    self.hierarchy[i].append(p_index)
                    _ = p_index_options.pop(p_index_options.index(p_index))
            if len(self.hierarchy[i]) == 0:  # Didn't find anything to add to hierarchy
                raise Exception("Failed to create a hierarchy, got only {}".format(str(self.hierarchy)))

            # Fill in more points in layer
            p_index_options_copy = copy(p_index_options)
            for p_index in p_index_options_copy:
                #  verifying the c-covering property and the packing property
                if self._get_min_distance_from(p_index, self.hierarchy[i - 1]) < self.c * 2 ** -(i-1)\
                        and self._get_min_distance_from(p_index, self.hierarchy[i]) >= 2 ** -i:
                    self.hierarchy[i].append(p_index)
                    _ = p_index_options.pop(p_index_options.index(p_index))
            i += 1

    def __str__(self):
        res = [self.hierarchy[0]]
        if len(self.hierarchy) > 1:
            for i in range(1, len(self.hierarchy)):
                res.append(res[i-1] + self.hierarchy[i])
        return str(res)

    def _get_min_distance_from(self, p_index, other_points_index: List) -> float:
        t = np.min([self.distances[p_index, j] for j in other_points_index])
        return t

