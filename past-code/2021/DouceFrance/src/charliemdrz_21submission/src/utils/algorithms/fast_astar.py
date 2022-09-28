import numba
import numpy as np
from numba import njit, jit
from numpy.random import choice

from utils.misc_objects_functions import _in_limits

maxint = (1 << 31) + .1


def a_star(root_point, ending_point, dimensions, cost_function):
    """
    Parameters
    ----------p
    root_point path origin
    ending_point path destination
    cost_function (RoadNetwork, Point, Point) -> int

    Returns
    -------
    best first path from root_point to ending_point if any exists
    """
    distance_map, neighbours, predecessor_map, heuristic_map = astar_env = _init(root_point, dimensions)

    clst_neighbor = root_point
    n_steps = 0
    max_step = max(1000, 10 * _heuristic(root_point, ending_point))
    while neighbours and (min(distance_map[n] for n in neighbours) < maxint) and (clst_neighbor != ending_point):
        n_steps += 1
        clst_neighbor = _closest_neighbor(astar_env, ending_point)
        neighbours.remove(clst_neighbor)
        _update_distances(astar_env + (cost_function,), dimensions, clst_neighbor)

        if n_steps >= max_step:
            break

    if clst_neighbor != ending_point:
        return []
    else:
        path = _path_to_dest(predecessor_map, root_point, ending_point, True)
        return path


@njit
def _init(point, dims):
    x, z = point
    _distance_map = np.full(dims, maxint)
    _distance_map[x, z] = 0
    _neighbours = {point}
    _predecessor_map = np.full((*dims, 2), max(dims))
    _heuristic_map = np.full(dims, maxint)
    return _distance_map, _neighbours, _predecessor_map, _heuristic_map


@njit(cache=True)
def _closest_neighbor(env, destination):

    distance_map, neighbours = env[:2]
    heuristic_map = env[3]
    closest_neighbors = [(0, 0)]
    min_heuristic = maxint
    for neighbour in neighbours:
        x, z = neighbour
        if heuristic_map[neighbour] == maxint:
            heuristic_map[neighbour] = _heuristic(neighbour, destination)
        current_heuristic = distance_map[x, z] + heuristic_map[neighbour]
        if current_heuristic < min_heuristic:
            closest_neighbors = [neighbour]
            min_heuristic = current_heuristic
        elif current_heuristic == min_heuristic:
            closest_neighbors.append(neighbour)
    return closest_neighbors[np.random.randint(0, len(closest_neighbors))]


@njit(cache=True)
def _heuristic(point, destination):
    x0, z0 = point
    xf, zf = destination
    return 1.1 * np.sqrt((xf - x0) ** 2 + (zf - z0) ** 2)


@jit(forceobj=True)
def _update_distance(env, updated_point, neighbor):
    distance_map, neighbors, predecessor_map, h_map, cost = env
    edge_cost = cost(updated_point, neighbor)
    if edge_cost == maxint:
        return

    new_distance = distance_map[updated_point] + edge_cost
    previous_distance = distance_map[neighbor]
    if previous_distance >= maxint:
        neighbors.add(neighbor)
    if previous_distance > new_distance:
        distance_map[neighbor] = new_distance
        predecessor_map[neighbor] = updated_point


@jit(forceobj=True, parallel=True)
def _update_distances(env, dims, point):
    x, z = point  # type: int, int
    for xz in _exploration_neighbourhood(x, z, *dims):
        _update_distance(env, point, xz)


@njit(cache=True)
def _path_to_dest(predecessor_map, origin, destination, fill_missing_points):
    current_point = destination
    path = [destination]
    while current_point != origin:
        current_point = (predecessor_map[current_point][0], predecessor_map[current_point][1])
        dist = abs_distance(path[-1], current_point)
        if fill_missing_points and dist > 1:
            # because of the large steps in exploration_neighbourhood, the path is sometimes "incomplete"
            # here we add intermediate blocks by exploring convex points between the last element of path and
            # the current one
            for i in range(1, dist):
                # i = 0 and i = dist correspond to path[-1] and current_point
                x = int(round(((dist - i) * path[-1][0] + i * current_point[0]) / dist))
                z = int(round(((dist - i) * path[-1][1] + i * current_point[1]) / dist))
                path.append((x, z))
        path.append(current_point)
    return nb_reversed(path)


@njit(cache=True)
def nb_reversed(arr: list):
    length = len(arr)
    target = []
    for i in range(length):
        target.append(arr[length-1 - i])
    return target


@njit(cache=True)
def _exploration_neighbourhood(x, z, width, length):
    neighbourhood = set()
    for dx, dz in [(0, 1), (-1, 2), (0, 2), (1, 2), (-1, 3), (0, 3), (1, 3)]:
        for _ in numba.prange(4):
            dx, dz = dz, -dx
            x0, z0 = x+dx, z+dz
            if _in_limits((x0, 0, z0), width, length):
                neighbourhood.add((x0, z0))
    return neighbourhood


@njit(cache=True)
def abs_distance(xz0, xz1):
    dx = abs(xz0[0] - xz1[0])
    dz = abs(xz0[1] - xz1[1])
    if dx > dz:
        return dx
    return dz
