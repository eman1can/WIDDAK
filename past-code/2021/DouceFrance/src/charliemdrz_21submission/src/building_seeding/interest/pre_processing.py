"""
Classes for generating and storing maps before using the visualization tool

A script is provided to show an example of the use of the classes and for preparing data for visualization

"""

from __future__ import division

from os import mkdir, makedirs
from matplotlib import pyplot as plt, colors
from os.path import isdir, join, exists, abspath, dirname
from shutil import rmtree
from time import strftime, localtime

import numpy as np
from building_seeding.interest.interest import InterestMap

# Sizes accepted by the visualization tool
# with the size of the figure which is saved in a .png and the width of the grid lines
from terrain import TerrainMaps

ACCEPTED_MAP_SIZES = {10: 0.70,
                      30: 0.25,
                      50: 0.25,
                      100: 0.20,
                      200: 0.15,
                      256: 0.10,
                      300: 0.07}


def grid_thickness(map_size):
    map_size_ref_list = list(ACCEPTED_MAP_SIZES.keys())
    map_size_ref_list.sort()
    for map_size_ref in map_size_ref_list:
        if map_size[0] * map_size[1] <= map_size_ref ** 2:
            return ACCEPTED_MAP_SIZES[map_size_ref]
    return ACCEPTED_MAP_SIZES[300]


# Word accepted in user input
VALID_CHOICES = {"yes": 1, "ye": 1, "y": 1, "no": 0, "n": 0, "": 0}


class VisuHandler:
    def __init__(self, do_visu, terrain: TerrainMaps, parcels):
        self.__count = 1
        self.__do_visu = do_visu
        self.__shape = (terrain.length, terrain.width)
        if do_visu:
            now = strftime("%d%m%Y-%Hh%M", localtime())
            self.__stock = MapStock(now, self.__shape, True)
        self.__parcels = parcels
        self.__roads = terrain.road_network
        self.__base_color_map = terrain.fluid_map.as_obstacle_array * 7

    def handle_new_parcel(self, param):
        # type: (InterestMap) -> None
        if not self.__do_visu:
            return

        building_type = self.__parcels[-1].building_type
        iteration = len(self.__parcels) - 1
        suffix = "_{}".format(building_type.name) if building_type is not None else ""

        acc, soc, int_map = param.accessibility, param.sociability, param.map
        # self.__stock.add_map(Map("{}_accessibility_map{}".format(iteration, suffix), acc.T, "jet", (0, 1)))
        # self.__stock.add_map(Map("{}_sociability_map{}".format(iteration, suffix), soc.T, "jet", (0, 1)))
        self.__stock.add_map(Map("{}_interest_map{}".format(iteration, suffix), int_map.T, "jet", (0, 1)))

        minecraft_map = (self.__roads.network > 0).astype(int) + self.__base_color_map

        COLORS = {"house": 2,
                  "crop": 3,
                  "windmill": 4,
                  "ghost": 5, "wood_tower": 5, "stone_tower": 5}

        for parcel in self.__parcels:
            xmin, xmax = parcel.minx, parcel.maxx
            zmin, zmax = parcel.minz, parcel.maxz

            minecraft_map[xmin:xmax, zmin:zmax][parcel.mask] = COLORS[parcel.building_type.name]
            # minecraft_map[parcel.center.x, parcel.center.z] = COLORS[parcel.building_type.name]

            minecraft_map[parcel.entry_point.x, parcel.entry_point.z] = 6

        # village_center = self.ghost.center
        # minecraft_map[village_center.x, village_center.z] = 5

        minecraft_cmap = colors.ListedColormap(['forestgreen', 'beige', 'indianred', 'darkkhaki', 'orange', 'red', 'purple', 'aqua'])
        self.__stock.add_map(Map("{}_minecraft_map{}".format(iteration, suffix),
                                 minecraft_map.T,
                                 minecraft_cmap,
                                 (0, 7),
                                 ['Grass', 'Road', 'House', 'Crop', 'Windmill', 'VillageCenter', 'EntryPoint', 'Water/Lava']))
        self.__count += 1


class Map:
    """
    A Map represents a matrix with colors
    """

    def __init__(self, name, matrix, color_map, extreme_values, categories=None):
        """
        Create a Map with a specific size and coloration

        :param name: (String) Map's name
        :param matrix: (np.Array) Numpy array that represents the map
        :param color_map: (String or matplotlib.colors.Colormap) Coloration
        """

        self.name = name
        self.shape = matrix.shape
        self.matrix = matrix
        self.color_map = color_map
        self.extreme_values = extreme_values
        self.categories = categories


class MapStock:
    """
    A MapStock manages a storage directory in which it saves given Map of the same size
    """

    def __init__(self, name, map_shape, clean_dir=None):
        """
        Create a MapStock with a specific Map size parameter

        :param name: (String) MapStock's name
        :param map_shape: (Int, Int) All the Maps managed by this MapStock must be a map_size x map_size square
        :param clean_dir: (Boolean or None, Default : None) Say weather or not the MapStock directory must be clean, if
                            it exists. That can occur when two MapStock with the same name are created or if a script is
                            launch several times. If None, ask the user during execution
        """
        self.name = name
        self.map_shape = map_shape
        self.directory = join(dirname(abspath(__file__)), "stock",
                              self.name + "_{}x{}".format(self.map_shape[0], self.map_shape[1]))
        self.manage_directory(clean_dir)

    def manage_directory(self, clean_dir):
        """
        Create a new storage directory or manage the existing one

        :param clean_dir: (Boolean or None, Default : None) Say weather or not the MapStock directory must be clean, if
                            it exists. That can occur when two MapStock with the same name are created or if a script is
                            launch several times. If None, ask the user during execution
        """

        if isdir(self.directory):

            if clean_dir is None:
                while True:

                    print("{} already exists, do you want to clean it? [y/N]".format(self.directory))
                    user_choice = raw_input().lower()
                    if user_choice in VALID_CHOICES:
                        clean_dir = VALID_CHOICES[user_choice]
                        break
                    print("Please respond with 'yes'")

            if clean_dir:
                rmtree(self.directory)
                try:
                    mkdir(self.directory)
                except:
                    mkdir(self.directory)

        else:
            makedirs(self.directory)

    def add_map(self, interest_map):
        # type: (Map) -> None
        """
        Add a map to the MapStock

        :param interest_map: (Map) the Map to add, with the same size than the map_size parameter
        """
        assert (interest_map.shape == self.map_shape)
        print("Adding {} map to the Stock...".format(interest_map.name))
        self.save_map_to_png(interest_map)

    def save_map_to_png(self, interest_map):
        """
        Save a map as a .png file into the MapStock directory

        :param interest_map: (Map) the Map to save
        """

        # Get predefined parameters
        lw = grid_thickness(self.map_shape)

        # Create a figure
        fig = plt.figure()

        # Draw the grid
        for x in range(self.map_shape[0] + 1):
            # plt.axhline(x, lw=lw, color='k', zorder=5)
            plt.axvline(x, lw=lw, color='k', zorder=5)
        for z in range(self.map_shape[1] + 1):
            plt.axhline(z, lw=lw, color='k', zorder=5)
            # plt.axvline(z, lw=lw, color='k', zorder=5)

        # Draw the cells
        im = plt.imshow(interest_map.matrix, interpolation='none', cmap=interest_map.color_map,
                        extent=[0, self.map_shape[1], 0, self.map_shape[0]],
                        zorder=0, vmin=interest_map.extreme_values[0], vmax=interest_map.extreme_values[1])

        # Turn off the axis labels
        plt.axis('off')

        cbar = plt.colorbar()
        if interest_map.categories:
            n = len(interest_map.categories)
            vmin, vmax = interest_map.extreme_values
            cbar.set_ticks([vmin * (1 - i/(2*n)) + vmax * i/(2*n) for i in range(1, n*2, 2)])
            cbar.set_ticklabels(interest_map.categories)

        # Save the figure
        file_path = join(self.directory, interest_map.name + ".png")
        if exists(file_path):
            print("Replacing map...")
        dpi = fig.get_dpi()
        plt.savefig(file_path, dpi=dpi*4)    # increase dpi factor to improve quality
        plt.close()


if __name__ == '__main__':

    # from matplotlib import pyplot as plt, colors
    from terrain.road_network import *
    from utils import Point2D
    from building_seeding.building_pool import BuildingType, BuildingType
    from building_seeding.interest.accessibility import accessibility
    # Accessibility example

    N = (7, 17)

    # p1, p2, p3 = Point2D(0, 38), Point2D(27, 17), Point2D(49, 13)
    p1, p2, p3 = Point2D(0, 2), Point2D(4, 13), Point2D(6, 4)
    # Minecraft Map thanks to a RoadNetwork

    road_net = RoadNetwork(N[0], N[1])
    road_net.create_road(p1, p2)
    road_net.connect_to_network(p3)
    road_cmap = colors.ListedColormap(['forestgreen', 'beige'])

    road_map = Map("road_network", road_net.network, road_cmap, (0, 1), ['Grass', 'Road'])

    # Accessibility Map

    access_net = accessibility(BuildingType.house, "Flat_scenario", road_net, N)
    access_cmap = "jet"
    access_map = Map("accessibility_map", access_net, access_cmap, (-1, 1))

    the_stock = MapStock("interest_test", N, clean_dir=True)
    the_stock.add_map(road_map)
    the_stock.add_map(access_map)

    # You can know see them into the stock/example_50x50 directory or through the visualization tool
