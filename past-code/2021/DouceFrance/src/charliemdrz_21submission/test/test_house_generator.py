from generation import ProcHouseGenerator
from generation.building_palette import *
from terrain.maps import Maps
from pymclevel import BoundingBox, MCLevel
from utils import TransformBox

displayName = "House generator test filter"

inputs = (("palette", ("Oak", "Birch", "Dark Oak", "Spruce", "Acacia", "Jungle", "Sand", "Red Sand", "Terracotta")),
          ("Creator: Charlie", "label")
          )


def perform(level, box, options):
    # type: (MCLevel, BoundingBox, dict) -> None
    box = TransformBox(box)
    maps = Maps(level, box)
    gen = ProcHouseGenerator(box)
    palette_str = options["palette"]
    if palette_str == "Oak":
        palette = oak_palette1
    elif palette_str == "Birch":
        palette = birch_house_palette1
    elif palette_str == "Dark Oak":
        palette = dark_oak_house_palette1
    elif palette_str == "Spruce":
        palette = spruce_palette1
    elif palette_str == "Acacia":
        palette = acacia_house_palette1
    elif palette_str == "Jungle":
        palette = jungle_house_palette1
    elif palette_str == "Sand":
        palette = sand_house_palette1
    elif palette_str == "Red Sand":
        palette = red_sand_house_palette1
    elif palette_str == "Terracotta":
        palette = terracotta_palette1
    else:
        raise ValueError("Unhandled option: {}".format(palette_str))
    gen.generate(level, maps.height_map, palette)
