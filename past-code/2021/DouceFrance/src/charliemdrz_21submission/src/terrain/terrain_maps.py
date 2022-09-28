from itertools import product

from terrain import ObstacleMap, RoadNetwork
from terrain.tree_map import TreesMap
from utils import BuildArea, BoundingBox
from terrain.biomes import BiomeMap
from terrain.fluid_map import FluidMap
from terrain.height_map import HeightMap
# from terrain.obstacle_map import Obstacle  # todo: rewrite ObstacleMap
from worldLoader import WorldSlice


class TerrainMaps:
    """
    The Map class gather all the maps representing the Minecraft Map selected for the filter
    """

    def __init__(self, level: WorldSlice, area: BuildArea):
        self.level = level
        self.area: BuildArea = area
        from time import time
        t0 = t1 = time()
        self.height_map = HeightMap(level, area)
        print(f'Computed height map in {time() - t1}')

        t1 = time()
        self.biome = BiomeMap(level, area)
        print(f'Computed biome map in {time() - t1}')

        t1 = time()
        self.fluid_map = FluidMap(level, area, self)
        print(f'Computed fluid map in {time() - t1}')

        t1 = time()
        self.obstacle_map = ObstacleMap(self.width, self.length, self)
        print(f'Computed obstacle map in {time() - t1}')

        t1 = time()
        self.road_network = RoadNetwork(self.width, self.length, self)  # type: RoadNetwork
        print(f'Computed road map in {time() - t1}')

        t1 = time()
        self.trees = TreesMap(level, self.height_map)
        print(f'Computed trees map in {time() - t1}')

        t1 = time()
        print(f'Computed terrain maps in {t1 - t0}')

    @property
    def width(self):
        return self.area.width

    @property
    def length(self):
        return self.area.length

    @property
    def shape(self):
        return self.width, self.length

    @property
    def box(self):
        return BoundingBox((self.area.x, 0, self.area.z), (self.width, 256, self.length))

    def in_limits(self, point, absolute_coords):
        if absolute_coords:
            return point in self.area
        else:
            return point + self.area.origin in self.area

    @staticmethod
    def request():
        from time import time
        print("Requesting build area...", end='')
        build_area = BuildArea()
        print(f"OK: {str(build_area)}")
        print("Requesting level...")
        t0 = time()
        level = WorldSlice((build_area.x, build_area.z, build_area.width, build_area.length))
        print(f"completed in {(time()-t0)}s")
        return TerrainMaps(level, build_area)

    def undo(self):
        """
        Undo all modifications to the terrain for debug purposes
        """
        from utils import setBlock, Point
        from gdmc_http_client_python.interfaceUtils import runCommand
        from utils.block_utils import alterated_pos
        for xa, za in filter(lambda xz: self.in_limits(Point(xz[0], xz[1]), True), alterated_pos):
            x, z = xa - self.area.x, za - self.area.z
            ya = self.height_map.upper_height(x, z) + 1
            for y in range(self.height_map.lower_height(x, z)-3, ya):
                setBlock(Point(xa, za, y), self.level.getBlockAt((xa, y, za)), 1000)
            runCommand(f'fill {xa} {ya} {za} {xa} {255} {za} minecraft:air')
        from interfaceUtils import sendBlocks
        sendBlocks()
