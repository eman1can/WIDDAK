from generation import MineEntry
from pymclevel import MCLevel, BoundingBox
from terrain import Maps
from utils import TransformBox

displayName = "Quarry generator test filter"

inputs = (("Quarry generator", "label"),
          ("Depth search", 5), ("Noise scale", 0.1), ("Depth scale", 1.0))


def perform(level, box, options):
    # type: (MCLevel, BoundingBox, dict) -> None
    box = TransformBox(box)
    maps = Maps(level, box)
    gen = MineEntry(box, options["Noise scale"], options["Depth scale"], options["Depth search"])
    gen.generate(level, maps.height_map.box_height(box, False))
