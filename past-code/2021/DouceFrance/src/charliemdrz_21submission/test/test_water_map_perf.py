from itertools import product

from generation import ProcHouseGenerator
from terrain.maps import Maps
import parameters
from pre_processing import Map, MapStock
from matplotlib import colors
from pymclevel import BoundingBox, MCLevel
from utils import TransformBox

displayName = "Water map performance"

inputs = (('hello there', 'label'),
          ('max exploration', 10))


def perform(level, box, options):
    # type: (MCLevel, BoundingBox, dict) -> None
    box = TransformBox(box)
    maps = Maps(level, box)
    img_stock = MapStock("faster_water_map", max(maps.width, maps.length))
    d = options['max exploration']

    maps.fluid_map.detect_sources(level, max_distance=d)
    color_map = colors.ListedColormap(['deepskyblue', 'forestgreen', 'darkcyan', 'lightseagreen', 'aquamarine'])
    water_map = Map("water_map_test_{}".format(parameters.MAX_WATER_EXPLORATION), max(maps.width, maps.length),
                    maps.fluid_map.water.T, color_map, (-1, 3), ["Unlabeled", "No water", "Ocean", "River", "Swamp"]
                    )
    img_stock.add_map(water_map)

    for matrix, title in zip([maps.fluid_map.river_distance, maps.fluid_map.ocean_distance],
                             ['sweet_water_distance{}'.format(d), 'salty_water_distance{}'.format(d)]):
        water_map = Map(title, max(maps.width, maps.length), matrix.T, "jet", (matrix.min(), matrix.max()))
        img_stock.add_map(water_map)
