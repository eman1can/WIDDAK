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
from os import getcwd, environ, chdir, listdir, makedirs
from os.path import split, join, exists
import sys

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
from gdpc.vox_lookup import HEX_TO_MINECRAFT

from src.vox import VoxFile

CLEAR_AREA_RADIUS = 30
CLEAR_AREA = ivec2(CLEAR_AREA_RADIUS, CLEAR_AREA_RADIUS)

def visualize_vox_template(template_path, location=None):
    # Get the build area
    buildArea = getBuildArea()
    print("Build area: " + vecString(buildArea))
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

    # Load a blueprint template
    f = open(template_path)
    template = json.load(f)
    print(height)

    # Set the center of the template build area
    if (location):
        center = addY(ivec2(location[0], location[2]), location[1]) 
    else :
        center = addY(ivec2(0, 0), 120)
    print(center)

    # Changed to max height instead of clear area
    with itf.pushTransform(center):
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


def convert_to_minecraft_blocks(vox_file):

    for model in vox_file.get_models():
        template = []
        for i in range(len(model)):
            layer = []
            for j in range(len(model[i])):
                row = []
                for k in range(len(model[i][j])):
                    if model[i][j][k] != 0:
                        minecraft_palette_index = model[i][j][k] - 1
                        color = hex(vox_file.get_color_for_index(minecraft_palette_index))
                        hex_color = '#' + color.split('x')[1].zfill(6) 
                        minecraft_block = HEX_TO_MINECRAFT.get(hex_color)
                        if minecraft_block is None:
                            minecraft_block = list(HEX_TO_MINECRAFT.values())[minecraft_palette_index]
                        row.append(minecraft_block)
                    else:
                        row.append(None)
                layer.append(row)
            template.append(layer)
        return template
    

def create_template_from_vox(vox_filepath):
    # Read in the VOX file
    vox_file = VoxFile(vox_filepath)
    vox_file.read()
    vox_file.close()

    # Convert the VOX file to a minecraft template
    minecraft_template = convert_to_minecraft_blocks(vox_file)

    # Save the template
    file_name = vox_filepath.split('/')[-1].split('.')[0] + '.json'
    path = 'examples/vox_templates/' + file_name
    with open(path, "w") as file:
        json_string = json.dumps(minecraft_template)
        file.write(json_string)
    return path


filepath1 = 'MarkovJunior/resources/rules/ModernHouseMOD2/ModernHouseMOD1_73618823.vox'
filepath2 = 'sections/MarkovJunior/output/EthanTree_1136010046.vox'
filepath3 = 'MarkovJunior/resources/Apartemazements_722238551.vox'
template_path = create_template_from_vox(filepath3)
location = [0, 0, 200]
visualize_vox_template(template_path, location)
