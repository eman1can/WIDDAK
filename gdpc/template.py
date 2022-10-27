from glm import ivec3

from .lookup import BIOMES, PALETTE, VOX_COLOR_MAP
from .vector_util import Box

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
    def from_vox_model(name, model, palette):
        pass

    def __init__(self, name, base_bi, var_ix, data):
        self._name = name
        self._base_bi = base_bi
        self._variation = var_ix
        self._data = data

        yl = len(data)
        xl = len(data[0])
        zl = len(data[0][0])

        self.shape = ivec3(yl, xl, zl)
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

    def __iter__(self):
        self._y = self._x = self._z = 0
        return self

    def __next__(self):
        for x, y, z in Box(ivec3(0, 0, 0), self.shape):
            blockID = self._data[y][x][z]
            yield x, y, z, blockID
        raise StopIteration

    def get_biome_variation(self, biome_index):
        pass  # TODO: Add function to vary buildings given a biome
