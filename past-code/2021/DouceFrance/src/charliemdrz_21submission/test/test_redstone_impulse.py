from pymclevel import MCLevel, BoundingBox, alphaMaterials as Block, TAG_Compound, TAG_Int, TAG_String
from pymclevel.entity import TileTick
from utilityFunctions import setBlock

displayName = "Redstone impulse test"

inputs = ()


def perform(level, box, options):
    # type: (MCLevel, BoundingBox, dict) -> None
    block = Block['Redstone Repeater (Unpowered, Delay 4, East)']
    x, y, z = box.origin + (0, 1, 0)
    tile_tick = TAG_Compound()
    tile_tick.add(TAG_Int(-1, 'p'))
    tile_tick.add(TAG_Int(10, 't'))
    tile_tick.add(TAG_Int(x, 'x'))
    tile_tick.add(TAG_Int(y, 'y'))
    tile_tick.add(TAG_Int(z, 'z'))
    tile_tick.add(TAG_String(block.stringID, 'i'))
    level.setBlockAt(x, y, z, block.ID)
    level.setBlockDataAt(x, y, z, block.blockData)
    level.addTileTick(tile_tick)

    x += 1
    block = Block['Dirt']
    setBlock(level, (block.ID, block.blockData), x, y, z)

    y += 1
    block = Block['Lever (Powered, Up_z)']
    setBlock(level, (block.ID, block.blockData), x, y, z)
