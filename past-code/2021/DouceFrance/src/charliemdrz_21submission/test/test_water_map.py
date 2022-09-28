from itertools import product

from generation import ProcHouseGenerator
from terrain.maps import Maps
from pre_processing import Map, MapStock
from matplotlib import colors
from pymclevel import BoundingBox, MCLevel
from utils import TransformBox

displayName = "Water map test filter"

inputs = (('algorithm', ('prop', 'spread', 'source (no learning)')),
          ('kernel', ('knn', 'rbf')),
          ('parameter', 4)
          )


def perform(level, box, options):
    # type: (MCLevel, BoundingBox, dict) -> None
    box = TransformBox(box)
    maps = Maps(level, box)
    img_stock = MapStock("water_map", max(maps.width, maps.length))
    alg, kernel, param = options['algorithm'], options['kernel'], options['parameter']

    # maps.fluid_map.detect_sources(level, alg, kernel, param)
    color_map = colors.ListedColormap(['deepskyblue', 'forestgreen', 'darkcyan', 'lightseagreen', 'aquamarine'])
    water_map = Map("water_map_test_{}{}{}".format(alg, kernel, param), max(maps.width, maps.length),
                    maps.fluid_map.water.T, color_map, (-1, 3), ["Unlabeled", "No water", "Ocean", "River", "Swamp"]
                    )
    img_stock.add_map(water_map)

    for matrix, title in zip([maps.fluid_map.river_distance, maps.fluid_map.ocean_distance, maps.fluid_map.lava_distance],
                             ['sweet_water_distance', 'salty_water_distance', 'lava_distance']):
        water_map = Map(title, max(maps.width, maps.length), matrix.T, "jet", (matrix.min(), matrix.max()))
        img_stock.add_map(water_map)
