import numpy as np


def arr_scaler(arr: np.ndarray) -> np.ndarray:
    return np.array([v/np.max(arr) for v in [row for row in arr]])


def calc_euclidean_distances(arr: np.ndarray) -> np.ndarray:
    """
    :param arr: an array of points in a euclidean space.
    :return: the distances between all points, by the euclidean distance. will be of size n**2 if n
            is the length of amount of points
    """
    n = len(arr)
    res = np.ndarray((n, n))
    for i in range(n):
        for j in range(n):
            res[i, j] = np.linalg.norm(arr[i] - arr[j])
    return res


def get_min_non_zero(x: np.ndarray) -> float:
    return np.min(x[x.nonzero()])


def get_min_interpoint_dist(distances: np.ndarray) -> float:
    return get_min_non_zero(distances) / np.max(distances)
