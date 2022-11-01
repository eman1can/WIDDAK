from ctypes import *


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
    libc = CDLL('cmake-build-debug/LibVoxel.dll')

    create = wrap_function(libc, 'renderer_create', c_void_p, [c_int, c_int])
    init = wrap_function(libc, 'renderer_init', c_int, [c_void_p])
    add_voxel = wrap_function(libc, 'renderer_add_voxel', c_void_p, [c_void_p, c_float, c_float, c_float, c_uint8, c_uint32])
    open = wrap_function(libc, 'renderer_open', c_void_p, None)
    renderer = create(1920, 1080)
    res = init(renderer)
    add_voxel(renderer, 0, 0, 0, 0, 0)
    open(c_void_p(renderer))
