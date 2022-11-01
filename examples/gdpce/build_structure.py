"""
Executable script that build an example structure in the center of the build area.

The purpose of this file is to demonstrate the usage of the core GDPC 5.0 enhancements provided
by this repository. It does not demonstrate every enhancement, and it assumes some familiarity
with the base GDPC framework.

The following enhancements are demonstrated:
- Vectors and various vector math utilities.
- The Transform class and the use of local coordinate systems.
- The placement of blocks with NBT data.
- The placement of saved models.

"""

__author__    = "Arthur van der Staaij"
__copyright__ = "Copyright 2022, Arthur van der Staaij"
__licence__   = "MIT"

# Path Fixing Code - Must Be First
import sys
from os import getcwd, environ, chdir
from os.path import split

script_path = getcwd()
sys.path.append(script_path)
while not script_path.endswith('WIDDAK'):
    script_path = split(script_path)[0]
    chdir(script_path)
if 'PYTHONPATH' in environ:
    if script_path + ';' not in environ['PYTHONPATH']:
        environ['PYTHONPATH'] += script_path + ';'
else:
    environ['PYTHONPATH'] = script_path
# End Path Fixing Code

import numpy as np
from glm import ivec2, ivec3, bvec3

from gdpc.vector_util import addY, vecString, Rect, centeredSubRect, rectSlice
from gdpc.util import eprint
from gdpc.block import Block
from gdpc.interface import Interface, getBuildArea, getWorldSlice
from gdpc.geometry import placeRect
import json


CLEAR_AREA_RADIUS = 30
CLEAR_AREA = ivec2(CLEAR_AREA_RADIUS, CLEAR_AREA_RADIUS)

def main():
    # Get the build area
    buildArea = getBuildArea()
    buildRect = buildArea.toRect()

    # Check whether the build area is large enough
    if any(buildRect.size < CLEAR_AREA):
        eprint(f"The build area rectangle is too small! Its size needs to be at least {vecString(CLEAR_AREA)}")
        sys.exit(1)

    # Get a world slice and a heightmap
    worldSlice = getWorldSlice(buildRect)
    heightmap = worldSlice.get_heightmap("WORLD_SURFACE")

    # Create an Interface object with a transform that translates to the build rect
    itf = Interface(addY(buildRect.offset))

    # Place build area indicator
    maxHeight = int(np.max(heightmap))
    placeRect(buildRect, maxHeight + 10, Block("orange_concrete"), width=1, itf=itf)

    # Build the example structure in the center of the build area, at the mean height.
    rect = centeredSubRect(buildRect, CLEAR_AREA)
    height = int(np.max(rectSlice(heightmap, Rect(size=rect.size)))) - 1

    # # Load a blueprint template
    f = open(f'sections/blueprints/building_templates.json')
    building_templates = json.load(f)
    template = building_templates["1"]["Meeting Point"]["3"]

    # Changed to max height instead of clear area
    with itf.pushTransform(addY(ivec2(0, 0), height)):
        for iy, y in enumerate(template):
            for iz, z in enumerate(y):
                for ix, block in enumerate(z):
                    if block is None:
                        continue
                    block = block.replace('dirt_path', 'grass_path')
                    itf.place(Block(block), ivec3(ix, iy, iz), local=True)

    # Flush block buffer
    itf.sendBufferedBlocks()
    itf.awaitBufferFlushes()


if __name__ == "__main__":
    main()
