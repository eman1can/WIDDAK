from numpy.random.mtrand import choice
from statistics import mean

from generation.building_palette import stony_palette
from generation.generators import MaskedGenerator, Generator, place_street_lamp
# from pymclevel.block_fill import fillBlocks
from utils import *


class PlazaGenerator(MaskedGenerator):

    def generate(self, level, height_map=None, palette=None):
        pass
        # terraform_map = self._terraform(level, height_map)
        # self._sub_generator_function(level, height_map, terraform_map, palette)
        # Generator.generate(self, level, height_map, palette)
    #
    # def choose_sub_generator(self, parcels):
    #     if self.width <= 7 or self.length <= 7 or self._box == parcels[0]._box:
    #         self._sub_generator_function = self.__city_plaza
    #     else:
    #         self._sub_generator_function = self.__city_park
    #
    # def __city_plaza(self, level, ground_height, build_height, palette):
    #     self._clear_trees(level)
    #     lamps_gap = max(6, min(self.length // 4, self.width // 4))  # blocks between two street lamps
    #     lamps_rest = lamps_gap // 2  # modulo -> lamp every lamps_gap blocks starting in lamps_rest
    #
    #     # iterate over the plaza surface
    #     for x, y, z in self.surface_pos(build_height):
    #         x0, z0 = x - self.origin.x, z - self.origin.z  # relative coords
    #
    #         # the minimal height for the plaza is the terraformed height
    #         if ground_height[x0, z0] < y:
    #             real_y = y
    #         elif (0 < x0 < self.width - 1) and (0 < z0 < self.length - 1):
    #             real_y = mean(ground_height[x1, z1] for (x1, z1) in product(range(x0-1, x0+2), range(z0-1, z0+2)))
    #             real_y = (real_y + build_height[x0, z0]) / 2  # smoothing term
    #
    #         else:
    #             # borders
    #             real_y = ground_height[x0, z0]
    #
    #         plaza_y = int(real_y) if (real_y % 1 < 0.35) else int(real_y + 1)
    #         if 0.35 <= (real_y % 1) <= 0.65:
    #             material = Materials["{} Slab (Bottom)".format(choice(["Cobblestone", "Stone", "Stone Brick"]))]
    #         else:
    #             material = Materials[choice(stony_palette.keys(), p=stony_palette.values())]
    #         setBlock(level, material, x, plaza_y, z)
    #         if plaza_y > y:
    #             fillBlocks(level, BoundingBox((x, y, z), (1, plaza_y-y, 1)), Materials["Stone"])
    #
    #         if x0 % lamps_gap == lamps_rest and z0 % lamps_gap == lamps_rest and self.is_masked(x0, z0):
    #             place_street_lamp(level, x, plaza_y - int('slab' in material.stringID), z, palette["door"])
    #
    # def __city_park(self, level, ground_height, build_height, palette):
    #     for x, y, z in self.surface_pos(build_height):
    #         if self.is_lateral(x, z):
    #             if (abs(x - self.origin.x - self.width // 2) <= 1) or ((z - self.origin.z - self.length // 2) <= 1):
    #                 continue  # openings
    #             material = Materials["Cobblestone"] if (self.is_corner(Point2D(x, z)) or (x+z) % 3 == 0) else Materials["Cobblestone Wall"]
    #             setBlock(level, material, x, y+1, z)
    #             setBlock(level, Materials["Cobblestone Slab (Bottom)"], x, y+2, z)
    #         else:
    #             setBlock(level, Materials["Grass Block"], x, y, z)
    #     pass
    #
    # def __abs_coords(self, x, z):
    #     pass
