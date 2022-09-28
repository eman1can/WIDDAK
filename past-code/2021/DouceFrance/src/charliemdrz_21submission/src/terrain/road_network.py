# coding=utf-8
from random import choice
from typing import Callable
from time import time

from numpy import empty

import terrain
from generation.generators import *
from generation.road_generator import RoadGenerator
from parameters import *
from utils import Point, euclidean

MAX_FLOAT = 100000.0
MAX_DISTANCE_CYCLE = 30
MIN_DISTANCE_CYCLE = 15
DIST_BETWEEN_NODES = 12
MIN_CYCLE_GAIN = 2
CYCLE_ALTERNATIVES = 4
maxint = 1 << 32


class RoadNetwork:
    """
    Road network, computes and stores roads to reach every location. If used correctly, the road network should be
    continuous, ie you can walk from every road point to every other road points by only walking on paths.
    The road network is built simultaneously with the RoadGenerator, which concretely builds the paths
    """
    def __init__(self, width, length, mc_map=None):
        # type: (int, int, terrain.TerrainMaps) -> RoadNetwork
        self.width = width
        self.length = length
        self.network = zeros((width, length), dtype=int)
        # Representing the distance from the network + the path to the network
        self.cost_map = full((width, length), maxint)
        self.distance_map = full((width, length), maxint)
        # paths from existing road points to every reachable destination
        self.path_map = empty((width, length), dtype=object)
        self.lambda_max = MAX_LAMBDA

        # points passed through create_road or connect_to_network
        self.nodes: Set[Point] = set()
        self.road_blocks: Set[Point] = set()
        self.special_road_blocks: Set[Point] = set()
        self.__generator = RoadGenerator(self, mc_map.box, mc_map) if mc_map else None
        self.__all_maps = mc_map

    # region GETTER AND SETTER

    def __is_point_obstacle(self, point):
        if self.__all_maps is not None:
            return not self.__all_maps.obstacle_map.is_accessible(point)
        else:
            return False

    def get_road_width(self, x: Point or int, z: int = None) -> int:
        """
        Get road width at specific point
        """
        if z is None:
            return self.get_road_width(x.x, x.z)
        else:
            return self.network[x, z]

    def __get_closest_node(self, point):

        closest_node = None
        min_distance = MAX_FLOAT
        if not self.nodes:
            closest_node = choice(list(self.road_blocks))
        else:
            for node in self.nodes:
                if euclidean(node, point) < min_distance:
                    closest_node = node
                    min_distance = euclidean(node, point)

        if not self.road_blocks.difference(self.nodes):
            return closest_node

        # try to promote an extremity to node
        alt_edge = [_ for _ in self.road_blocks.difference(self.nodes)]
        alt_dist = [euclidean(_, point) for _ in alt_edge]
        i = int(argmin(alt_dist))
        edge, dist = alt_edge[i], alt_dist[i]
        if dist < min_distance:
            if euclidean(edge, closest_node) >= DIST_BETWEEN_NODES:
                self.nodes.add(edge)
            closest_node = edge
        return closest_node

    def get_distance(self, x: Point or int, z: int = None) -> float:
        if z is None:
            return maxint if self.__is_point_obstacle(x) else self.get_distance(x.x, x.z)
        else:
            if self.distance_map[x][z] == maxint:
                return maxint
            return max(0, self.distance_map[x][z] - self.get_road_width(self.get_closest_road_point(Point(x, z))))

    def __set_road_block(self, xp, z=None):
        # type: (Point or int, None or int) -> None
        if z is None:
            # steep roads are not marked as road points
            maps = self.__all_maps
            if maps and (maps.height_map.steepness(xp.x, xp.z) >= 0.35 or maps.fluid_map.is_water(xp)
                         or not maps.obstacle_map.is_accessible(xp)):
                self.special_road_blocks.add(xp)
            else:
                self.road_blocks.add(xp)
            x, z = xp.x, xp.z
            if self.network[x, z] == 0:
                self.network[x, z] = MIN_ROAD_WIDTH
            elif self.network[x, z] < MAX_ROAD_WIDTH:
                self.network[x, z] += 1
        else:
            self.__set_road_block(Point(xp, z))

    def is_road(self, x, z=None):
        # type: (Point or int, None or int) -> bool
        if z is None:
            return self.is_road(x.x, x.z)
        else:
            return self.network[x][z] > 0

    def get_closest_road_point(self, point):
        # type: (Point) -> Point
        if self.is_road(point):
            return point
        if self.is_accessible(point):
            return self.path_map[point.x][point.z][0]
        else:
            return self.__get_closest_node(point)

    def __invalidate(self, point):
        self.distance_map[point.x][point.z] = maxint
        self.path_map[point.x][point.z] = None

    def __set_road(self, path):
        # type: ([Point]) -> None
        force_update = False
        # if any(self.__is_point_obstacle(point) for point in path):
        #     force_update = True
        #     p = path[-1]
        #     refresh_perimeter = product(sym_range(p.x, len(path), self.width), sym_range(p.z, len(path), self.length))
        #     refresh_sources = []
        #     for x, z in refresh_perimeter:
        #         if self.is_road(x, z):
        #             refresh_sources.append(Point(x, z))
        #         else:
        #             self.distance_map[x, z] = maxint
        #             self.cost_map[x, z] = maxint
        #             self.path_map[x, z] = []
        #     self.__update_distance_map(refresh_sources)
        #     path = self.path_map[p.x, p.z]
        #     # path = self.a_star(path[0], path[-1])
        # else:
        if self.__generator:
            self.__generator.handle_new_road(path)
        for point in path:
            self.__set_road_block(point)
        self.__update_distance_map(path, force_update)

    def is_accessible(self, point: Point) -> bool:
        path = self.path_map[point.x][point.z]
        return type(path) == list and (len(path) > 0 or self.is_road(point))

    # endregion
    def calculate_road_width(self, x, z):
        """
        todo: algorithme simulationniste ? dépendance au centre ?
        """
        # return self.network[x, z]
        return 3

    # region PUBLIC INTERFACE

    def create_road(self, root_point=None, ending_point=None, path=None):
        # type: (Point, Point, List[Point]) -> List[Point]
        if path is None:
            assert root_point is not None and ending_point is not None
            print(f"[RoadNetwork] Compute road path from {str(root_point + self.__all_maps.area.origin)} towards {str(ending_point + self.__all_maps.area.origin)}", end="")
            _t0 = time()
            path = self.a_star(root_point, ending_point, RoadNetwork.road_build_cost)
            self.nodes.update({root_point, ending_point})
            print(f"in {(time() - _t0):0.2f}s")
        self.__set_road(path)
        return path

    def connect_to_network(self, point_to_connect: Point, margin: int = 0) -> List[Set[Point]]:
        """
        Create roads to connect a point to the network. Creates at least one road, and potential other roads (to create
        cycles)
        Parameters
        ----------
        point_to_connect new destination in the network
        margin how close to get to the new point when reaching it

        Returns
        -------
        Created road cycles (possibly empty)
        """

        # safe check: the point is already connected
        if self.is_road(point_to_connect):
            return []

        # either the path is precomputed or computed with a*
        path: List[Point]
        if self.is_accessible(point_to_connect):
            path = self.path_map[point_to_connect.x][point_to_connect.z]
            print(f"[RoadNetwork] Found existing road towards {str(point_to_connect)}")
        else:
            _t0 = time()
            path = self.a_star(self.__get_closest_node(point_to_connect), point_to_connect, RoadNetwork.road_build_cost)
            print(f"[RoadNetwork] Computed road path towards {str(point_to_connect)} in {(time()-_t0):0.2f}s")

        # if a* fails, return
        if not path:
            return []

        # else, register new road(s)
        if margin > 0:
            truncate_index = next(i for i, p in enumerate(path) if manhattan(p, point_to_connect) <= margin)
            path = path[:truncate_index]
            if not path: return []
            point_to_connect = path[-1]
        self.__set_road(path)
        self.nodes.add(point_to_connect)

        _t1, cycles = time(), []
        for node in sorted(self.nodes, key=lambda n: euclidean(n, point_to_connect))[1:min(CYCLE_ALTERNATIVES, len(self.nodes))]:
            old_path, new_path = self.cycle_creation_condition(node, point_to_connect)
            if new_path:
                new_path = self.create_road(path=new_path)
                cycles.append(set(old_path).union(set(new_path)))
                if len(cycles) == 2:
                    # allow max 2 new cycles
                    break
        print(f"[RoadNetwork] Computed {len(cycles)} new road cycles in {(time()-_t1):0.2f}s")

        if path and all(euclidean(path[0], node) > DIST_BETWEEN_NODES for node in self.nodes):
            self.nodes.add(path[0])

        return cycles

    # endregion

    def generate(self, level, districts):
        hm = level.height_map[:]  # type: terrain.HeightMap
        self.__generator.generate(level, hm[:], districts)

    def __update_distance_map(self, road, force_update=False):
        self.dijkstra(road, self.lambda_max, force_update)

    def road_build_cost(self, src_point, dest_point):
        value = scale = manhattan(src_point, dest_point)
        # if we don't have access to terrain info
        if self.__all_maps is None or self.is_road(dest_point):
            return value

        # if dest_point is an obstacle, return inf
        is_dest_obstacle = not self.__all_maps.obstacle_map.is_accessible(dest_point)
        is_dest_obstacle |= self.__all_maps.fluid_map.is_lava(dest_point, margin=MIN_DIST_TO_LAVA)
        if is_dest_obstacle:
            return maxint

        # specific cost to build on water
        if self.__all_maps.fluid_map.is_water(dest_point, margin=MIN_DIST_TO_RIVER):
            if not self.__all_maps.fluid_map.is_water(src_point):
                return scale * BRIDGE_COST
            return scale * BRIDGE_UNIT_COST

        # discount to get roads closer to water
        src_water = self.__all_maps.fluid_map.water_distance(src_point)
        dest_water = self.__all_maps.fluid_map.water_distance(dest_point)
        if 2.5 * MIN_DIST_TO_RIVER >= src_water > dest_water > MIN_DIST_TO_RIVER:
            value += (dest_water - src_water) * .7 * scale

        # additional cost for slopes
        elevation = abs(self.__all_maps.height_map.steepness(src_point, norm=False).dot(dest_point - src_point))
        value += scale * elevation ** 2

        return max(scale, value)

    def road_only_cost(self, src_point, dest_point):
        return manhattan(src_point, dest_point) if self.is_road(dest_point) else maxint

    # return the path from the point satisfying the ending_condition to the root_point, excluded
    def dijkstra(self, root_points, max_distance, force_update):
        # type: (List[Point], int, bool) -> None
        """
        Accelerated Dijkstra algorithm to compute distance & shortest paths from root points to all others.
        The cost function is the euclidean distance
        Parameters
        ----------
        root_points null distance points to start the exploration
        max_distance todo
        force_update todo

        Returns
        -------
        Nothing. Result is stored in self.distance_map and self.path_map
        """
        def init():
            _distance_map = full((self.width, self.length), maxint)  # on foot distance walking from road points
            _cost_map = full((self.width, self.length), maxint)  # cost distance building from road points
            for root_point in root_points:
                _distance_map[root_point.x, root_point.z] = 0
                _cost_map[root_point.x, root_point.z] = 0
            _neighbours = set(root_points)
            _predecessor_map = empty((self.width, self.length), dtype=object)
            return _cost_map, _distance_map, _neighbours, _predecessor_map

        def closest_neighbor():
            _closest_neighbors = []
            min_cost = maxint
            for neighbor in neighbors:
                _current_cost = cost_map[neighbor.x, neighbor.z]
                if _current_cost < min_cost:
                    _closest_neighbors = [neighbor]
                    min_cost = _current_cost
                elif _current_cost == min_cost:
                    _closest_neighbors += [neighbor]
            return choice(_closest_neighbors)
            # old_neighbours = neighbors if len(neighbors) < 16 else neighbors[:16]
            # distances = map(lambda n: distance_map[n.x, n.z], old_neighbours)
            # return old_neighbours[argmin(distances)]
            # return neighbors[0]

        def distance(orig_point, dest_point):
            if self.__all_maps is None:
                return euclidean(orig_point, dest_point)

            fluids = self.__all_maps.fluid_map
            if fluids.is_lava(dest_point):
                return maxint
            elif fluids.is_water(dest_point):
                return BRIDGE_UNIT_COST
            else:
                orig_height = self.__all_maps.height_map[orig_point]
                dest_height = self.__all_maps.height_map[dest_point]
                if abs(orig_height - dest_height) > 1:
                    return maxint
            return euclidean(orig_point, dest_point)

        def update_distance(updated_point, neighbor, _neighbors):
            edge_cost = self.road_build_cost(updated_point, neighbor)
            edge_dist = distance(updated_point, neighbor)
            if edge_cost == maxint or edge_dist == maxint:
                return

            new_cost = cost_map[updated_point.x][updated_point.z] + edge_cost
            new_dist = distance_map[updated_point.x][updated_point.z] + edge_dist
            previous_cost = cost_map[neighbor.x][neighbor.z]
            if previous_cost >= maxint and new_dist <= max_distance and not self.is_road(neighbor) \
                    and (new_cost < self.cost_map[neighbor.x][neighbor.z] or force_update):
                _neighbors.add(neighbor)
            if previous_cost > new_cost:
                cost_map[neighbor.x][neighbor.z] = new_cost
                distance_map[neighbor.x][neighbor.z] = new_dist
                predecessor_map[neighbor.x][neighbor.z] = updated_point

        def update_distances(updated_point):
            x, z = updated_point.x, updated_point.z
            path = path_to_dest(updated_point)
            is_straight_road = (len(path) < 3) or (path[-1].x == path[-3].x) or (path[-1].z == path[-3].z)
            if (x + 1 < self.width) and (is_straight_road or path[-2].z == z):
                update_distance(updated_point, Point(x + 1, z), neighbors)
            if (x - 1 >= 0) and (is_straight_road or path[-2].z == z):
                update_distance(updated_point, Point(x - 1, z), neighbors)
            if (z + 1 < self.length) and (is_straight_road or path[-2].x == x):
                update_distance(updated_point, Point(x, z + 1), neighbors)
            if (z - 1 >= 0) and (is_straight_road or path[-2].x == x):
                update_distance(updated_point, Point(x, z - 1), neighbors)

        def path_to_dest(dest_point):
            current_point = dest_point
            path = []
            while not self.is_road(current_point):
                path = [current_point] + path
                current_point = predecessor_map[current_point.x][current_point.z]
            return path

        def update_maps_info_at(point):
            x, z = point.x, point.z
            if self.cost_map[x, z] > cost_map[x, z]:
                self.cost_map[point.x][point.z] = cost_map[point.x][point.z]
                self.distance_map[point.x][point.z] = distance_map[point.x][point.z]
                self.path_map[point.x][point.z] = path_to_dest(point)

        cost_map, distance_map, neighbors, predecessor_map = init()
        while len(neighbors) > 0:
            clst_neighbor = closest_neighbor()
            neighbors.remove(clst_neighbor)
            update_maps_info_at(clst_neighbor)
            update_distances(clst_neighbor)

    def a_star(self, root_point, ending_point, cost_function, timer=False, recursive=True):
        # type: (Point, Point, Callable[[RoadNetwork, Point, Point], int]) -> List[Point]
        """
        Parameters
        ----------
        root_point path origin
        ending_point path destination
        cost_function (RoadNetwork, Point, Point) -> int

        Returns
        -------
        best first path from root_point to ending_point if any exists
        """
        from utils.algorithms import a_star
        if root_point == ending_point:
            return [root_point]
        t0 = time()
        try:
            from utils.algorithms.hierarchical_astar import hierarchical_astar
            f = hierarchical_astar if recursive else a_star
            tuple_path = f((root_point.x, root_point.z), (ending_point.x, ending_point.z), (self.width, self.length), lambda u, v: cost_function(self, Point(u[0], u[1]), Point(v[0], v[1])))
        except SystemError or KeyError or ValueError:
            return []
        if timer:
            t0 = time() - t0 + .001
            print(f"Fast a*'ed a {len(tuple_path)} blocks road in {int(t0) if t0 > 1 else t0} seconds, avg: {int(len(tuple_path)/t0)}mps")
        return [Point(u, v) for u, v in tuple_path]

    def cycle_creation_condition(self, node1: Point, node2: Point) -> (List[Point], List[Point]):
        """
        Evaluates whether it's useful to create a new road between two road points
        :param node1:
        :param node2:
        :return:
        """
        straight_dist = euclidean(node1, node2)
        if not (MIN_DISTANCE_CYCLE <= straight_dist <= MAX_DISTANCE_CYCLE):
            return [], []

        existing_path = self.a_star(node1, node2, RoadNetwork.road_only_cost, recursive=False)
        current_dist = len(existing_path)
        if current_dist / straight_dist < MIN_CYCLE_GAIN:
            return existing_path, []
        straight_path = self.a_star(node1, node2, RoadNetwork.road_build_cost, recursive=False)
        straight_dist = len(straight_path)
        if straight_dist and current_dist / straight_dist >= MIN_CYCLE_GAIN:
            return existing_path, straight_path
        return existing_path, []
