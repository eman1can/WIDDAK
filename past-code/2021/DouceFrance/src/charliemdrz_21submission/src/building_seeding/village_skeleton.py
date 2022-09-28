"""
Village skeleton growth
"""

from numpy import argmin
from statistics import mean

from building_seeding.districts import Districts
from terrain import TerrainMaps
from building_seeding.building_pool import BuildingPool, BuildingType
from building_seeding.interest.pre_processing import VisuHandler
from building_seeding.parcel import Parcel, MaskedParcel
from building_seeding.interest import InterestSeeder
from parameters import MIN_PARCEL_SIZE, AVERAGE_PARCEL_SIZE
from utils import *


class VillageSkeleton:

    def __init__(self, scenario: str, maps: TerrainMaps, districts: Districts, parcel_list: List[Parcel]):
        self.scenario = scenario
        self.size = (maps.width, maps.length)
        self.maps = maps
        self.ghost = districts.town_centers[0]
        buildable_surface = maps.width * maps.length - maps.fluid_map.as_obstacle_array.sum()
        self.building_iterator = BuildingPool(districts.buildable_surface)
        self.__parcel_list = parcel_list
        self.parcel_size = MIN_PARCEL_SIZE

        # parcel_list.append(Parcel(ghost_position, BuildingType.from_name('ghost'), maps))
        self.__interest = InterestSeeder(maps, districts, parcel_list, scenario)

    def add_parcel(self, seed, building_type):
        if isinstance(seed, Point):
            if building_type.name in ["crop"]:
                new_parcel = MaskedParcel(seed, building_type, self.maps)
            else:
                new_parcel = Parcel(seed, building_type, self.maps)
        elif isinstance(seed, Parcel):
            new_parcel = seed
            new_parcel.building_type = BuildingType.ghost
        else:
            raise TypeError("Expected Point or Parcel, found {}".format(seed.__class__))
        self.__parcel_list.append(new_parcel)
        new_parcel.mark_as_obstacle(self.maps.obstacle_map, margin=AVERAGE_PARCEL_SIZE//3)

    def __handle_new_road_cycles(self, cycles):

        for road_cycle in cycles:
            city_block = CityBlock(road_cycle, self.maps)
            block_parcel = city_block.parcels()
            seed = block_parcel.center
            # block_seed = Point(int(mean(p.x for p in road_cycle)), int(mean(p.z for p in road_cycle)))
            block_type = self.__interest.get_optimal_type(seed)
            if block_type:
                self.add_parcel(seed, block_type)
                # self._create_masked_parcel(block_seed, BuildingType().ghost)
                # parcel is considered already linked to road network
            else:
                # if there already is a parcel in the block, or very close, it is moved to the block seed
                dist_to_parcels = list(map(lambda parcel: euclidean(parcel.center, seed), self.__parcel_list))
                if min(dist_to_parcels) <= AVERAGE_PARCEL_SIZE / 2:
                    index = int(argmin(dist_to_parcels))
                    old_parcel = self.__parcel_list[index]
                    self.maps.obstacle_map.hide_obstacle(old_parcel.origin, old_parcel.mask, False)
                    block_parcel.mark_as_obstacle(self.maps.obstacle_map)
                    block_parcel.building_type = old_parcel.building_type
                    self.__parcel_list[index] = block_parcel
                else:
                    # add a park or plaza in the new cycle
                    self.add_parcel(block_parcel, BuildingType.ghost)

    def grow(self, time_limit: int, do_visu: bool):
        print("Seeding parcels")
        map_plots = VisuHandler(do_visu, self.maps, self.__parcel_list)
        build_iter = self.building_iterator

        t0 = time()
        for building_type in build_iter:

            print(f"\nTrying to place {building_type.name} - #{build_iter.count} out of {build_iter.size}")

            # Village Element Seeding Process
            self.__interest.reuse_existing_parcel(building_type)  # If succeeds should update building_type in place
            building_position = self.__interest.get_seed(building_type)

            if building_position is None:
                print("No suitable position found")
                continue

            print("Placed at x:{}, z:{}".format(building_position.x, building_position.z))

            # Road Creation Process
            cycles = self.maps.road_network.connect_to_network(building_position, margin=AVERAGE_PARCEL_SIZE/2)
            self.add_parcel(building_position, building_type)
            map_plots.handle_new_parcel(self.__interest[building_type])  # does nothing if not do_visu
            # self.__handle_new_road_cycles(cycles)
            if time_limit and time() - t0 >= time_limit:
                print("Time limit reached: early stopping parcel seeding")
                break


class CityBlock:
    def __init__(self, road_cycle, maps):
        self.__road_points = road_cycle
        self.__maps = maps
        self.__origin = Point(min(_.x for _ in road_cycle), min(_.z for _ in road_cycle))
        self.__limits = Point(max(_.x for _ in road_cycle), max(_.z for _ in road_cycle))

    @staticmethod
    def connection(src_point, dst_point, maps):
        return not maps.road_network.is_road(dst_point)

    def parcels(self):
        seed = Point(int(mean(p.x for p in self.__road_points)), int(mean(p.z for p in self.__road_points)))
        origin, mask = connected_component(self.__maps, seed, CityBlock.connection)
        parcel_origin = Point(max(origin.x, self.minx), max(origin.z, self.minz))
        parcel_limits = Point(min(origin.x+mask.shape[0], self.maxx), min(origin.z+mask.shape[1], self.maxz))
        parcel_shapes = Point(1, 1) + parcel_limits - parcel_origin
        parcel_mask = mask[(parcel_origin.x - origin.x): (parcel_origin.x - origin.x + parcel_shapes.x),
                           (parcel_origin.z - origin.z): (parcel_origin.z - origin.z + parcel_shapes.z)]
        return MaskedParcel(parcel_origin, BuildingType.ghost, self.__maps, parcel_mask)

    @property
    def minx(self):
        return self.__origin.x

    @property
    def maxx(self):
        return self.__limits.x

    @property
    def minz(self):
        return self.__origin.z

    @property
    def maxz(self):
        return self.__limits.z
