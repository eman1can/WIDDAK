from numba.typed import List as nbList
from numpy.random import randint

from utils.algorithms.fast_astar import abs_distance, numba, _in_limits, maxint, \
    _path_to_dest, _heuristic as euclidean, njit, np, jit
from utils.misc_objects_functions import index_argmin

GAMMA = 4


def hierarchical_astar(source, target, dimensions, cost_function):
    """
    Custom A* algorithm - computes path with decreasing steps
    :param source: source point (x, z)
    :param target: target point (x, z)
    :param dimensions: (width, length)
    :param cost_function: cost function ((xo, zo), (xd, zd)) -> value
    """

    # Compute initial step
    step = 1
    d = abs_distance(source, target)
    while step * GAMMA < d:
        step *= GAMMA

    def get_cumsum():
        """
        Computes target heuristic for each point in the rough path
        :return:
        """
        l = [0]
        for i in range(len(rough_path) - 1, 0, -1):
            l.append(l[-1] + cost_function(rough_path[i], rough_path[i - 1]))
        res = nbList()
        [res.append(_) for _ in reversed(l)]
        return res

    rough_path = [source, target]

    while True:
        distance_map, neighbours, predecessor_map, heuristic_map = astar_env = _init(source, dimensions)
        cumsum = get_cumsum()
        clst_neighbour = source
        heuristic_idx = {}

        while neighbours and (min(distance_map[n] for n in neighbours) < maxint) and abs_distance(clst_neighbour, target) >= step:

            # pick new exploration point -> point closer to target
            clst_neighbour = _closest_neighbor(astar_env, rough_path, cumsum)
            neighbours.remove(clst_neighbour)
            neighbours = list(filter(lambda n: heuristic_idx[n] >= heuristic_idx[clst_neighbour], neighbours))
            astar_env = distance_map, neighbours, predecessor_map, heuristic_map
            known_neighbours = len(neighbours)

            # explore neighbours to this point
            _update_distances(astar_env + (cost_function,), dimensions + (step,), clst_neighbour)

            # handle new neighbours: store their heuristic index
            for new_neighbour in neighbours[known_neighbours:]:
                heuristic_idx[new_neighbour] = _heuristic_index(new_neighbour, rough_path)

        if step == 1:
            if abs_distance(clst_neighbour, target) >= step:
                return []
            else:
                return _path_to_dest(predecessor_map, source, target, True)
        else:
            rough_path = _path_to_dest(predecessor_map, source, clst_neighbour, False) + [target]
            step //= GAMMA


# @njit
def _heuristic_index(point, path):
    distance_to_path = nbList()
    [distance_to_path.append(euclidean(point, point2)) for point2 in path]
    return index_argmin(distance_to_path)


# @njit()
def _heuristic(point, path, path_heuristic):
    i = _heuristic_index(point, path)
    if i == len(path) - 1:
        return euclidean(point, path[-1])
    target = path[i + 1]
    return euclidean(point, target) + path_heuristic[i + 1]


# @njit()
def _closest_neighbor(env, path, path_heuristic):
    distance_map, neighbors = env[:2]
    heuristic_map = env[3]
    closest_neighbors = nbList()
    # closest_neighbors.append((1 << 16, 1 << 16))
    min_heuristic = maxint + 1
    for neighbor in neighbors:
        x, z = neighbor
        if heuristic_map[neighbor] >= maxint:
            heuristic_map[neighbor] = _heuristic(neighbor, path, path_heuristic)
        current_heuristic = distance_map[x, z] + heuristic_map[neighbor]
        if not closest_neighbors or current_heuristic < min_heuristic:
            closest_neighbors = nbList()
            closest_neighbors.append(neighbor)
            min_heuristic = current_heuristic
        elif current_heuristic == min_heuristic:
            closest_neighbors.append(neighbor)
    return closest_neighbors[randint(len(closest_neighbors))]


# @jit(forceobj=True, parallel=True)
def _update_distances(env, dims, point):
    """
    :param env: (...)
    :param dims: (width, length, step)
    :param point: (x, z)
    """
    x, z = point  # type: int, int
    for xz in _exploration_neighbourhood(x, z, *dims):
        _update_distance(env, point, xz)


# @njit(cache=True)
def _exploration_neighbourhood(x, z, width, length, step):
    neighbourhood = set()
    for dx, dz in [(0, step), (step, step), (-step, 2 * step), (0, 2 * step), (step, 2 * step)]:
        for _ in numba.prange(4):
            dx, dz = dz, -dx
            x0, z0 = x + dx, z + dz
            if _in_limits((x0, 0, z0), width, length):
                neighbourhood.add((x0, z0))
    return neighbourhood


@njit
def _init(point, dims):
    x, z = point
    _distance_map = np.full(dims, maxint)
    _distance_map[x, z] = 0
    _neighbours = [point]
    _predecessor_map = np.full((*dims, 2), max(dims))
    _heuristic_map = np.full(dims, maxint)
    return _distance_map, _neighbours, _predecessor_map, _heuristic_map


@jit(forceobj=True)
def _update_distance(env, updated_point, neighbor):
    distance_map, neighbors, predecessor_map, h_map, cost = env
    edge_cost = cost(updated_point, neighbor)
    if edge_cost == maxint:
        return

    new_distance = distance_map[updated_point] + edge_cost
    previous_distance = distance_map[neighbor]
    if previous_distance >= maxint:
        neighbors.append(neighbor)
    if previous_distance > new_distance:
        distance_map[neighbor] = new_distance
        predecessor_map[neighbor] = updated_point

