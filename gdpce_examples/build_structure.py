#!/usr/bin/env python3

""" Executable script that build an example structure in the center of the build area.

    The purpose of this file is to demonstrate the usage of the core GDPC 5.0 enhancements provided
    by this repository. It does not demonstrate every enhancement, and it assumes some familiarity
    with the base GDPC framework.

    The following enhancements are demonstrated:
    - Vectors and various vector math utilities.
    - The Transform class and the use of local coordinate systems.
    - The placement of blocks with NBT data.
    - The placement of saved models.

    To install or learn more about the base GDPC framework, visit
    https://github.com/nilsgawlik/gdmc_http_client_python
"""

__author__    = "Arthur van der Staaij"
__copyright__ = "Copyright 2022, Arthur van der Staaij"
__licence__   = "MIT"

import sys
sys.path.append('/Users/emilygavrilenko/Coding/WIDDAK/')

import numpy as np
from glm import ivec2, ivec3, bvec3
from gdpce.util import eprint

from gdpce.vector_util import addY, vecString, Rect, Box, centeredSubRect, rectSlice
from gdpce.transform import Transform, rotatedBoxTransform, scaledBoxTransform, flippedBoxTransform
from gdpce.nbt_util import signNBT
from gdpce.block import Block
from gdpce.interface import Interface, getBuildArea, getWorldSlice
from gdpce.geometry import placeBox, placeRectOutline, placeCheckeredBox
import json


CLEAR_AREA_RADIUS = 30
CLEAR_AREA = ivec2(CLEAR_AREA_RADIUS, CLEAR_AREA_RADIUS)

# Build a structure in the world
def buildStructure(itf: Interface, structure: list, should_clear: True):
    # print(structure)

    # Clear the area
    if (should_clear):
        for i in range(CLEAR_AREA_RADIUS):
            for j in range(CLEAR_AREA_RADIUS):
                for k in range(CLEAR_AREA_RADIUS):
                    itf.placeBlock(ivec3(i - CLEAR_AREA_RADIUS/2, j - CLEAR_AREA_RADIUS/2, k - CLEAR_AREA_RADIUS/2), Block("air"))

    # Build the structure
    for y in range(len(structure)):
        for x in range(len(structure[y])):
            for z in range(len(structure[y][x])):
                if structure[y][x][z] != None:
                    block = structure[y][x][z]
                    block = block.replace('dirt_path', 'grass_path')
                    itf.placeBlock(ivec3(x, y, z), Block(block))

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
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

    # Create an Interface object with a transform that translates to the build rect
    itf = Interface(addY(buildRect.offset))

    # Place build area indicator
    meanHeight = int(np.mean(heightmap))
    placeRectOutline(itf, Rect(size=buildRect.size), meanHeight + 20, Block("red_concrete"))

    # Build the example structure in the center of the build area, at the mean height.
    rect = centeredSubRect(Rect(size=buildRect.size), CLEAR_AREA)
    height = int(np.mean(rectSlice(heightmap, rect))) - 1

    # Load a blueprint template
    f = open(f'blueprints/building_templates.json')
    building_templates = json.load(f)
    template_name = 'Plains_meeting_point_3_blueprint'

    # Build the structure 
    with itf.pushTransform(addY(rect.offset, height)):
        buildStructure(itf, building_templates.get(template_name), should_clear=True)

    # Flush block buffer
    itf.sendBufferedBlocks()


if __name__ == "__main__":
    main()
