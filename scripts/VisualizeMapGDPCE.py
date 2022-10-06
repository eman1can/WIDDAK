"""
    A GDPCE Version of the VisualizeMap.py from GDCP
"""

__author__    = "Ethan Wolfe"
__copyright__ = "Copyright 2022, Ethan Wolfe"
__licence__   = "MIT"

import cv2

import numpy as np

from glm import ivec2

from os import mkdir
from os.path import exists, join

from PIL import Image as PILImage
from gdpc_source.gdpc import lookup
from gdpc_source.gdpc.toolbox import loop2d
from gdpc_source.gdpc.worldLoader import WorldSlice

from gdpce.interface import getWorldSlice
from gdpce.geometry import Rect

from gdpceu.renderer import Renderer
from gdpceu.world_loader import SavedWorldSlice, World, WorldSlice

renderer = Renderer()
renderer.set_default_viewer()

# template = [
#     [
#         [None, 'minecraft:oak_trapdoor', 'minecraft:oak_trapdoor', 'minecraft:oak_trapdoor', None],
#         ['minecraft:oak_trapdoor', 'minecraft:grass_block', 'minecraft:grass_block', 'minecraft:grass_block', 'minecraft:oak_trapdoor'],
#         [None, 'minecraft:oak_trapdoor', 'minecraft:oak_trapdoor', 'minecraft:oak_trapdoor', None]
#     ],
#     [
#         [None, None, None, None, None],
#         [None, 'minecraft:poppy', 'minecraft:oxeye_daisy', 'minecraft:dandelion', None],
#         [None, None, None, None, None]
#     ]
# ]
#
# renderer.make_3d_template_render(template).show_3d_render()

#
# rect = Rect(ivec2(-2048, -2048), ivec2(64, 256))
#
# with open(join('worlds', 'TestWorld1764', 'saved', f'{-2048}_{-2048}_{512}.chunk'), 'rb') as chunk_file:
#     byte_data = chunk_file.read()
# slice = SavedWorldSlice(byte_data, -2048, -2048, -1536, -1536)
#
# renderer.make_3d_render(rect, slice, fill_mode='am')
# renderer.save_3d_render()
# renderer.show_3d_render()
#
# exit(0)
# Load Saved Worlds
for world in ['TestWorld1764.dat', 'TestWorld1765.dat', 'TestWorld1766.dat', 'TestWorld1767.dat']:
    test_world = World(join('worlds', world))
    rect = Rect(ivec2(-2048, -2048), ivec2(256, 256))
    world_slice = test_world.getWorldSlice(rect)
    #
    # renderer.make_2d_render(rect, world_slice)
    # renderer.save_2d_render().show_2d_render()

    renderer.make_3d_render(rect, world_slice, fill_mode='rm').show_3d_render()
    # renderer.save_3d_render()
    break

# Load build area from Main World


exit(0)


class PickledWorldSlice(WorldSlice):
    def __init__(self, byte_data, x1, z1, x2, z2):
        self.rect = x1, z1, x2 - x1, z2 - z1
        self.chunkRect = (x1 // 16, z1 // 16, (x2 - x1 - 1) // 16 + 1, (z2 - z1 - 1) // 16 + 1)
        self.heightmapTypes = ["MOTION_BLOCKING",
                              "MOTION_BLOCKING_NO_LEAVES",
                              "OCEAN_FLOOR",
                              "WORLD_SURFACE"]
        self.byte_data = byte_data
        self._load_slice()


def MakeMapOfWorldSlice(rect, slice):
    heightMap = np.array(slice.heightmaps["OCEAN_FLOOR"][:-1, :-1], dtype=int)

    # calculate the gradient (steepness)
    decrementor = np.vectorize(lambda a: a - 1)
    cvheightmap = np.clip(decrementor(heightMap), 0, 255).astype(np.uint8)
    gradientX = cv2.Scharr(cvheightmap, cv2.CV_16S, 1, 0)
    gradientY = cv2.Scharr(cvheightmap, cv2.CV_16S, 0, 1)

    # create a dictionary mapping block ids ("minecraft:...") to colors
    palette = lookup.PALETTELOOKUP

    # create a 2d map containing the surface block colors
    topcolor = np.zeros(rect.size, dtype='int')
    unknownBlocks = set()
    xo, zo = rect.offset
    xr, zr = rect.size
    for x, z in loop2d(0, 0, xr - 1, zr - 1):
        # check up to 5 blocks below the heightmap
        for dy in range(5):
            # calculate absolute coordinates
            y = int(heightMap[(x, z)]) - dy
            try:
                blockID = slice.getBlockAt(xo + x, y, zo + z)
            except IndexError:
                raise IndexError(f'Failed on Index {x} {y} {z}')
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
    topcolor = cv2.merge((topcolor & 0xff, (topcolor >> 8) & 0xff, (topcolor >> 16) & 0xff))

    # calculate a brightness value from the gradient
    brightness = np.expand_dims((gradientX + gradientY).astype("int"), 2).clip(-64, 64)
    topographic = np.array(topcolor, copy=True) + brightness
    topcolor = np.transpose(topcolor.clip(0, 256).astype('uint8'), (1, 0, 2))
    topographic = np.transpose(topographic.clip(0, 256).astype('uint8'), (1, 0, 2))

    return topcolor, topographic


def main():
    print('Getting The World Slice')
    # Get the build area

    step = 512  # Don't change this to use saved chunks
    x1, z1, x2, z2 = 0, 0, 8192, 8192

    def combine_images(first, second, axis):
        if first is None:
            return second
        return np.concatenate((first, second), axis=axis)

    world_name = "TestWorld"
    if not exists(f'worlds/{world_name}'):
        mkdir(f'worlds/{world_name}')

    full_image = None
    full_topographic_image = None
    print(f'{0:5} - {0:5}', end='')
    for x in range(x1, x2, step):
        row_image = None
        row_topographic_image = None
        for z in range(z1, z2, step):
            print('\b' * 13, end='')
            print(f'{x:5} - {z:5}', end='')
            rect = Rect(ivec2(z, x), ivec2(step, step))
            slice_name = f'worlds/{world_name}/{x}_{z}_{step}.chunk'
            if exists(slice_name):
                with open(slice_name, 'rb') as data:
                    byte_data = data.read()
                    slice = PickledWorldSlice(byte_data, rect.begin[0], rect.begin[1], rect.end[0], rect.end[1])
            else:
                slice = getWorldSlice(rect)
                with open(slice_name, 'wb') as data:
                    data.write(slice.byte_data)
            slice_image, slice_topographic_image = MakeMapOfWorldSlice(rect, slice)
            row_image = combine_images(row_image, slice_image, 1)
            row_topographic_image = combine_images(row_topographic_image, slice_topographic_image, 1)
        full_image = combine_images(full_image, row_image, 0)
        full_topographic_image = combine_images(full_topographic_image, row_topographic_image, 0)
    print('\b' * 13, end='')
    print(f'{x2:5} - {z2:5}', end='')

    def show_image(image_data):
        raw_image = PILImage.fromarray(image_data)
        b, g, r = raw_image.split()
        image = PILImage.merge('RGB', (r, g, b))
        return image

    color_image = show_image(full_image)
    topographic_image = show_image(full_topographic_image)
    color_image.save(f'{world_name}_render.tif')
    topographic_image.save(f'{world_name}_topographic_render.tif')
    # duration = time() - start
    # print(f'It Took {duration} seconds to get all world slices')


if __name__ == "__main__":
    main()
