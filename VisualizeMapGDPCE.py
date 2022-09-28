"""
    A GDPCE Version of the VisualizeMap.py from GDCP
"""

__author__    = "Ethan Wolfe"
__copyright__ = "Copyright 2022, Ethan Wolfe"
__licence__   = "MIT"


import numpy as np
from gdpc import lookup
from gdpc.toolbox import loop2d
from glm import ivec2
from matplotlib import pyplot as plt
from gdpce.interface import getBuildArea, getWorldSlice
from gdpce.geometry import Rect

import cv2
print('Finished Imports')

def main():
    print('Getting The World Slice')
    # Get the build area
    buildArea = getBuildArea()
    buildRect = buildArea.toRect()

    # Get world slice and height map
    worldSlice = getWorldSlice(buildRect)
    heightMap = np.array(worldSlice.heightmaps["OCEAN_FLOOR"], dtype=int)

    print('Calculating World Data')
    # calculate the gradient (steepness)
    decrementor = np.vectorize(lambda a: a - 1)
    cvheightmap = np.clip(decrementor(heightMap), 0, 255).astype(np.uint8)
    gradientX = cv2.Scharr(cvheightmap, cv2.CV_16S, 1, 0)
    gradientY = cv2.Scharr(cvheightmap, cv2.CV_16S, 0, 1)

    # create a dictionary mapping block ids ("minecraft:...") to colors
    palette = lookup.PALETTELOOKUP

    # create a 2d map containing the surface block colors
    topcolor = np.zeros((buildRect.size + 1), dtype='int')
    unknownBlocks = set()

    for x, z in loop2d(0, 0, *buildRect.size):
        # check up to 5 blocks below the heightmap
        for dy in range(5):
            # calculate absolute coordinates
            y = int(heightMap[(x, z)]) - dy

            blockID = worldSlice.getBlockAt(x, y, z)
            if blockID in lookup.MAPTRANSPARENT:
                # transparent blocks are ignored
                continue
            else:
                if blockID not in palette:
                    # unknown blocks remembered for debug purposes
                    unknownBlocks.add(blockID)
                else:
                    topcolor[(x, z)] = palette[blockID]
                break

    if len(unknownBlocks) > 0:
        print("Unknown blocks: " + str(unknownBlocks))

    # separate the color map into three separate color channels
    topcolor = cv2.merge(((topcolor) & 0xff, (topcolor >> 8) & 0xff, (topcolor >> 16) & 0xff))

    # calculate a brightness value from the gradient
    brightness = np.expand_dims((gradientX + gradientY).astype("int"), 2)
    brightness = brightness.clip(-64, 64)

    topcolor += brightness
    topcolor = topcolor.clip(0, 256)

    # display the map
    topcolor = topcolor.astype('uint8')
    topcolor = np.transpose(topcolor, (1, 0, 2))
    plt_image = cv2.cvtColor(topcolor, cv2.COLOR_BGR2RGB)

    plt.imshow(plt_image)
    plt.show()


if __name__ == "__main__":
    main()
