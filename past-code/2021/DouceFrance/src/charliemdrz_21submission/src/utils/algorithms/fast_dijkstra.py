from numba import njit
from math import sqrt
from typing import Tuple, List
import numpy as np


@njit
def is_init_neigh(distance_map: np.ndarray, _x: int, _z: int):
    # Context: find border water points in a water surface.
    # Surrounded water points are useless in exploration
    W, L = distance_map.shape
    if distance_map[_x, _z] != 0:
        return False
    else:
        for dx, dz in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            x0, z0 = _x + dx, _z + dz
            if (0 <= x0 < W) and (0 <= z0 < L) and distance_map[x0, z0] != 0:
                return True
        return False


@njit(cache=True)
def cost(height_map: np.ndarray, src_point: Tuple[int, int], dst_point: Tuple[int, int]):
    x0, z0 = src_point
    x1, z1 = dst_point
    y0 = height_map[src_point]
    y1 = height_map[dst_point]
    return sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2 + (z0 - z1) ** 2)


@njit(cache=True)
def update_distance(distance_map: np.ndarray, height_map: np.ndarray, neighbours: List, origin: Tuple[int, int], destination: Tuple[int, int], max_distance):
    new_distance = distance_map[origin[0], origin[1]] + cost(height_map, origin, destination)
    previous_distance = distance_map[destination[0], destination[1]]
    if previous_distance >= max_distance > new_distance:
        neighbours.append(destination)
    distance_map[destination[0], destination[1]] = min(previous_distance, new_distance)


@njit(cache=True)
def update_distances(distance_map: np.ndarray, height_map: np.ndarray, neighbours: List, neighbour: Tuple[int, int], max_distance):
    W, L = distance_map.shape
    x0, z0 = neighbour
    for xn in range(x0 - 1, x0 + 2):
        for zn in range(z0 - 1, z0 + 2):
            if (xn != x0 or zn != z0) and 0 <= xn < W and 0 <= zn < L and distance_map[xn, zn] > 0:
                update_distance(distance_map, height_map, neighbours, neighbour, (xn, zn), max_distance)


@njit
def fast_dijkstra(distance_map: np.ndarray, height_map: np.ndarray):
    max_distance = distance_map.max()
    W, L = distance_map.shape
    neighbours = []
    for x1 in range(W):
        for z1 in range(L):
            if is_init_neigh(distance_map, x1, z1):
                neighbours.append((x1, z1))

    while len(neighbours) > 0:
        # true Dijkstra would require to explore the nearest neighbour. For faster computing, we assume that the oldest
        # added neighbour is not so far from being the closest unexplored
        clst_neighbor = neighbours[0]
        update_distances(distance_map, height_map, neighbours, clst_neighbor, max_distance)
        del neighbours[0]

    return distance_map
