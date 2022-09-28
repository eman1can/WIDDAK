from itertools import product

from pymclevel import MCLevel, BoundingBox
from utils import Point2D, clear_tree_at

displayName = "Clear tree test filter"

inputs = ()


def perform(level, box, options):
    # type: (MCLevel, BoundingBox, dict) -> None
    for x, z in product(range(box.minx, box.maxx), range(box.minz, box.maxz)):
        clear_tree_at(level, Point2D(x, z))
