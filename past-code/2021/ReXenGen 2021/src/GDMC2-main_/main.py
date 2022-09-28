import interfaceUtils as minecraft
import maths


USE_BATCHING = True


def setBlock(block, xyz):
    x, y, z = xyz
    if USE_BATCHING:
        minecraft.placeBlockBatched(x, y, z, block, 100)
    else:
        minecraft.setBlock(x, y, z, block)


def getBlock(xyz):
    x, y, z = xyz
    return minecraft.getBlock(x, y, z)


def fillBlock(block, xyz):
    print(minecraft.runCommand(f"fill %i %i %i %i %i %i {block}" % tuple(xyz)))


def setLine(block, xyz0, xyz1, pixelPerfect=True):
    points = maths.line(xyz0, xyz1, pixelPerfect)
    for i in points:
        setBlock(block, (i[0], i[1], i[2]))