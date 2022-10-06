from math import ceil
from os.path import join

from glm import ivec2

from gdpc_source.gdpc.worldLoader import WorldSlice
from gdpce.vector_util import Rect


class World:
    def __init__(self, world_save_file, allow_outside=False):
        self._allow_outside = allow_outside
        if not world_save_file.endswith('.dat'):
            print('This is not a valid world file')
            exit(1)
        self.allow_outside = self._allow_outside
        with open(world_save_file, 'r') as dat_file:
            self.world_name, self.step, self.x1, self.z1, self.x2, self.z2 = dat_file.read().split(',')
        self.x1, self.x2, self.z1, self.z2 = int(self.x1), int(self.x2), int(self.z1), int(self.z2)
        self.step = int(self.step)

    def getWorldBounds(self):
        return Rect(ivec2(self.x1, self.z1), ivec2(self.x2 - self.x1, self.z2 - self.z1))

    def getWorldSlice(self, rect):
        x1, z1, = rect.offset
        x2, z2 = rect.end
        if x1 < self.x1 or z1 < self.z1 or x2 > self.x2 or z2 > self.z2:
            print('Rect out of bounds of world file!')
            exit(1)
        # Locate The World Slices
        cx1 = self.x1 + abs(x1 - self.x1) // self.step * self.step
        cz1 = self.z1 + abs(z1 - self.z1) // self.step * self.step
        cx2 = ceil(x2 / self.step) * self.step
        cz2 = ceil(z2 / self.step) * self.step
        # Get Huge Slice
        # Get Portion of that Slice
        master_slice = None
        for x in range(cx1, cx2, self.step):
            row_slice = None
            for z in range(cz1, cz2, self.step):
                with open(join('worlds', self.world_name, 'saved', f'{x}_{z}_{self.step}.chunk'), 'rb') as chunk_file:
                    byte_data = chunk_file.read()
                slice = SavedWorldSlice(byte_data, x, z, min(x + self.step, self.x2), min(z + self.step, self.z2))
                row_slice = slice if row_slice is None else row_slice + slice
            master_slice = row_slice if master_slice is None else master_slice + row_slice
        # Crop the slice to the portion we want
        return master_slice


class SavedWorldSlice(WorldSlice):
    def __init__(self, byte_data, x1, z1, x2, z2):
        self.rect = x1, z1, x2 - x1, z2 - z1
        cxl = int(ceil((x2 - x1) / 16))
        czl = int(ceil((z2 - z1) / 16))
        self.chunkRect = (x1 // 16, z1 // 16, cxl, czl)
        self.heightmapTypes = ["MOTION_BLOCKING",
                              "MOTION_BLOCKING_NO_LEAVES",
                              "OCEAN_FLOOR",
                              "WORLD_SURFACE"]
        self.byte_data = byte_data
        self._load_slice()

    def __add__(self, other):
        if other is None:
            return self
        # Other Must Be To the Right Or Below
        x1s, z1s, xls, zls = self.rect
        x1o, z1o, xlo, zlo = other.rect
        if x1s + xls == x1o and zls == zlo:
            # To the Right
            print('To The Right')
            x1, z1, x2, z2 = x1s, z1s, x1o + xlo, z1o + zlo

        elif z1s + zls == z1o and xls == xlo:
            # To the Bottom
            print('To The Bottom')
        else:
            print('Chunks not adjacent')
            return None
