from math import ceil
from os import listdir
from time import time
from typing import Union

import amulet
import amulet.utils.world_utils as world_utils
import numpy as np
from amulet.api.errors import ChunkLoadError, ChunkDoesNotExist
from glm import ivec3

from gdpc.lookup import BIOMES, BIOMES_NAME_TO_INDEX
from gdpc.vector_util import Box, Rect
from amulet.api.level import World, Structure
from gdpc.worldLoader import WorldSlice as BaseWorldSlice


class WorldSlice(BaseWorldSlice):
    def __init__(self, file_path, rect):
        if 'level.dat' not in listdir(file_path):
            raise AttributeError('The path you specified is not a Minecraft world!')
        super().__init__()
        self._amulet_handle: Union[World, Structure] = amulet.load_level(file_path)
        self.load(None, rect)

    def __del__(self):
        self._amulet_handle.close()

    def load(self, world_data: None, rect: Rect):
        """
        Load data from amulet into local arrays
        """

        dimension = 'minecraft:overworld'
        self.rect = rect
        self.chunk_rect = rect // 16

        self.biomes = np.zeros((int(ceil(self.rect.dx / 4)), int(ceil(self.rect.dz / 4)), 64), dtype=np.uint8)

        heightmaps = self._amulet_handle.get_chunk(0, 0, dimension).misc['height_mapC']
        self.heightmap_types = list(heightmaps.keys())

        self.heightmaps = np.zeros((len(self.heightmap_types), self.rect.dx, self.rect.dz), dtype=np.uint16)

        chunk_count = int(ceil(rect.area / (16 * 16)))
        print(f'\nReading and Unpacking Chunk Data')
        start_time = time()

        cix = 0
        for x, z in self.chunk_rect.loop():
            try:
                chunk = self._amulet_handle.get_chunk(x, z, dimension)
            except ChunkDoesNotExist:
                raise Exception('Failed to load chunk in world!')
            except ChunkLoadError:
                raise Exception('World File is corrupted')

            if chunk.status.value != 2.0:
                raise Exception('World not fully loaded!')

            # Copy Biomes - TODO: Check for Biome Dimension
            for brx, bry, brz in Box.from_box(0, 0, 0, 4, 64, 4).loop():
                biome_index = chunk.biomes[brx, bry, brz]  # Get the 4, 4, 4 numpy array of biomes
                biome_name = chunk.biome_palette[biome_index][len('universal_minecraft:'):]
                # print(x + brx, z + brz, bry, biome_name)
                self.biomes[x * 4 + brx, z * 4 + brz, bry] = BIOMES_NAME_TO_INDEX[biome_name]

            # Copy heightmaps
            hx, hz = x * 16, z * 16
            for hix, heightmap in enumerate(chunk.misc['height_mapC'].values()):
                self.heightmaps[hix, hz:hz + 16, hx:hx+16] = heightmap - 1

            if cix & 10 == 0:
                self._amulet_handle.unload()

            if cix != 0:
                print('\b' * 49, end='')
            print(f'{cix + 1:10} / {chunk_count:10} {round((cix + 1) / chunk_count * 100, 2):10}% - {round(time() - start_time, 2):10}s', end='')
            cix += 1
        print(f'\nDone - {time() - start_time}')

    def get_relative_block_id_at(self, p: ivec3) -> str:
        gp = self.to_global(p)
        block = self._amulet_handle.get_block(gp.z, gp.y, gp.x, 'minecraft:overworld')
        name = self.universal_to_java(block.base_name, block.properties)
        self._amulet_handle.unload()
        return name

    def universal_to_java(self, base_name: str, properties: dict) -> str:
        if 'plant_type' in properties:
            base_name = properties['plant_type']
        if base_name == 'infested_block':
            base_name = 'infested_' + properties['material']
        elif 'material' in properties:
            base_name = properties['material'] + '_' + base_name
        if base_name in ('crimson_log', 'warped_log'):
            base_name = base_name[:-3] + 'stem'
        if base_name == 'wool':
            base_name = properties['color'] + '_wool'
        if base_name == 'stained_terracotta':
            base_name = properties['color'] + '_terracotta'
        if base_name == 'glazed_terracotta':
            base_name = properties['color'] + '_glazed_terracotta'
        if base_name in ('wall_banner',):
            print(base_name, properties)
        return f'minecraft:{base_name}'
