"""
Classes for generating and storing maps before using the visualization tool

A script is provided to show an example of the use of the classes and for preparing data for visualization

"""

from __future__ import division
import matplotlib
import matplotlib.pyplot as plt
from os.path import isdir, join, exists, abspath, dirname
from os import mkdir
from shutil import rmtree


# Sizes accepted by the visualization tool
# with the size of the figure which is saved in a .png and the width of the grid lines
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
        if map_size <= map_size_ref:
            return ACCEPTED_MAP_SIZES[map_size_ref]
    return ACCEPTED_MAP_SIZES[300]

# Word accepted in user input
VALID_CHOICES = {"yes": 1, "ye": 1, "y": 1, "no": 0, "n": 0, "": 0}


class Map:
    """
    A Map represents a matrix with colors
    """

    def __init__(self, name, size, matrix, color_map, extreme_values, categories=None):
        """
        Create a Map with a specific size and coloration

        :param name: (String) Map's name
        :param size: (Int) The map is a size x size square
        :param matrix: (np.Array) Numpy array that represents the map
        :param color_map: (String or matplotlib.colors.Colormap) Coloration
        """

        assert ((size, size) == matrix.shape)
        self.name = name
        self.size = size
        self.matrix = matrix
        self.color_map = color_map
        self.extreme_values = extreme_values
        self.categories = categories


class MapStock:
    """
    A MapStock manages a storage directory in which it saves given Map of the same size
    """

    def __init__(self, name, map_size, clean_dir=None):
        """
        Create a MapStock with a specific Map size parameter

        :param name: (String) MapStock's name
        :param map_size: (Int) All the Maps managed by this MapStock must be a map_size x map_size square
        :param clean_dir: (Boolean or None, Default : None) Say weather or not the MapStock directory must be clean, if
                            it exists. That can occur when two MapStock with the same name are created or if a script is
                            launch several times. If None, ask the user during execution
        """
        self.name = name
        self.map_size = map_size
        self.directory = join(dirname(abspath(__file__)), "stock",
                              self.name + "_{}x{}".format(self.map_size, self.map_size))
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
            mkdir(self.directory)

    def add_map(self, map):
        """
        Add a map to the MapStock

        :param map: (Map) the Map to add, with the same size than the map_size parameter
        """
        assert (map.size == self.map_size)
        print("Adding {} map to the Stock...".format(map.name))
        self.save_map_to_png(map)

    def save_map_to_png(self, map):
        """
        Save a map as a .png file into the MapStock directory

        :param map: (Map) the Map to save
        """

        # Get predefined parameters
        lw = grid_thickness(self.map_size)

        # Create a figure
        fig = plt.figure()

        # Draw the grid
        for x in range(self.map_size + 1):
            plt.axhline(x, lw=lw, color='k', zorder=5)
            plt.axvline(x, lw=lw, color='k', zorder=5)

        # Draw the cells
        im = plt.imshow(map.matrix, interpolation='none', cmap=map.color_map, extent=[0, self.map_size, 0, self.map_size],
                   zorder=0, vmin=map.extreme_values[0], vmax=map.extreme_values[1])

        # Turn off the axis labels
        plt.axis('off')

        cbar = plt.colorbar()
        if map.categories:
            n = len(map.categories)
            vmin, vmax = map.extreme_values
            cbar.set_ticks([vmin * (1 - i/(2*n)) + vmax * i/(2*n) for i in range(1, n*2, 2)])
            cbar.set_ticklabels(map.categories)



        # Save the figure
        file_path = join(self.directory, map.name + ".png")
        if exists(file_path):
            print("Replacing map...")
        dpi = fig.get_dpi()
        plt.savefig(file_path, dpi=dpi*9)    # increase dpi factor to improve quality
        plt.close()

if __name__ == '__main__':


    from terrain.road_network import *
    from utils import Point2D
    from building_seeding import house_type
    from building_seeding.interest import accessibility

    # Accessibility example

    N = 50

    p1, p2, p3 = Point2D(0, 38), Point2D(27, 17), Point2D(49, 13)

    # Minecraft Map thanks to a RoadNetwork

    road_net = RoadNetwork(N, N)
    road_net.find_road(p1, p2)
    road_net.find_road(p2, p3)
    road_cmap = matplotlib.colors.ListedColormap(['forestgreen', 'beige'])

    road_map = Map("road_network", N, road_net.network, road_cmap, (0, 1), ['Grass', 'Road'])

    # Accessibility Map

    access_net = accessibility(house_type, "Flat_scenario", road_net, (N, N))
    access_cmap = "jet"
    access_map = Map("accessibility_map", N, access_net, access_cmap, (-1, 1))

    the_stock = MapStock("interest_test", N, clean_dir=True)
    the_stock.add_map(road_map)
    the_stock.add_map(access_map)

    # You can know see them into the stock/example_50x50 directory or through the visualization tool
