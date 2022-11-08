from ctypes import *
from os.path import join

from gdpc.template import Template
from gdpc.textures import MULTI_TEXTURES, MULTI_TEXTURES_LIST, SIMPLE_TEXTURES


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
    add_voxel = wrap_function(libc, 'renderer_add_voxel', c_void_p, [c_void_p, c_float, c_float, c_float, c_uint8, c_uint32])
    open = wrap_function(libc, 'renderer_open', c_void_p, None)
    renderer = create(1920, 1080)
    res = init(renderer)

    template = Template.from_file(join('local', 'templates', 'modern_house.template'))
    ox, oy, oz = -5,  -4, -10

    for x, y, z, blockID, blockState in template.loop():
        if blockID == 'minecraft:air':
            continue
        category = -1
        index = 0
        if blockID in SIMPLE_TEXTURES:
            category = 0
            index = SIMPLE_TEXTURES.index(blockID)
        elif blockID in MULTI_TEXTURES_LIST:
            category = 1
            index = MULTI_TEXTURES_LIST.index(blockID)
        if category == -1:
            continue
        # print(f'renderer->addVoxel(glm::fvec3({x + ox}, {y + oy}, {z + oz}), {category}, {index}); // {blockID}')
        add_voxel(renderer, x + ox, y + oy, z + oz, category, index)
    open(c_void_p(renderer))
