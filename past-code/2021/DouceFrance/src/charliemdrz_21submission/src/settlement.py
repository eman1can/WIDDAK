from __future__ import division

import logging
from math import exp
from random import choice
from typing import List

from numpy import percentile
from numpy.random import geometric, normal

from building_seeding import Districts, Parcel, VillageSkeleton, BuildingType, MaskedParcel
from generation.building_palette import get_biome_palette
from generation.generators import place_sign
from interfaceUtils import sendBlocks
from parameters import MAX_HEIGHT, BUILDING_HEIGHT_SPREAD, MIN_PARCEL_SIZE
from terrain import TerrainMaps
from terrain.road_network import RoadNetwork
from utils import *
from utils.algorithms import min_spanning_tree, tree_distance

MEAN_ROAD_COVERED_SURFACE = 64  # to compute number of roads, max 1 external connexion per 1/64 of the settlement size
SETTLEMENT_ACCESS_DIST = 25  # maximum distance from settlement center to road net


class Settlement:
    """
    Intermediate project: generate a realistic village on a flat terrain
    """
    def __init__(self, maps):
        # type: (TerrainMaps) -> Settlement
        self._maps = maps  # type: TerrainMaps
        self.districts = Districts(self._maps.area)
        self._origin = maps.area.origin
        self._center: Point = Point(0, 0)
        self._road_network = self._maps.road_network
        self._parcels: List[Parcel] = []

    def __random_border_point(self):
        # type: () -> Point
        # width, length = self.limits.width, self.limits.length
        # # random draw to decide on what side the border will be. Favors larger sides
        # if bernouilli(width / (width + length)):
        #     # border point along x border
        #     x = 0 if bernouilli() else self.limits.width - 1
        #     z = randint(0, length - 1)
        # else:
        #     # border point along z border
        #     x = randint(0, width - 1)
        #     z = 0 if bernouilli() else self.limits.length - 1
        # return Point2D(x, z)
        return choice(self._maps.fluid_map.external_connections)

    def build_districts(self, **kwargs):
        self.districts.build(self._maps, **kwargs)

        # init road net
        if self.districts.n_districts >= 2:
            main_roads = min_spanning_tree(self.districts.district_centers)
            for p1, p2 in main_roads:
                self._road_network.create_road(p1, p2)
        else:
            self._road_network.create_road(self.districts.district_centers[0], self.districts.district_centers[0])
        self.init_road_network()

        # mark town centers
        for town_center in self.districts.town_centers:
            self._parcels.append(Parcel(town_center, BuildingType.ghost, self._maps))
            self._parcels[-1].mark_as_obstacle(self._maps.obstacle_map)

    def init_road_network(self):
        # out_connections = [self.__random_border_point()]
        max_road_count = max(1, min(self.limits.width, self.limits.length) // MEAN_ROAD_COVERED_SURFACE)
        # logging.debug('Max road count: {}'.format(max_road_count))
        road_count = min(geometric(1./max_road_count), max_road_count*3//2)
        logging.debug('New settlement will have {} external connections B)'.format(road_count))
        # logging.debug('First border point @{}'.format(str(out_connections[0])))
        # self._road_network.create_road(self._parcels[0].entry_point, out_connections[0])
        out_connections = [Point(self.limits.width//2, self.limits.length//2)]

        for road_id in range(road_count):
            min_distance_to_roads = min(self.limits.width, self.limits.length) / (road_id+1)
            logging.debug('Generating road #{}'.format(road_id+1))
            # generate new border point far enough from existing points
            while True:
                new_road_point = self.__random_border_point()
                distances = [euclidean(road_point, new_road_point) for road_point in out_connections]
                distance_to_roads = min(distances)
                log_args = (str(new_road_point), distance_to_roads, min_distance_to_roads)
                if distance_to_roads >= min_distance_to_roads:
                    out_connections.append(new_road_point)
                    logging.debug('\tSettled on border point {} at {}m >= {}m'.format(*log_args))
                    break
                else:
                    logging.debug('\tDismissed point {} at {}m < {}m'.format(*log_args))
                    min_distance_to_roads *= 0.9
            self._road_network.connect_to_network(out_connections[-1])

    def build_skeleton(self, time_limit: int, do_visu: bool = False):
        village_skeleton = VillageSkeleton('Flat_scenario', self._maps, self.districts, self._parcels)
        village_skeleton.grow(time_limit, do_visu)
        # for parcel in filter(lambda p: p.building_type.name == 'ghost', self._parcels):
        #     self._parcels.remove(parcel)

    def define_parcels(self):
        """
        Parcel extension from initialized parcels. Parcels are expended in place
        """
        print("Extending parcels")
        # self._parcels = self._parcels[1:]
        obs = self._maps.obstacle_map
        obs.map[:] = 0
        obs.add_network_to_obstacle_map()
        for parcel in self._parcels:
            parcel.mark_as_obstacle(obs)
        obs.map += self._maps.fluid_map.as_obstacle_array
        expendable_parcels: List[Parcel] = [p for p in self._parcels[:] if p.is_expendable()]

        surface = sum(p.bounds.volume for p in expendable_parcels)
        while expendable_parcels:
            # extend expendables parcels while there still are some

            for parcel in expendable_parcels:
                if parcel.entry_point == parcel.center:
                    self._parcels.remove(parcel)
                    expendable_parcels.remove(parcel)
                    continue
                # direction computation
                road_dir_x = parcel.entry_x - parcel.mean_x
                road_dir_z = parcel.entry_z - parcel.mean_z
                road_dir = Direction.of(road_dir_x, 0, road_dir_z)
                lateral_dir = road_dir.rotate() if bernouilli() else -road_dir.rotate()

                priority_directions = [road_dir, lateral_dir, -lateral_dir, -road_dir]
                for direction in priority_directions:
                    if parcel.is_expendable(direction):
                        parcel.expand(direction)
                        break

            expendable_parcels = list(filter(lambda _: _.is_expendable, expendable_parcels))
            tmp = surface
            surface = sum(p.bounds.volume for p in expendable_parcels)
            if tmp >= surface:
                break

        # set parcels heights
        def define_parcels_heights(__parcel):
            # type: (Parcel) -> None
            min_y = percentile(__parcel.height_map, 25)
            max_y = percentile(__parcel.height_map, 75)
            road_y = self._maps.height_map[__parcel.entry_point]
            y = road_y
            if road_y > max_y:
                y = max_y
            elif road_y < min_y:
                y = min_y
            try:
                d = min(euclidean(__parcel.center, _.center) for _ in
                        filter(lambda p: p.building_type.name == "ghost", self._parcels)
                        )
            except ValueError:
                d = 0
            h = int(MAX_HEIGHT * exp(-d / BUILDING_HEIGHT_SPREAD))
            __parcel.set_height(y, h)

        print("Defining parcels' and buildings' heights")
        for p in self._parcels:
            p.compute_entry_point()
            define_parcels_heights(p)
            # translate all parcels to absolute coordinates
            p.translate_to_absolute_coords(self._origin)

    def generate(self, terrain: TerrainMaps, print_stack=False):
        self._road_network.generate(terrain, self.districts)
        self.__generate_road_signs()

        for parcel in self._parcels:  # type: Parcel
            def in_bounds():
                corner1 = parcel.origin + self._origin
                corner2 = corner1 + Point(parcel.width, parcel.length) - Point(1, 1)
                return corner1 in self._maps.area and corner2 in self._maps.area

            if not in_bounds():
                continue
            parcel_biome = parcel.biome(terrain)
            palette = get_biome_palette(parcel_biome)
            if isinstance(parcel, MaskedParcel):
                obstacle_mask = self._maps.obstacle_map.box_obstacle(parcel.bounds)
                parcel.add_mask(obstacle_mask)
            if print_stack:
                gen = parcel.generator
                gen.choose_sub_generator(self._parcels)
                gen.generate(terrain, parcel.height_map, palette)
            else:
                try:
                    gen = parcel.generator
                    gen.choose_sub_generator(self._parcels)
                    gen.generate(terrain, parcel.height_map, palette)
                except Exception:
                    print("FAIL")

        sendBlocks()

    @property
    def town_center(self):
        return self._center

    @property
    def limits(self):
        return self._maps.area

    def terraform(self):
        """
        Smooth out the terrain around locations that will be built on
        """
        import cv2
        from numpy import uint8
        base_height = uint8(self._maps.height_map[:])
        smooth_height = cv2.medianBlur(base_height, 7)

        # Compute constructable locations: road net + parcels
        mask = zeros(base_height.shape)

        for pos in self._road_network.road_blocks:
            x0 = max(pos.x - 2, 0)
            x1 = min(pos.x + 3, self.limits.width)
            z0 = max(pos.z - 2, 0)
            z1 = min(pos.z + 3, self.limits.length)
            mask[x0:x1, z0:z1] = 1

        for parcel in self._parcels:
            x0 = max(parcel.minx - 2, 0)
            x1 = min(parcel.maxx + 3, self.limits.width)
            z0 = max(parcel.minz - 2, 0)
            z1 = min(parcel.maxz + 3, self.limits.length)
            mask[x0:x1, z0:z1] = 1
        # del x0, x1, z0, z1, parcel, pos

        mask[self._maps.fluid_map.water > 0] = 0  # discount water

        for x, z in filter(lambda u: mask[u] and base_height[u] != smooth_height[u],
                           product(range(self.limits.width), range(self.limits.length))):
            xa = x + self.limits.x
            za = z + self.limits.z
            ya = base_height[x, z]
            new_y = smooth_height[x, z]
            self._maps.height_map.update([Point(x, z)], [new_y])
            surface_block = self._maps.level.getBlockAt((xa, ya, za))
            setBlock(Point(xa, za, new_y), surface_block)

            if new_y > ya:
                below_block = self._maps.level.getBlockAt((xa, ya - 1, za))
                box = TransformBox((xa, ya, za), (1, new_y - ya, 1))
                fillBlocks(box, below_block)

            elif new_y < ya:
                # actually an else block
                box = TransformBox((xa, new_y + 1, za), (1, ya - new_y - 1, 1))
                fillBlocks(box, BlockAPI.blocks.Air)

    def clean_road_network(self):
        road_map = (self._road_network.network > 0).astype(int)
        network: RoadNetwork = self._road_network

        def degree(p: Point):
            arr = road_map[max(0, p.x - 1):min(p.x + 2, road_map.shape[0]),
                           max(0, p.z - 1):min(p.z + 2, road_map.shape[1])]
            return arr.sum() - 1

        def get_neighbour(p: Point):
            for dx, dz in product(range(-1, 2), range(-1, 2)):
                if self._maps.in_limits(p + Point(dx, dz), False) and road_map[p.x + dx, p.z + dz]:
                    return p + Point(dx, dz)

        def unset_road(p: Point):
            if p in network.road_blocks:
                network.road_blocks.remove(p)
            else:
                network.special_road_blocks.remove(p)
            road_map[p.x, p.z] = 0
            network.network[p.x, p.z] =0

        for extremity in filter(lambda node: degree(node) == 1, network.nodes):
            truncated_length = 0
            while truncated_length < 8 and degree(extremity) == 1:
                unset_road(extremity)
                extremity = get_neighbour(extremity)
                truncated_length += 1

    def __generate_road_signs(self):
        roads = min_spanning_tree(self.districts.district_centers)
        distance_map = tree_distance(roads)
        for point in self.districts.district_centers:
            towns = sorted(filter(lambda u: point != u, self.districts.town_centers), key=lambda town: distance_map[point, town])
            towns = towns[:3] if len(towns) > 3 else towns
            y = self._maps.height_map[point] + 1
            setBlock(Point(point.x, point.z, y-1), BlockAPI.blocks.PolishedDiorite)
            for dy, town in enumerate(towns):
                dir = town - point
                dir = Point(-dir.z, dir.x)
                pos = point + self._origin + Direction.Top.value * (y + dy)
                if point in self.districts.town_centers and town == towns[-1]:
                    place_sign(pos, BlockAPI.blocks.OakSign, dir, Text1=self.districts.town_names[point], Text2="--------", Text3=f"{self.districts.town_names[town]}", Text4=f"<--- {int(distance_map[point, town])}m")
                else:
                    place_sign(pos, BlockAPI.blocks.OakSign, dir, Text2=f"{self.districts.town_names[town]}", Text3=f"<--- {int(distance_map[point, town])}m")
