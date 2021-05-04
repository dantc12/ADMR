from typing import List, Tuple

import numpy as np
from pulp import LpProblem, lpSum, LpVariable, LpMinimize

from hierarchy import Hierarchy

ALPHAS = [7, 24, 75, 588, 612]
# Max values in calculator:
# 7^118
# 24^72
# 75^53
# 588^36
# 612^35


class LinearProgram:
    h: Hierarchy
    d: int
    delta: float
    scaled_distances: np.ndarray

    n: int
    t: int

    model: LpProblem
    c: List[LpVariable]
    z: List[List[LpVariable]]

    def __init__(self,
                 h: Hierarchy,
                 d: int,
                 delta: float):
        self.h = h
        self.d = d
        self.delta = delta
        self.scaled_distances = h.scaled_distances

        self._initialize_vars()

    def _initialize_vars(self):
        self.n = len(self.h.S)
        self.t = len(self.h.hierarchy) - 1

        # Create the model
        self.model = LpProblem(name="linear program", sense=LpMinimize)

        # Initialize the decision variables
        self.c = []
        for i in range(self.n):
            self.c.append(LpVariable(name=f"c_{i}", lowBound=0))

        self.z = []
        for i in range(self.t + 1):
            self.z.append([])
            for j in range(len(self.h.hierarchy[i])):
                self.z[i].append(LpVariable(name=f"z_{i}{j}", lowBound=0, upBound=1))

    def solve(self):
        d_tag = 4 * self.d - 1

        # Add the constraints to the model
        # constraint (10)
        for i in range(self.t):
            for j in range(len(self.z[i])):
                self.model += (self.z[i][j] <= self.z[i+1][j], f"constraint (10)_i{i}_j{j}")

        # constraint (11)
        for alpha in ALPHAS:
            for j in range(self.n):
                for i in range(self.t + 1):
                    self.model += (lpSum([self.z[k][l] for (k, l) in self._N_i_j(alpha, i, j)]) <= (2 * alpha) ** d_tag,
                                   f"constraint (11)_alpha{alpha}_j{j}_i{i}")

        # constraint (12)
        for j in range(len(self.z[self.t])):
            for i in range(self.t + 1):
                self.model += (lpSum([self.z[k][l] for (k, l) in self._N_i_j(7, i, j)]) >= self.z[self.t][j],
                               f"constraint (12)_j{j}_i{i}")

        # constraint (13)
        for j in range(self.n):
            for k in range(self.t + 1):
                for i in range(k):
                    self.model += (lpSum([self.z[l][r] for (l, r) in self._N_i_j(24, i, j)]) >= (1 / (2 * 24) ** d_tag) * lpSum([self.z[l][r] for (l, r) in self._N_i_j(24, k, j)]),
                                   f"constraint (13)_j{j}_k{k}_i{i}")

        # constraint (15)
        for j in range(self.n):
            # LpVariable doesn't seem to support `/` operator, so I multiplied ineq by delta
            self.model += (self.delta * self.z[self.t][j] + self.c[j] >= self.delta, f"constraint (15)_j{j}")

        # constraint (16)
        for j in range(self.n):
            for i in range(self.t + 1):
                self.model += ((2 ** -i) * self.z[self.t][j] + self.c[j] + self.delta * lpSum([self.z[k][l] for (k, l) in self._N_i_j(12, i, j)]) >= self.delta,
                               f"constraint (16)_j{j}_i{i}")

        # objective
        self.model += lpSum(self.c)

        print(self.model)
        # Solve the problem
        status = self.model.solve()

    def _N_i_j(self, alpha: int, i: int, j: int) -> List[Tuple[int, int]]:
        res_z = []

        if j in self.h.hierarchy[i]:
            center = j
        else:
            center = self.h.hierarchy[i][0]
            for r in self.h.hierarchy[i][1:]:
                if self.scaled_distances[j, r] < self.scaled_distances[j, center]:
                    center = r

        for k in range(len(self.z[i])):
            if self.scaled_distances[center, k] <= alpha * (2 ** -i):
                res_z.append((i, k))

        return res_z



