import numpy as np
from glm import ivec3

from sections.Blueprints.identifiers import ID_TO_NAME
from amulet.api.block import Block
from .color import Color
from .lookup import BIOMES, BIOMES_NAME_TO_INDEX, PALETTE
from .vector_util import Box
from .vox_lookup import HEX_TO_MINECRAFT, VOX_TO_MINECRAFT
from .worldLoader import WorldSlice

NO_BIOME = -1

# Variations
DEFAULT = 0


class TemplateManager:
    def __init__(self):
        self._templates = {k: {} for k in BIOMES.keys()}
        self._templates[NO_BIOME] = {}

    def get_templates_by_biome(self, biome_index):
        return self._templates[biome_index]

    def get_template(self, biome_index, template, variation=DEFAULT):
        return self._templates[biome_index][template][variation]

    def register_template(self, biome_index, template, variation=DEFAULT, force=False):
        name = template.get_name()
        if name in self._templates[biome_index] and variation in self._templates[biome_index][name] and not force:
            print('This template already exists')
            return
        if name not in self._templates[biome_index]:
            self._templates[biome_index][name] = {}
        self._templates[biome_index][name][variation] = template

    def remove_template(self, biome_index, name):
        self._templates[biome_index].pop(name)


class Template:
    @staticmethod
    def from_vox_model(name, model, palette, palette_key, biome):
        y, x, z = model.shape
        output_model = [[[None for _ in range(z)] for _ in range(x)] for _ in range(y)]
        color = Color({})

        specific_palette = None
        if palette_key in VOX_TO_MINECRAFT:
            specific_palette = VOX_TO_MINECRAFT[palette_key]

        for xi, yi, zi in Box.from_box(0, 0, 0, x, y, z).loop():
            ix = model[yi][xi][zi]
            hex_color = '#' + color.int_bgr_hex_to_string(int(palette[ix]))

            blockID = 'minecraft:air'
            if hex_color in specific_palette:
                if isinstance(specific_palette[hex_color], str):
                    blockID = specific_palette[hex_color]
                else:
                    blockID = specific_palette[hex_color][biome]

            output_model[yi][xi][zi] = Block.from_string_blockstate(blockID)
        # TODO: Add Cleanup algorithm for stairs, trapdoors, etc.
        bix = BIOMES_NAME_TO_INDEX[biome]
        return Template(name, bix, 0, output_model)

    @staticmethod
    def from_world_slice(name, world_slice: WorldSlice, area: Box):
        data = [[["" for _ in range(area.dz)] for _ in range(area.dx)] for _ in range(area.dy)]
        for x, y, z in area.loop():
            data[y - area.y1][x - area.x1][z - area.z1] = world_slice.get_block_data_at(ivec3(x, y, z))
        return Template(name, 0, 0, data)

    def __init__(self, name, base_bi, var_ix, data):
        self._name = name
        self._base_bi = base_bi
        self._variation = var_ix
        self._data: list[list[list[Block]]] = data

        yl = len(data)
        xl = len(data[0])
        zl = len(data[0][0])

        self.shape = ivec3(xl, yl, zl)
        self._y = self._x = self._z = 0

    def get_name(self):
        return self._name

    def get_id(self):
        return f'{self._base_bi}_{self._name}_{self._variation}'

    def get_biome_index(self):
        return self._base_bi

    def get_biome(self):
        return BIOMES[self._base_bi]

    def get_block(self, x, y, z):
        return self._data[y][x][z]

    def get_hex_color(self, x, y, z):
        blockID = self._data[y][x][z]
        return PALETTE[blockID]

    def to_string(self):
        output = ''
        max_name_size = 0
        # 10 11 12
        for x, y, z in Box(ivec3(0, 0, 0), self.shape).loop():
            blockID = self._data[y][x][z].namespaced_name
            max_name_size = max(max_name_size, len(ID_TO_NAME[blockID]))
        for y in self._data:
            for x in y:
                output += '|'
                for z in x:
                    output += ID_TO_NAME[z.namespaced_name].center(max_name_size) + ' '
                output += '|\n'
            output += '-' * ((max_name_size + 1) * len(y[0]) + 2) + '\n'
        return output

    def _exists(self, block: Block):
        return block is not None and block.base_name != 'air'

    def _get_relations(self):
        # 0000 0000
        # Front, Top, Back, Bottom, Left, Right
        x, y, z = self.shape
        relations = np.zeros((y, x, z), np.uint8)
        for xi, yi, zi in Box(ivec3(0, 0, 0), self.shape).loop():
            res = 0
            res |= zi + 1 < z and self._exists(self._data[yi][xi][zi + 1])
            res |= (yi + 1 < y and self._exists(self._data[yi + 1][xi][zi])) << 1
            res |= (zi - 1 >= 0 and self._exists(self._data[yi][xi][zi - 1])) << 2
            res |= (yi - 1 >= 0 and self._exists(self._data[yi - 1][xi][zi])) << 3
            res |= (xi - 1 >= 0 and self._exists(self._data[yi][xi - 1][zi])) << 4
            res |= (xi + 1 < x and self._exists(self._data[yi][xi + 1][zi])) << 5
            relations[yi][xi][zi] = res
        return relations

    def loop(self):
        relations = self._get_relations()
        for x, y, z in Box(ivec3(0, 0, 0), self.shape).loop():
            block = self._data[y][x][z]
            if block is None:
                continue
            yield x, y, z, relations[y][x][z], block

    def get_biome_variation(self, biome_index):
        pass  # TODO: Add function to vary buildings given a biome

    def to_file(self, path):
        if not path.endswith('.template'):
            path += '.template'
        ids = set()
        for x, y, z in Box(ivec3(0, 0, 0), self.shape).loop():
            block = self._data[y][x][z]
            ids.add(block.blockstate)
        ids = list(ids)

        id_count = len(ids)
        id_lengths = [len(x) - len('minecraft:') for x in ids]
        indices = []
        for x, y, z in Box(ivec3(0, 0, 0), self.shape).loop():
            block = self._data[y][x][z]
            indices.append(ids.index(block.blockstate))

        with open(path, 'wb') as file:
            file.write(int.to_bytes(len(self._name), 2, 'little'))
            file.write(self._name.encode('utf-8'))
            x, y, z = self.shape
            file.write(int.to_bytes(x, 4, 'little'))
            file.write(int.to_bytes(y, 4, 'little'))
            file.write(int.to_bytes(z, 4, 'little'))
            file.write(int.to_bytes(self._base_bi, 2, 'little'))
            file.write(int.to_bytes(self._variation, 2, 'little'))
            file.write(int.to_bytes(id_count, 2, 'little'))
            for id_length in id_lengths:
                file.write(int.to_bytes(id_length, 1, 'little'))
            for identifier in ids:
                file.write(identifier[len('minecraft:'):].encode('utf-8'))
            for block_index in indices:
                file.write(int.to_bytes(block_index, 1, 'little'))

    @staticmethod
    def from_file(path):
        if not path.endswith('.template'):
            path += '.template'
        with open(path, 'rb') as file:
            name_length = int.from_bytes(file.read(2), 'little')
            name = file.read(name_length).decode('utf-8')
            x = int.from_bytes(file.read(4), 'little')
            y = int.from_bytes(file.read(4), 'little')
            z = int.from_bytes(file.read(4), 'little')
            biome_index = int.from_bytes(file.read(2), 'little')
            variation_index = int.from_bytes(file.read(2), 'little')
            id_count = int.from_bytes(file.read(2), 'little')
            identifiers = []
            id_lengths = []
            for ix in range(id_count):
                id_lengths.append(int.from_bytes(file.read(1), 'little'))
            for id_length in id_lengths:
                identifiers.append('minecraft:' + file.read(id_length).decode('utf-8'))
            data = [[['' for _ in range(z)] for _ in range(x)] for _ in range(y)]
            for x, y, z in Box.from_box(0, 0, 0, x, y, z).loop():
                index = int.from_bytes(file.read(1), 'little')
                data[y][x][z] = Block.from_string_blockstate(identifiers[index])
            return Template(name, biome_index, variation_index, data)
