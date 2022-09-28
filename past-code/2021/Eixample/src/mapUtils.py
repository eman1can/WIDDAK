import numpy as np


def calcGoodHeightmap(worldSlice):
    """**Calculates a heightmap ideal for building.**
    Trees are ignored and water is considered ground.

    Args:
        worldSlice (WorldSlice): an instance of the WorldSlice class containing the raw heightmaps and block data

    Returns:
        any: numpy array containing the calculated heightmap
    """
    hm_mbnl = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    heightmapNoTrees = hm_mbnl[:]
    area = worldSlice.rect

    for x in range(area[2]):
        for z in range(area[3]):
            while True:
                y = heightmapNoTrees[x, z]
                block = worldSlice.getBlockAt(
                    (area[0] + x, y - 1, area[1] + z))
                if block[-4:] == '_log':
                    heightmapNoTrees[x, z] -= 1
                else:
                    break

    return np.array(np.minimum(hm_mbnl, heightmapNoTrees))


def getMostFrequentHeight(heightMap):
    return np.bincount(heightMap.flatten()).argmax()


def rotatePointAroundOrigin(origin, point, rotation):
    angle = np.deg2rad(rotation * 90)
    return [
        int(np.round(np.cos(angle) * (point[0] - origin[0]) - np.sin(angle) * (point[2] - origin[2]) + origin[0], 4)),
        point[1],
        int(np.round(np.sin(angle) * (point[0] - origin[0]) + np.cos(angle) * (point[2] - origin[2]) + origin[2], 4))
    ]
