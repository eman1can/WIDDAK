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

from gdpc.direct_interface import place_block, place_block_at, place_blocks

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

from amulet.api.block import Block
from gdpc.vector_util import addY, vecString, Rect, centeredSubRect, rectSlice
from gdpc.util import eprint
from gdpc.interface import Interface, getBuildArea, getWorldSlice
from gdpc.template import Template
import json
from gdpc.vox_lookup import HEX_TO_MINECRAFT, VOX_TO_MINECRAFT

from src.vox import VoxFile

CLEAR_AREA_RADIUS = 30
CLEAR_AREA = ivec2(CLEAR_AREA_RADIUS, CLEAR_AREA_RADIUS)


def clear_build_area():
    build_area = getBuildArea()
    world_slice = getWorldSlice(build_area.toRect())

    air = Block('minecraft', 'air')
    to_replace = []
    for p in build_area.loop():
        block = world_slice.get_block_data_at(p)
        if block.base_name != 'air':
            to_replace.append(p)
            # place_block(air, p)
            # print(*p, block.base_name)
    # print(to_replace)
    place_block_at(air, ivec3(0, 0, 0), to_replace)


def visualize_vox_template(template, location=None):
    # Get the build area
    buildArea = getBuildArea()
    buildRect = buildArea.toRect()
    print("Build area: " + str(buildArea))

    # Check whether the build area is large enough
    if any(buildRect.size < CLEAR_AREA):
        eprint(f"The build area rectangle is too small! Its size needs to be at least {vecString(CLEAR_AREA)}")
        sys.exit(1)

    # Get a world slice and a heightmap
    world_slice = getWorldSlice(buildRect)
    heightmap = world_slice.get_heightmap("WORLD_SURFACE")

    # Create an Interface object with a transform that translates to the build rect
    # itf = Interface(addY(buildRect.offset))

    # Place build area indicator
    max_height = int(np.max(heightmap))
    # placeRect(buildRect, maxHeight + 10, Block('minecraft', 'orange_concrete'), width=1, itf=itf)

    # Build the example structure in the center of the build area, at the mean height.
    rect = centeredSubRect(buildRect, CLEAR_AREA)
    height = int(np.max(rectSlice(heightmap, Rect(size=rect.size)))) - 1

    # Set the center of the template build area
    if (location):
        center = addY(ivec2(location[0], location[2]), location[1]) 
    else:
        center = addY(ivec2(0, 0), 120)
    print(center)

    # Changed to max height instead of clear area
    # with itf.pushTransform(center):

    blocks = []
    for ix, iy, iz, relation, block in template.loop():
        blocks.append((block, ivec3(ix, iy, iz)))
        if len(blocks) > 100:
            place_blocks(blocks, ivec3(buildArea.x1, buildArea.y1, buildArea.z1))
            blocks = []
    place_blocks(blocks, ivec3(buildArea.x1, buildArea.y1, buildArea.z1))
    # Flush block buffer
    # itf.sendBufferedBlocks()
    # itf.awaitBufferFlushes()

# Convert VOX file colors to match colors in palette.xml
def convert_to_hexcolor(orig_color):
    color = hex(int(orig_color))
    color = color.split('x')[1].zfill(6) 
    color = color[4:6] + color[2:4] + color[0:2]
    hex_color = '#' + color
    return hex_color

# Return the minecraft block for the given hex color
# Return bedrock if no match is found
def get_minecraft_block(hex_color, biome):
    biome_blocks = VOX_TO_MINECRAFT.get(hex_color)
    if biome_blocks and biome_blocks.get(biome):
        return biome_blocks.get(biome)
    minecraft_block = HEX_TO_MINECRAFT.get(hex_color)
    if minecraft_block:
        return minecraft_block
    return 'minecraft:bedrock'


def convert_to_minecraft_blocks(vox_file, biome):
    all_colors = set()

    for model in vox_file.get_models():
        template = []
        for i in range(len(model)):
            layer = []
            for j in range(len(model[i])):
                row = []
                for k in range(len(model[i][j])):
                    if model[i][j][k] != 0:
                        minecraft_palette_index = model[i][j][k] 
                        hex_color = convert_to_hexcolor(vox_file.get_color_for_index(minecraft_palette_index))
                        minecraft_block = get_minecraft_block(hex_color, biome)
                        row.append(minecraft_block)
                        all_colors.add(hex_color)
                    else:
                        row.append(None)
                layer.append(row)
            template.append(layer)
        print(all_colors)
        return template
    

def create_template_from_vox(vox_filepath, name, key, biome='forest'):
    # Read in the VOX file
    vox = VoxFile.from_file(vox_filepath)
    # Make the Template
    template = Template.from_vox_model(name, vox.get_model(), vox.get_color_palette(), key, biome)
    return template


filepath1 = 'MarkovJunior/resources/rules/ModernHouseMOD2/ModernHouseMOD1_73618823.vox'
filepath2 = 'sections/MarkovJunior/output/EthanTree_1136010046.vox'
filepath3 = 'MarkovJunior/resources/Apartemazements_722238551.vox'
filepath4 = 'MarkovJunior/resources/TreeV2_2120272460.vox'

# template_path = create_template_from_vox(filepath4, 'forest')
# location = [100, 130, 80]
# visualize_vox_template(template_path, location)

# template_path = create_template_from_vox(filepath4, 'taiga')
# location = [90, 130, 80]
# visualize_vox_template(template_path, location)

# template_path = create_template_from_vox(filepath4, 'birch_forest')
# location = [80, 130, 80]
# visualize_vox_template(template_path, location)


clear_build_area()
template = create_template_from_vox(filepath1, 'Modern House', 'modern_house', 'jungle')
location = [70, 130, 70]
visualize_vox_template(template, location)

