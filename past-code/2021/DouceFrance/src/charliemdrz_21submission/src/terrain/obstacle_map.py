
from utils import *


class ObstacleMap:

    def __init__(self, width, length, mc_map=None):
        # type: (int, int, TerrainMaps) -> ObstacleMap
        self.__width = width
        self.__length = length
        # self.map = full((self.__width, self.__length), True)
        self.map = zeros((self.__width, self.__length))
        self.__all_maps = mc_map
        self.__init_map_with_environment(mc_map.box)
        self.__hidden_obstacles = []

    def __init_map_with_environment(self, bounding_box):
        # TODO: For every water/tree bloc, set bloc to un-accessible - this method should not be in this class
        pass

    def add_obstacle(self, point, mask=None):
        # type: (Point, ndarray) -> None
        """
        Main function to add an obstacle
        Parameters
        ----------
        point lower bounds of the rectangular obstacle surface
        mask boolean array indicating obstacle points in the obstacle surface
        Returns None
        -------
        """
        if mask is None:
            mask = full((1, 1), True)
        self.__add_obstacle(point, mask, 1)

    def is_accessible(self, point):
        # type: (Point) -> bool
        return self.map[point.x, point.z] == 0

    def __set_obstacle(self, x, z, cost=1):
        # self.map[x, z] = False
        self.map[x, z] += cost

    def __add_obstacle(self, point, mask, cost):
        for dx, dz in product(range(mask.shape[0]), range(mask.shape[1])):
            p = point + Point(dx, dz)
            if self.__all_maps.in_limits(p, False) and mask[dx, dz]:
                self.__set_obstacle(p.x, p.z, cost)

    def hide_obstacle(self, point, mask=None, store_obstacle=True):
        """Hide an obstacle on the map, if store_obstacle, the obstacle will be stored in self._hidden_obstacles
        and later added again with reveal_obstacles()"""
        if mask is None:
            mask = full((1, 1), True)
        self.__add_obstacle(point, mask, -1)
        if store_obstacle:
            self.__hidden_obstacles.append((Point(point.x, point.z), array(mask)))

    def reveal_obstacles(self):
        """Adds all hidden obstacles"""
        while self.__hidden_obstacles:
            p, mask = self.__hidden_obstacles.pop()
            self.__add_obstacle(p, mask, 1)

    def add_network_to_obstacle_map(self):
        from terrain.road_network import RoadNetwork
        if self.__all_maps is not None:
            network = self.__all_maps.road_network  # type: RoadNetwork
            for x0, z0 in product(range(self.__width), range(self.__length)):
                if network.is_road(x0, z0):
                    # build a circular obstacle of designated width around road point
                    margin = network.get_road_width(x0, z0) / 2 - .5
                    for x1, z1 in product(sym_range(x0, margin, self.width), sym_range(z0, margin, self.length)):
                        if not self.map[x1, z1]:
                            self.__set_obstacle(x1, z1)

    def box_obstacle(self, box):
        matrix = self.map[box.minx: box.maxx, box.minz:box.maxz]
        return matrix <= 1

    def __getitem__(self, item):
        if len(item) == 2:
            x, z = item
            return self.map[x, z] == 0

    @property
    def width(self):
        return self.map.shape[0]

    @property
    def length(self):
        return self.map.shape[1]
