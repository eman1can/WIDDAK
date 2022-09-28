from itertools import product
from time import sleep

from terrain import TerrainMaps
from utils import Point, BlockAPI, setBlock
from random import sample

terrain = TerrainMaps.request()
directions = ["east", "west", "north", "south"]
bools = ["true", "false"]
halves = ["top", "bottom"]
materials = ["acacia", "birch", "stone", "cobblestone"]

for dx, dz in product(range(terrain.width), range(terrain.length)):
    p = Point(terrain.area.x + dx, terrain.area.z + dz, terrain.height_map[dx, dz])
    b = BlockAPI.getStairs(sample(materials, 1)[0], facing=sample(directions, 1)[0], half=sample(halves, 1)[0], waterlogged=sample(bools, 1)[0])
    print(p, b)
    print(setBlock(p, b))
    sleep(.3)

