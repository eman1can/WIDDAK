from typing import Tuple

import numba
from numba import prange, i8
from numba.core.types import UniTuple, Set as nbSet

from terrain import HeightMap
from terrain.map import Map
from utils import *
from utils.misc_objects_functions import _in_limits
from worldLoader import WorldSlice


class TreesMap(Map):
    def __init__(self, level: WorldSlice, height: HeightMap):
        values, trees = _process(level, height)
        super().__init__(values)
        self.__trees: List[List, Tuple[int, int, int]] = trees
        self.__origin = Point(level.rect[0], level.rect[1])

    def remove_tree_at(self, position: Point):
        tree_index = int(self[position])
        for x, y, z in self.__trees[tree_index]:
            tree_point = Point(x, z, y) + self.__origin
            setBlock(tree_point, BlockAPI.blocks.Air)
        self.__trees[tree_index] = []


# @numba.jit()
def _detect_trunks(level: WorldSlice, height: HeightMap):
    # detect trunks
    first_elt = UniTuple(i8, 2)(height.width, height.length)
    # trunks = nbSet(UniTuple(i8, 2))(first_elt)
    trunks = {first_elt}

    for xz in prange(height.width * height.length):
        x = xz // height.length
        z = xz % height.length
        y = height[x, z] + 1
        block = getBlockRelativeAt(level, x, y, z)
        if _is_trunk(block):
            trunks.add((x, z))

    trunks.remove(first_elt)
    return trunks


def _process(level: WorldSlice, height: HeightMap):
    width, length = height.width, height.length
    values = zeros((width, length))

    trunks = _detect_trunks(level, height)
    print(len(trunks))

    # Initialize tree structure & propagation
    tree_blocks: List[UniTuple(i8, 2)] = []
    marked_blocks: nbSet(UniTuple(i8, 2)) = set()

    tree_index = 1
    trees = [[]]
    for position in trunks:
        trees.append([])
        tree_blocks.append((*position, tree_index))
        marked_blocks.add(position)
        tree_index += 1

    # propagate trees through trunks and leaves (and mushrooms)
    while tree_blocks:
        # Get the oldest element in the blocks to process
        x1, z1, tree_index = tree_blocks.pop(0)  # type: int, int, int

        # add it to the structure of its tree
        for y1 in range(height[x1, z1]+1, height.upper_height(x1, z1)+1):
            trees[tree_index].append((x1, y1, z1))
        values[x1, z1] = tree_index

        # check if neighbours for possible other tree points
        for x2 in prange(x1 - 1, x1 + 2):
            for z2 in prange(z1 - 1, z1 + 2):
                if _in_limits((x2, 0, z2), width, length):
                    y2 = height.upper_height(x2, z2)
                    position = (x2, y2, z2)
                    possible_tree_point = (x2, z2)
                    if (possible_tree_point not in marked_blocks) and _is_tree(getBlockRelativeAt(level, *position)):
                        marked_blocks.add(possible_tree_point)
                        tree_blocks.append((*possible_tree_point, tree_index))

    print(sum(len(tree) for tree in trees))
    return values, trees


@numba.njit(cache=True)
def _is_trunk(block: str) -> bool:
    return 'log' in block or 'stem' in block


@numba.njit(cache=True)
def _is_tree(bid: str) -> bool:
    return _is_trunk(bid) or '_leaves' in bid or 'mushroom_block' in bid


# @numba.njit(b1(UniTuple(i8, 3), string, nbSet(UniTuple(i8, 3))))
# def _neighbours_not_trees(p0: UniTuple(i8, 3), block0: str, trunks0: Set[UniTuple(i8, 3)]):
#     if block0.startswith("oak") or block0.startswith("birch") or block0.startswith("acacia"):
#         return True
#     x, z, y = p0
#     for dx, dz, dy in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)]:
#         if (x + dx, z + dz, y + dy) in trunks0:
#             return False
#     return True
