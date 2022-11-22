"""### Provides tools for reading chunk data.

This module contains functions to:
* Calculate a heightmap ideal for building
* Visualise numpy arrays
"""
__all__ = ['WorldSlice']
__version__ = "v5.1"

from amulet.api.block import Block, StringTag
from io import BytesIO
from os.path import join, split
from time import time
from typing import Optional

import numpy as np
from glm import ivec2, ivec3
from numpy import ceil, log2

from . import direct_interface as di
from .bitarray import BitConverter
from .vector_util import Rect
from .lookup import VERSIONS, SUPPORTS, TCOLORS
from .nbt import NBTFile


class CachedSection:
    """**Represents a cached chunk section (16x16x16)**."""

    def __init__(self, palette, blockStatesBitArray):
        self.palette = palette
        self.blockStatesBitArray = blockStatesBitArray

    # __repr__ displays the class well enough so __str__ is omitted
    def __repr__(self):
        return f"CachedSection({repr(self.palette)}, " \
            f"{repr(self.blockStatesBitArray)})"


DEFAULT_HEIGHTMAP_TYPES = ["MOTION_BLOCKING", "MOTION_BLOCKING_NO_LEAVES", "OCEAN_FLOOR", "WORLD_SURFACE"]


class WorldData:
    def __init__(self, rect: Rect, nbt_data):
        self.rect = rect
        self.nbt_data = nbt_data

    def __add__(self, other):
        nbt_data = self.nbt_data + other.nbt_data
        rect = Rect.from_rect(nbt_data.chunkX.value, nbt_data.chunkZ.value, nbt_data.chunkDX.value, nbt_data.chunkDZ.value)
        return WorldData(rect, nbt_data)

    def get_sub_section(self, rect):
        cx, cz, cdx, cdz = rect.tuple

        # Compound Tag('file') {List Tag('Chunks'): [], Int Tag('ChunkX'): 0, Int Tag('ChunkZ'): 0, Int Tag('ChunkDX'): 0, Int Tag('ChunkDZ'): 0}
        byte_data = b'\x0A\x00\x04\x66\x69\x6C\x65\x09\x00\x06\x43\x68\x75\x6E\x6B\x73\x0A\x00\x00\x00\x00\x03\x00\x06\x43\x68\x75\x6E\x6B\x5A\x00\x00\x00\x00\x03\x00\x07\x43\x68\x75\x6E\x6B\x44\x58\x00\x00\x00\x00\x03\x00\x06\x43\x68\x75\x6E\x6B\x58\x00\x00\x00\x00\x03\x00\x07\x43\x68\x75\x6E\x6B\x44\x5A\x00\x00\x00\x00\x00'
        nbt_file = NBTFile(buffer=BytesIO(byte_data))
        nbt_file.chunkX.value = cx
        nbt_file.chunkZ.value = cz
        nbt_file.chunkDX.value = cdx
        nbt_file.chunkDZ.value = cdz

        for chunk in self.nbt_data.chunks.tags:
            if not (cx <= chunk['Level']['xPos'].value < cx + cdx):
                continue
            if not (cz <= chunk['Level']['zPos'].value < cz + cdz):
                continue
            nbt_file.chunks.append(chunk)
        return WorldData(rect, nbt_file)

    @staticmethod
    def load_from_file(file_name, rect):
        if not file_name.endswith('chunk'):
            raise TypeError('Invalid File. Must be a CHUNK file')
        # with open(file_name, 'rb') as file:  # TODO: Change to GzipFile Using NBTFile
        #     header_bytes = file.read(3)
        #     if header_bytes != b'\x1F\x8B\x08':
        #         raise TypeError('This is not a CHUNK file!')
        #     byte_data = header_bytes + file.read()
        nbt_data = NBTFile(filename=file_name)
        return WorldData(rect, nbt_data)

    @staticmethod
    def load_from_server(chunk_rect):
        byte_data = di.getChunks(chunk_rect, rtype='bytes')
        nbt_data = NBTFile(buffer=BytesIO(byte_data))
        return WorldData(chunk_rect, nbt_data)

    def to_file(self, file_name):
        self.nbt_data.write_file(file_name)


class WorldSlice:
    """**Contains information on a slice of the world**."""
    def __init__(self):
        self.heightmap_types = DEFAULT_HEIGHTMAP_TYPES
        self.rect: Rect = Rect.from_rect(0, 0, 0, 0)
        self.chunk_rect: Rect = Rect.from_rect(0, 0, 0, 0)
        self.world_name: Optional[str] = None
        self.step: Optional[int] = None

        self.chunks = None
        self.chunk_palettes = None
        self.biomes = None
        self.heightmaps: Optional[np.ndarray] = None
        self.data_version = None

        self.saved_data = None

    def to_local(self, point: ivec3):
        """ Transform a given point from global coordinates to coordinates local to this world slice"""
        return point - ivec3(self.rect.x1, 0, self.rect.z1)

    def to_global(self, point: ivec3):
        """ Transform a given point from local coordinates to global coordinates """
        return ivec3(self.rect.x1, 0, self.rect.z1) + point

    @staticmethod
    def from_file(file_path, rect=None):
        """
        Load this slice from a file saved by the to_file function
        """
        if not file_path.endswith('dat'):
            raise TypeError('Invalid File. Must be a DAT file')
        print('Reading Slice Info')
        try:
            with open(file_path, 'r') as file:
                world_name, step, x1, z1, x2, z2 = file.read().split(',')
                step, x1, z1, x2, z2 = int(step), int(x1), int(z1), int(x2), int(z2)
        except ValueError:
            raise TypeError('Invalid File. This is not a DAT file')

        print('Calculating Slice Parameters')
        if rect is None:
            rect = Rect.from_corners(x1, z1, x2, z2)
        else:
            if rect.x1 < x1 or rect.z1 < z1 or rect.x2 > x2 or rect.z2 > z2:
                raise ValueError('Passed rect is outside bounds of world!')

        path, dat_file = split(file_path)

        ret = WorldSlice()
        ret.world_name = world_name
        ret.step = step

        chunk_rect = rect // 16
        saved_rect = chunk_rect * 16 // step * step
        chunk_count = saved_rect.area // (step * step)

        print(f'Loading Slice Chunks (0 / {chunk_count})...')
        start_time = time()
        if step == saved_rect.dx and step == saved_rect.dz:
            # The world slice is from one chunk
            world_data = WorldData.load_from_file(join(path, world_name, 'saved', f'{saved_rect.x1}_{saved_rect.z1}_{step}.chunk'), rect)
            print(f'Done')
            subset = world_data.get_sub_section(chunk_rect)
        else:
            full_world_data = None
            for ix, (sx, sz) in enumerate(saved_rect.loop(ivec2(step, step))):
                world_data = WorldData.load_from_file(join(path, world_name, 'saved', f'{sx}_{sz}_{step}.chunk'), rect)
                full_world_data = world_data if full_world_data is None else (full_world_data + world_data)
                if ix > 0:
                    print('\b' * 48, end='')
                print(f'{ix + 1:10} / {chunk_count:10} {round((ix + 1) / chunk_count, 2):10}% - {round(time() - start_time, 2):10}', end='')
            print(f'\nDone - {time() - start_time}')
            subset = full_world_data.get_sub_section(chunk_rect)
        ret.load(subset, rect)
        return ret

    @staticmethod
    def from_server(rect: Rect, save_data=False, step=8):
        """
        Query the server for this world slice
        """
        ret = WorldSlice()

        chunk_rect = rect // 16
        step = min(step, chunk_rect.dx // 2, chunk_rect.dz // 2)
        chunk_count = int(ceil(chunk_rect.area / (step * step)))
        start_time = time()
        print(f'Loading Slice Chunks (0 / {chunk_count})...')
        full_world_data = None
        for ix, (sx, sz) in enumerate(chunk_rect.loop(ivec2(step, step))):
            world_data = WorldData.load_from_server(Rect.from_rect(sx, sz, step, step))
            full_world_data = world_data if full_world_data is None else (full_world_data + world_data)
            if ix > 0:
                print('\b' * 49, end='')
            print(f'{ix + 1:10} / {chunk_count:10} {round((ix + 1) / chunk_count * 100, 2):10}% - {round(time() - start_time, 2):10}s', end='')
        print(f'Done - {time() - start_time}')
        subset = full_world_data.get_sub_section(chunk_rect)
        ret.load(subset, rect)
        if save_data:
            ret.saved_data = full_world_data
        return ret

    # def to_file(self, world_name, minecraft_world_name, save_path, step):
    #     save_location = join(get_minecraft_location(), 'saves')
    #
    #     if not exists(join(save_location, minecraft_world_name)):
    #         print('That minecraft world does not exist!\nYou\'ll have to copy the world yourself', file=sys.stderr)
    #     if self.saved_data is None:
    #         raise ValueError('Please call from_server with save_data=True; This slice has no savable data')
    #     if step % 16 != 0:
    #         raise TypeError('Step should be divisible by 16!')
    #
    #     print('Saving World Slice')
    #
    #     world_folder = join(save_path, world_name)
    #     dat_file = join(save_path, world_name + '.dat')
    #     raw_folder = join(world_folder, 'raw')
    #     chunk_folder = join(world_folder, 'saved')
    #
    #     if not exists(world_folder):
    #         makedirs(world_folder)
    #     if not exists(chunk_folder):
    #         mkdir(chunk_folder)
    #     if not exists(raw_folder):
    #         mkdir(raw_folder)
    #
    #     if not exists(join(raw_folder, 'level.dat')):
    #         if exists(join(save_location, minecraft_world_name)):
    #             print('Copying Minecraft World...', end='')
    #             for file in listdir(join(save_location, minecraft_world_name)):
    #                 if file == 'session.lock':
    #                     continue
    #                 src = join(save_location, minecraft_world_name, file)
    #                 dst = join(raw_folder, file)
    #                 if isdir(src):
    #                     copytree(src, dst)
    #                 else:
    #                     copy(src, dst)
    #             print('Done')
    #     print('Saving Slice Info...', end='')
    #
    #     rect = self.chunk_rect * 16
    #     chunk_count = int(ceil(self.chunk_rect.area / (step * step)))
    #     cs = step // 16
    #
    #     file_data = ','.join([world_name, str(step), str(rect.x1), str(rect.z1), str(rect.x2), str(rect.z2)])
    #     with open(dat_file, 'a') as file:
    #         file.write(file_data)
    #     print('Done')
    #
    #     print(f'Saving Slice Chunks...')
    #     start_time = time()
    #     for ix, (cx, cz) in enumerate(self.chunk_rect.loop(ivec2(cs, cs))):
    #         sub_data = self.saved_data.get_sub_section(Rect.from_rect(cx, cz, cs, cs))
    #         sub_data.to_file(join(world_folder, 'saved', f'{cx}_{cz}_{step}.chunk'))
    #         if ix > 0:
    #             print('\b' * 45, end='')
    #         print(f'{ix + 1:10} / {chunk_count:10} {round((ix + 1) / chunk_count * 100, 2):6}% - {round(time() - start_time, 2):10}s', end='')
    #     print(f'\nDone - {time() - start_time}')

    def get_heightmap(self, heightmap_name: str) -> np.ndarray:
        hix = self.heightmap_types.index(heightmap_name)
        return self.heightmaps[hix]

    def load(self, world_data: WorldData, rect: Rect):
        """
        Load chunk data into local data arrays, unpacking compressed data
        https://wiki.vg/Chunk_Format
        """

        self.rect = world_data.rect * 16
        self.chunk_rect = world_data.rect

        self.chunks = np.zeros((self.rect.dx, self.rect.dz, 256), dtype=np.uint16)
        self.biomes = np.zeros((int(ceil(self.rect.dx / 4)), int(ceil(self.rect.dz / 4)), 64), dtype=np.uint8)
        self.chunk_palettes: list[list[list[Optional[list[Block]]]]] = [[[None for _ in range(16)] for _ in range(self.chunk_rect.dz)] for _ in range(self.chunk_rect.dx)]

        self.heightmap_types = list(world_data.nbt_data.chunks[0]['Level']['Heightmaps'].keys())
        self.data_version = world_data.nbt_data.chunks[0]['DataVersion'].value

        self.heightmaps = np.zeros((len(self.heightmap_types), self.rect.dx, self.rect.dz), dtype=np.uint16)
        heightmap_converter = BitConverter(9, 256)

        chunk_count = int(ceil(rect.area / (16 * 16)))
        print(f'\nReading and Unpacking Chunk Data')
        start_time = time()

        for cix, chunk in enumerate(world_data.nbt_data.chunks):
            level = chunk['Level']
            # Get the x and z pos of this chunk and convert to relative
            rcx = level['xPos'].value - self.chunk_rect.x1  # Chunk is 1 Indexed
            rcz = level['zPos'].value - self.chunk_rect.z1

            # if rcx < 0 or rcx >= self.chunk_rect.xl or rcz < 0 or rcz >= self.chunk_rect.zl:
            #     continue

            if level['Status'].value != 'full':
                raise Exception('Chunk was not loaded!')

            for rx in range(16):
                ax = rcx * 16 + rx
                brx = ax // 4
                for rz in range(16):
                    az = rcz * 16 + rz
                    brz = az // 4

                    # if ax >= rect.xl or az >= rect.zl:
                    #     continue

                    # Copy biome palette to per block data
                    for y in range(0, 64):
                        bix = y * 4 * 4 + rx // 4 * 4 + rz // 4
                        self.biomes[brx, brz, y] = level['Biomes'][bix]

                    # Convert the heightmap palette to heightmap value for each block
                    for hix, heightmap in enumerate(level['Heightmaps'].values()):
                        ix = rz * 16 + rx
                        self.heightmaps[hix, ax, az] = heightmap_converter.getAt(heightmap, ix) - 1
                    # Convert Sections
                    for section in level['Sections']:
                        cy = section['Y'].value

                        if 'BlockStates' not in section or len(section['BlockStates']) == 0:
                            continue
                        if self.chunk_palettes[rcx][rcz][cy] is None:
                            blocks = []
                            for block in section['Palette'].tags:
                                namespace, name = str(block['Name']).split(':')
                                properties = {}
                                if 'Properties' in block:
                                    for k, v in block['Properties'].items():
                                        properties[k] = StringTag(v)
                                blocks.append(Block(namespace, name, properties))
                            self.chunk_palettes[rcx][rcz][cy] = blocks
                        bits_per_entry = int(max(4, ceil(log2(len(section['Palette'].tags)))))
                        converter = BitConverter(bits_per_entry, 4096)
                        # Get Block Data
                        for y in range(16):
                            ci = y * 16 * 16 + rz * 16 + rx
                            self.chunks[ax, az, cy * 16 + y] = converter.getAt(section['BlockStates'], ci)
            if cix > 0:
                print('\b' * 49, end='')
            print(f'{cix + 1:10} / {chunk_count:10} {round((cix + 1) / chunk_count * 100, 2):10}% - {round(time() - start_time, 2):10}s', end='')
        print(f'\nDone - {time() - start_time}')

    def __repr__(self):
        return f"WorldSlice{(self.rect.x1, self.rect.z1, self.rect.x2, self.rect.z2)}"

    def _floor_div_p(self, p: ivec3, v: int):
        return ivec3(p.x // v, p.y // v, p.z // v)

    def _div_mod_p(self, p: ivec3, v: int):
        return ivec3(p.x % v, p.y % v, p.z % v)

    def _relative(self, p: ivec3) -> ivec3:
        """ Return relative indices for accessing data """
        return ivec3(p.x - self.rect.x1, p.y, p.z - self.rect.z1)

    def get_relative_block_data_at(self, rp: ivec3) -> Block:
        """ Return block data from relative coordinates"""
        # print(cx, cy, cz, x, y, z, len(self.chunk_palettes), len(self.chunk_palettes[0]))
        cp = self._floor_div_p(rp, 16)
        palette_index = self.chunks[rp.x, rp.z, rp.y]
        palette = self.chunk_palettes[cp.x][cp.z][cp.y]
        if palette is None:
            return Block('minecraft', 'air')
        if palette_index >= len(palette):
            print('IndexError', palette, palette_index)
            return Block('minecraft', 'air')
        return palette[palette_index]

    def get_block_data_at(self, p: ivec3) -> Block:
        """ Return block data """
        return self.get_relative_block_data_at(self._relative(p))

    def get_relative_block_id_at(self, p: ivec3) -> str:
        """ Return the block's namespaced id at relative coordinates """
        block_data = self.get_relative_block_data_at(p)
        return block_data.namespaced_name

    def get_block_id_at(self, p: ivec3) -> str:
        """ Return the block's namespaced id at coordinates """
        return self.get_relative_block_id_at(self._relative(p))

    def get_biome_at(self, p: ivec3) -> int:
        """ Return biome at given coordinates

        Biome Data is represented as a 4x4x4 area
        """
        return self.get_relative_biome_at(self._relative(p))

    def get_relative_biome_at(self, rp: ivec3):
        bp = self._floor_div_p(rp, 4)

        biome_index = self.biomes[bp.z, bp.x, bp.y]

        return biome_index

    def get_biomes_in_chunk(self, p: ivec3) -> list[int]:
        """**Return a list of biomes in the same chunk**."""

        cp, rp = self._relative(p)
        bp = rp // 4

        biomes = set()
        for x, y, z in bp:
            biomes.add(biomes[x, z, y])
        return [ix for ix in biomes]

    def get_primary_biome_in_chunk(self, p: ivec3) -> int:
        """**Return the most prevelant biome in the same chunk**."""
        from .lookup import BIOMES

        cp, rp = self._relative(p)
        bp = rp // 4

        biomes = {}
        highest = 0
        highest_index = 0
        for x, y, z in bp:
            biome_index = biomes[x, z, y]
            if biome_index in biomes:
                biomes[biome_index] += 1
            else:
                biomes[biome_index] = 1
            if biomes[biome_index] > highest:
                highest_index = biome_index
                highest = biomes[biome_index]

        return BIOMES[highest_index]


def closest_version(version):
    """Retrieve next-best version code to given version code."""
    if version in VERSIONS:
        return version
    for val in sorted(VERSIONS.keys(), reverse=True):
        if version - val >= 0:
            return val
    return 0


def check_version():
    """Retrieve Minecraft version and check compatibility."""
    world_slice = WorldSlice.from_server(Rect.from_corners(0, 0, 1, 1))
    # check compatibility
    if world_slice.data_version not in VERSIONS or VERSIONS[SUPPORTS] not in VERSIONS[world_slice.data_version]:
        closest = closest_version(world_slice.data_version)
        closest_name = VERSIONS[closest]
        closest_name += " snapshot" if world_slice.data_version > closest else ""
        if closest > SUPPORTS:
            print(f"{TCOLORS['orange']}WARNING: You are using a newer "
                  f"version of Minecraft then GDPC supports!\n"
                  f"\tSupports: {VERSIONS[SUPPORTS]} "
                  f"Detected: {closest_name}{TCOLORS['CLR']}")
        elif closest < SUPPORTS:
            print(f"{TCOLORS['orange']}WARNING: You are using an older "
                  f"version of Minecraft then GDPC supports!\n"
                  f"\tSupports: {VERSIONS[SUPPORTS]} "
                  f"Detected: {closest_name}{TCOLORS['CLR']}")
        else:
            raise ValueError(f"{TCOLORS['red']}Invalid supported version:"
                             f"SUPPORTS = {world_slice.data_version}!{TCOLORS['CLR']}")
    else:
        closest_name = VERSIONS[world_slice.data_version]

    return world_slice.data_version, closest_name
