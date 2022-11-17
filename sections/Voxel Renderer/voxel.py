from ctypes import *
from os.path import join

from gdpc.lookup import STAIRS
from gdpc.template import Template
from gdpc.textures import CATEGORIES, MULTI_TEXTURES, MULTI_TEXTURES_LIST, SIMPLE_TEXTURES, STAIR_TEXTURES, STAIR_TEXTURES_LIST, VARIABLE_HEIGHT


def wrap_function(lib, func_name, res_type, arg_types):
    """ Simplify wrapping ctypes functions """
    func = lib.__getattr__(func_name)
    func.restype = res_type
    func.argtypes = arg_types
    return func


class Point(Structure):
    _fields_ = [('x', c_int32), ('y', c_int32)]

    def __repr__(self):
        return f'<{self.x} {self.y}>'


if __name__ == "__main__":
    libc = CDLL('sections/Voxel Renderer/cmake-build-debug/LibVoxel.dll')

    create = wrap_function(libc, 'renderer_create', c_void_p, [c_int, c_int])
    init = wrap_function(libc, 'renderer_init', c_int, [c_void_p])
    add_voxel = wrap_function(libc, 'renderer_add_voxel', c_void_p, [c_void_p, c_float, c_float, c_float, c_uint8, c_uint8, c_uint32])
    open = wrap_function(libc, 'renderer_open', c_void_p, None)
    renderer = create(1920, 1080)
    res = init(renderer)

    template = Template.from_file(join('local', 'templates', 'rustic_cabin.template'))
    ox, oy, oz = -5,  -4, -10

    missing = set()
    for x, y, z, relation, block in template.loop():
        blockID = block.namespaced_name
        if blockID == 'minecraft:air':
            continue
        if relation == 0x3F:
            continue
        category = -1
        index = 0
        if blockID in SIMPLE_TEXTURES:
            category = CATEGORIES.index('SIMPLE')
            index = SIMPLE_TEXTURES.index(blockID)
        elif blockID in MULTI_TEXTURES_LIST:
            category = CATEGORIES.index('MULTI_TEXTURE')
            index = MULTI_TEXTURES_LIST.index(blockID)
        elif blockID in STAIR_TEXTURES_LIST:
            category = CATEGORIES.index('STAIRS')
            index = STAIR_TEXTURES_LIST.index(blockID)
        elif blockID in [x for l in VARIABLE_HEIGHT.values() for x in l]:
            for height, vh_list in VARIABLE_HEIGHT.items():
                category = CATEGORIES.index('SIMPLE_' + str(height)[2:].zfill(2))
                index = vh_list.index(blockID)
        if category == -1:
            if blockID not in missing:
                missing.add(blockID)
                print('// Skipping', blockID + '; Not found')
            continue
        rotation = 0
        block_state = block.properties
        if 'axis' in block_state:
            axis = str(block_state['axis'])
            rotation += {'y': 0, 'z': 1, 'x': 2}[axis]
        if 'facing' in block_state:
            facing = str(block_state['facing'])
            rotation += {'north': 0, 'east': 2, 'south': 4, 'west': 6}[facing]
        if 'half' in block_state:
            half = str(block_state['half'])
            rotation += {'bottom': 0, 'top': 6}[half]
        # if len(blockState) > 0:
        #     print(blockID, blockState)
        # print(f'renderer->addVoxel(glm::fvec3({x + ox}, {y + oy}, {z + oz}), {relation}, {rotation}, {category}, {index}); // {blockID}')
        add_voxel(renderer, x + ox, y + oy, z + oz, relation, rotation, category, index)
    open(c_void_p(renderer))
