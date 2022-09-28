import random
import math
from pymclevel import biome_types, schematic, MCSchematic, box as bx
from Beautiful_Pallete import Pallete
import utilityFunctions as utilityFunctions

# Information visible in mcedit, can be used for user-input
inputs = (
	("Canal House Generator", "label"),
	("Creator: Koen", "label"),
    ("length", (8, 0, 256)),
    ("height", (10, 0, 256)),
    ("width", (3, 0, 256)),
    ("offset (x)", (0, -256, 256)),
    ("offset (y)", (4, 0, 256)),
    ("offset (z)", (0, -256, 256)),
    ("door location (N=0, W=1, S=2, E=3)", (0, 0, 3)),
    ("number of floors", (2, 1, 10)),
    ("facade type (small stairs=0, large stairs=1, bell=2, flat=3)", (0, 0, 3))
)

def build_bridge(length, delta, width):
    #delta must be greater than length / 2
    delta = delta if delta < int((length - 0)/2) else int((length  - 0) / 2)

    height = delta + 3
    level = MCSchematic((length, height, width))#working object
    box = bx.BoundingBox((0,0,0),(length, height, width))

    pallete = Pallete()

    torch = (50, 5)

    for x in range(delta):
        y = x
        for z in range(width):
            utilityFunctions.setBlock(level, (pallete.stair, 0), x, y, z )
        utilityFunctions.setBlock(level, pallete.fence, x, y + 1, 0)
        utilityFunctions.setBlock(level, pallete.fence, x, y + 1, width - 1)
        utilityFunctions.setBlock(level, pallete.fence, x, y + 2, 0)
        utilityFunctions.setBlock(level, pallete.fence, x, y + 2, width - 1)
    
    x = delta - 1
    utilityFunctions.setBlock(level, torch, x, x + 2, 0)
    utilityFunctions.setBlock(level, torch, x, x + 2, width - 1)

    y = delta - 1
    for x in range(delta, length - delta):
        for z in range(width):
            utilityFunctions.setBlock(level, pallete.floor, x, y, z )
        utilityFunctions.setBlock(level, pallete.fence, x, y + 1, 0)
        utilityFunctions.setBlock(level, pallete.fence, x, y + 1, width - 1)

    not_placed = True
    for x in range(length - delta, length):
        y = length - x - 1
        for z in range(width):
            utilityFunctions.setBlock(level, (pallete.stair, 1), x, y, z )
        utilityFunctions.setBlock(level, pallete.fence, x, y + 1, 0)
        utilityFunctions.setBlock(level, pallete.fence, x, y + 1, width - 1)

        utilityFunctions.setBlock(level, pallete.fence, x, y + 2, 0)
        utilityFunctions.setBlock(level, pallete.fence, x, y + 2, width - 1)

        if not_placed:
            utilityFunctions.setBlock(level, torch, x, y + 2, 0)
            utilityFunctions.setBlock(level, torch, x, y + 2, width - 1)
        not_placed = False

    #print length , height , width
    return level, box

def place_bridge(og_level, length, delta, width, base, rotations):
    scheme, box = build_bridge(length, delta, width)

    if rotations % 2 == 0:
        rot_box = bx.BoundingBox((0,0,0),(box.maxx-box.minx,box.maxy-box.miny,box.maxz-box.minz))
    else:
        rot_box = bx.BoundingBox((0,0,0),(box.maxz-box.minz,box.maxy-box.miny,box.maxx-box.minx))

    for _ in range(rotations):
        scheme.rotateLeft()

    og_level.copyBlocksFrom(scheme, rot_box, base)



def perform(level, box, options):
    height = options["height"]
    width = options["width"]
    length = options["length"]
    base_x = options["offset (x)"]
    base_y = options["offset (y)"]
    base_z = options["offset (z)"]
    rotations = options["door location (N=0, W=1, S=2, E=3)"]
    no_floors = options["number of floors"]
    facade_type = options["facade type (small stairs=0, large stairs=1, bell=2, flat=3)"]
    place_bridge(level, length, height, width, (base_x, base_y, base_z), rotations)
    #self.fence = 85
    #self.fence = 188
    #self.fence = 189