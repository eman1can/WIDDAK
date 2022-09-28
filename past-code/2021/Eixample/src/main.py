import interfaceUtils
import HousingBlock

# Set to True to enable multi-threading. This will make the built go slightly faster, but can also crash the
# Minecraft Forge server/client when there are too many threads, which may occur when constructing in a large
# build area.
USE_THREADING = False


def getBuildArea(area=(0, 0, 128, 128)):
    # x position, z position, x size, z size

    # see if a build area has been specified
    # you can set a build area in minecraft using the /setbuildarea command
    serverBuildArea = interfaceUtils.requestBuildArea()
    if serverBuildArea != -1:
        x1 = serverBuildArea["xFrom"]
        z1 = serverBuildArea["zFrom"]
        x2 = serverBuildArea["xTo"]
        z2 = serverBuildArea["zTo"]
        area = (x1, z1, x2 - x1, z2 - z1)

    print("working in area xz s%s" % (str(area)))
    return area


buildArea = getBuildArea()

HousingBlock.USE_THREADING = USE_THREADING

settlementSizeX = 0
while settlementSizeX <= buildArea[2]:
    settlementSizeZ = 0
    while settlementSizeZ <= buildArea[3]:
        housingBlock = HousingBlock.HousingBlock(
            x=buildArea[0] + settlementSizeX, z=buildArea[1] + settlementSizeZ
        )
        settlementSizeZ += housingBlock.getSizeZ()
        housingBlock.place()
    settlementSizeX += housingBlock.getSizeX()

interfaceUtils.sendBlocks()
