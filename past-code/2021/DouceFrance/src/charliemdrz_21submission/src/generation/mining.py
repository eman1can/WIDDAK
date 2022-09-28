# from __future__ import division
#
# from math import sqrt
# from random import randint
#
# from numpy import percentile
#
# from generation import Generator, HousePalette
# # from pymclevel import alphaMaterials as Material
# # from pymclevel.block_fill import fillBlocks
# from utils import *
#
#
# class MineEntry(Generator):
#
#     def __init__(self, box, noise_scale=0.1, depth_scale=1, depth_search=5):
#         Generator.__init__(self, box)
#         self.__noise_scale = noise_scale
#         self.__depth_scale = depth_scale
#         self.__depth_search = depth_search
#         self.__border_radius = 7
#
#     def generate(self, level, height_map=None, palette=None):
#         # type: (MCInfdevOldLevel, array, HousePalette) -> None
#
#         def scan_for_cave_entry(xstep=3, ystep=2, zstep=3):
#             # type: (int, int, int) -> tuple
#             """Top down search for a mine or cave. Jumps in step in each direction"""
#             cave_x, cave_y, cave_z = -1, 0, -1
#             shift_x, shift_z = (self.width-1) % xstep != 0, (self.length-1) % zstep != 0
#             explored_coords = list(product(range(int(0.2*self.width), int(0.8*self.width), xstep),
#                                            range(int(0.2*self.length), int(0.8*self.length), zstep)))
#             ymax = height_map.max()
#             for exp_y in range(ymax, -1, -ystep):
#                 shuffle(explored_coords)
#                 for exp_x, exp_z in explored_coords:
#                     exp_x += randint(1, (self.width-1) % xstep) if shift_x else 0
#                     exp_z += randint(1, (self.length-1) % zstep) if shift_z else 0
#                     b = level.blockAt(x0+exp_x, exp_y, z0+exp_z)
#
#                     if exp_y >= height_map[exp_x, exp_z] - self.__depth_search:
#                         continue
#
#                     elif b == 0:
#                         cave_x, cave_y, cave_z = exp_x, exp_y, exp_z
#                         break
#
#                 if cave_x != -1:
#                     break
#
#             while level.blockAt(x0+cave_x, cave_y + 1, z0+cave_z) == 0:
#                 cave_y += 1
#
#             return cave_x, cave_y, cave_z
#
#         def dig_down_to_cave_entry():
#             def dist_to_entry(_x, _y, _z):
#                 return sqrt((_x - entry_x)**2 + (_y - entry_y)**2 + (_z - entry_z)**2)
#             dist_array = array([[dist_to_entry(x, height_map[x, z], z) for z in range(L)] for x in range(W)])
#             mask_dist = percentile(dist_array.ravel(), 80)
#             min_dist = dist_array.min()
#             mask_array = dist_array <= mask_dist
#             # mask_array[0, :] = False
#             # mask_array[W-1, :] = False
#             # mask_array[:, 0] = False
#             # mask_array[:, L-1] = False
#
#             def dig_height(_x, _z):
#                 if not mask_array[_x, _z] or height_map[_x, _z] <= entry_y:
#                     return height_map[_x, _z]
#
#                 dist = dist_array[_x, _z]
#                 dist_ratio = (dist - min_dist) / (mask_dist - min_dist)
#
#                 dist_to_border = euclidean(Point2D(_x, _z), self._box.closest_border(_x, _z, True))
#                 if dist_to_border <= self.__border_radius:
#                     dist_ratio = dist_to_border * dist_ratio + (self.__border_radius - dist_to_border)
#                     dist_ratio /= self.__border_radius
#
#                 eps = dist_ratio ** 3 + self.__noise_scale * (random() - 0.5)
#                 return entry_y + eps * (height_map[_x, _z] - entry_y)
#
#             height_map1 = array([[dig_height(x, z) for z in range(L)] for x in range(W)])
#
#             def smooth_height(_x, _z):
#                 if not mask_array[_x, _z]:
#                     return height_map1[_x, _z]
#
#                 height_sum, count = 0, 0
#                 for dx, dz in product(range(-1, 2), range(-1, 2)):
#                     neighbour_x, neighbour_z = _x + dx, _z + dz
#                     if 0 <= neighbour_x < W and 0 <= neighbour_z < L and mask_array[neighbour_x, neighbour_z]:
#                         height_sum += height_map1[neighbour_x, neighbour_z]
#                         count += 1
#                 return int(round(height_sum / count))
#
#             height_map2 = array([[smooth_height(x, z) for z in range(L)] for x in range(W)])
#
#             for x, z in product(range(W), range(L)):
#                 if mask_array[x, z]:
#                     h2, h0 = height_map2[x, z], height_map[x, z]
#                     fillBlocks(level, TransformBox((x0+x, h2, z0+z), (1, h0+3-h2, 1)), Material[0])  # remove vegetation
#
#         if height_map is None:
#             raise ValueError("Cannot generate mine without height map")
#
#         x0, z0, W, L = self._box.minx, self._box.minz, self.width, self.length
#         self._clear_trees(level)
#         entry_x, entry_y, entry_z = scan_for_cave_entry()  # returns coords relative to self._box
#         print("Cave found at ({}, {}, {})".format(x0+entry_x, entry_y, z0+entry_z))
#         cave_y = entry_y
#         entry_y = max(cave_y, height_map.min() - int(self.__depth_scale * sqrt(min(W, L))))
#         dig_down_to_cave_entry()
#
#         while level.blockAt(entry_x, cave_y-1, entry_z) == 0:
#             cave_y -= 1
#         ladder_box = TransformBox((x0+entry_x+1, cave_y, z0+entry_z), (1, entry_y-cave_y, 1))
#         hole_box = ladder_box.expand(dx_or_dir=1, dz=1).translate(dx=-1)
#         direction = West
#         block = Material["Ladder ({})".format(direction)]
#         fillBlocks(level, hole_box, Material[0])
#         fillBlocks(level, ladder_box, block)
#         fillBlocks(level, ladder_box.translate(dx=1), Material["Oak Wood (Upright)"], [Material[0]])
#
#
# class Agent:
#     def __init__(self, level):
#         self.level = level
#         self.position = None  # type: Point3D
#         self.direction = None  # type: Direction
#         self.view_distance = 5  # type: int
#         self.surroundings = None  # type: array
#
#     def facing_height(self, direction=None):
#         if direction is None:
#             direction = self.direction
#
#
# class MineExplorer(Agent):
#     """An agent that explores a cave, places torches and structures, chests to store ores, etc"""
#
#     def explore(self, starting_point, direction=None):
#         self.position = starting_point
#         self.direction = direction if direction is not None else next(cardinal_directions())
#         # todo: don't know how to do this
#
#
#
