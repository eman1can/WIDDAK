from fix_file_path import *
from glm import ivec2, ivec3
from amulet.api.block import Block
from gdpc.vector_util import addY, vecString
from gdpc.util import eprint
from gdpc.interface import getBuildArea, getWorldSlice
from gdpc.template import Template
from src.vox import VoxFile
from gdpc.direct_interface import place_block_at, place_blocks

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
    place_block_at(air, ivec3(0, 0, 0), to_replace)


def visualize_vox_template(template, location=None):
    # Get the build area
    buildArea = getBuildArea()
    buildRect = buildArea.toRect()

    # Check whether the build area is large enough
    if any(buildRect.size < CLEAR_AREA):
        eprint(f"The build area rectangle is too small! Its size needs to be at least {vecString(CLEAR_AREA)}")
        sys.exit(1)

    # Set the center of the template build area
    if (location):
        center = addY(ivec2(location[0], location[2]), location[1]) 
    else:
        center = addY(ivec2(0, 0), 120)
    print(center)

    blocks = []
    for ix, iy, iz, relation, block in template.loop():
        blocks.append((block, ivec3(ix, iy, iz)))
        if len(blocks) > 100:
            place_blocks(blocks, ivec3(buildArea.x1, buildArea.y1, buildArea.z1))
            blocks = []
    place_blocks(blocks, ivec3(buildArea.x1, buildArea.y1, buildArea.z1))

def create_template_from_vox(vox_filepath, name, key, biome='forest'):
    # Read in the VOX file
    vox = VoxFile.from_file(vox_filepath)
    # Make the Template
    template = Template.from_vox_model(name, vox.get_model(), vox.get_color_palette(), key, biome)
    return template