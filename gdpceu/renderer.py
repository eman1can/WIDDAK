from os.path import exists
from time import sleep

import numpy as np
import open3d as o3d

from sys import platform
from PIL import Image, ImageShow

from gdpc_source.gdpc import lookup
from gdpc_source.gdpc.toolbox import loop2d, loop3d

"""
The default viewer is the default system application for PNG files.
Change this to be Whatever you want
"""
class PhotoViewer(ImageShow.Viewer):
    def __init__(self, viewer_exe, format, options=None, **kwargs):
        self._exe = viewer_exe
        self.format = format
        if options is not None:
            self.options = options
        super().__init__(**kwargs)

    def get_command(self, file, **options):
        return f'{self._exe} "{file}" && ping -n 2 127.0.0.1 >NUL && del /f "{file}"'

if platform == 'windows' and exists('C:/IrfanView/i_view64.exe'):
    print('Register IrfanView as Photo Viewer')







class Renderer:
    def __init__(self):
        self._render = None
        self._color_map = {}
        self._palette = lookup.PALETTELOOKUP
        self._height_map = None
        self._xo, self._yo, self._zo = 0, 0, 0

        self._render_3d = None
        self._render_2d = None
        self._viewer = None

    def set_default_viewer(self, viewer='C:/IrfanView/i_view64.exe'):
        ImageShow.register(PhotoViewer(viewer, 'PNG'), 0)
        ImageShow.register(PhotoViewer(viewer, 'JPEG', {"compress_level": 1}), 0)
        self._viewer = PhotoViewer(viewer, 'TIFF')
        ImageShow.register(self._viewer, 0)

    def get_color_map(self):
        return self._color_map

    def bgr_hex_to_float_rgb(self, hex):
        if hex in self._color_map:
            return self._color_map[hex]
        b = (hex & 0xFF) / 0xFF
        g = ((hex >> 8) & 0xFF) / 0xFF
        r = ((hex >> 16) & 0xFF) / 0xFF
        c = np.array([r, g, b], dtype=np.float64)
        self._color_map[hex] = c
        return c

    def rgb_hex_to_float_rgb(self, hex):
        if hex in self._color_map:
            return self._color_map[hex]
        r = (hex & 0xFF) / 0xFF
        g = ((hex >> 8) & 0xFF) / 0xFF
        b = ((hex >> 16) & 0xFF) / 0xFF
        c = np.array([r, g, b], dtype=np.float64)
        self._color_map[hex] = c
        return c

    def hex_to_int_rgb(self, hex):
        if hex in self._color_map:
            return self._color_map[hex]
        b = hex & 0xFF
        g = (hex >> 8) & 0xFF
        r = (hex >> 16) & 0xFF
        c = np.array([r, g, b], dtype=np.uint8)
        self._color_map[hex] = c
        return c

    def _setup_render(self, world_slice, color_map):
        self._color_map = color_map if color_map is not None else {}
        self._height_map = np.array(world_slice.heightmaps["WORLD_SURFACE"][:-1, :-1], dtype=int)

    def _setup_template_render(self, color_map):
        self._color_map = color_map if color_map is not None else {}

    def _get_hex_color_for_id(self, blockID):
        if blockID == 'minecraft:air' or blockID == 'minecraft:cave_air':
            return 0x000000
        elif blockID not in self._palette:
            print(f'Unknown block: {blockID}')
            return 0xFF00C7  # Hot Pink / Missing Texture
        else:
            return self._palette[blockID]

    def _get_hex_color(self, world_slice, x, y, z):
        try:
            blockID = world_slice.getBlockAt(x, y, z)
            return self._get_hex_color_for_id(blockID)
        except IndexError:
            raise IndexError(f'Failed to get block at index {x} {y} {z}')

    def make_2d_render(self, rect, world_slice, color_map=None):
        self._setup_render(world_slice, color_map)
        self._render_2d = np.zeros((*rect.size, 3), dtype=np.uint8)

        x1, z1 = rect.begin
        xo, zo = x1 - world_slice.rect[0], z1 - world_slice.rect[1]
        print(x1, z1, xo, zo)
        for x, z in loop2d(*rect.size):
            y = self._height_map[(xo + x, zo + z)] - 1  # Surface Map is Offset by 1
            hc = self._get_hex_color(world_slice, x1 + x, y, z1 + z)
            rgbc = self.hex_to_int_rgb(hc)
            self._render_2d[x, z] = rgbc
        return self

    def show_2d_render(self):
        if self._render_2d is None:
            print('2d render not created!')
            return self
        pil_image = Image.fromarray(self._render_2d, mode='RGB')
        ImageShow.show(pil_image, '2D Render')
        return self

    def save_2d_render(self, file_path='output.tiff'):
        if self._render_2d is None:
            print('2d render not created!')
            return self
        pil_image = Image.fromarray(self._render_2d, mode='RGB')
        pil_image.save(file_path)
        return self

    def make_3d_render(self, rect, world_slice, color_map=None, xs=0, ys=0, zs=0, fill_mode='am', nn=2):
        self._setup_render(world_slice, color_map)
        self._render_3d = o3d.geometry.TriangleMesh()

        x1, z1 = rect.begin
        x2, z2 = rect.end
        xl, zl = x2 - x1, z2 - z1
        xo, zo = x1 - world_slice.rect[0], z1 - world_slice.rect[1]
        by = 0
        if fill_mode == 'am':
            by = np.min(self._height_map[xo:xo + xl, zo:zo + zl]) - 1  # Height Map is Offset by 1
        elif fill_mode == 'ab':
            by = 0

        for x, z in loop2d(0, 0, xl, zl):  # Loop2D is [inclusive, inclusive]
            if fill_mode == 'rm':
                by = np.min(self._height_map[max(xo, xo + x - nn):min(xo + xl, xo + x + nn), max(zo, zo + z - nn):min(zo + zl, zo + z + nn)]) - 1  # Height Map is Offset by 1
            ty = self._height_map[xo + x, zo + z]
            for y in range(by, ty):
                hc = self._get_hex_color(world_slice, x1 + x, y, z1 + z)
                if hc == 0x000000:
                    continue
                rgbc = self.bgr_hex_to_float_rgb(hc)
                cube = o3d.geometry.TriangleMesh.create_box(width=1, height=1, depth=1)
                cube.paint_uniform_color(rgbc)
                cube.translate([x + x * xs, y + y * ys, z + z * zs], relative=False)
                self._render_3d += cube
        return self

    def show_3d_render(self):
        if self._render_3d is None:
            print('3d render not created!')
            return self
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        opt = vis.get_render_option()
        opt.background_color = np.asarray([0, 0, 0])
        self._render_3d.transform([[0.862, 0.011, -0.507, 0.0], [-0.139, 0.967, -0.215, 0.7], [0.487, 0.255, 0.835, -1.4], [0.0, 0.0, 0.0, 1.0]])
        vis.add_geometry(self._render_3d)
        vis.run()
        vis.destroy_window()
        return self

    def save_3d_render(self, file_path='output.ply'):
        if self._render_3d is None:
            print('3d render not created!')
            return self
        o3d.io.write_triangle_mesh(file_path, self._render_3d)
        return self

    def make_2d_template_render(self, template, color_map=None):
        self._setup_template_render(color_map)

        yl = len(template)
        xl = len(template[0])
        zl = len(template[0][0])

        self._render_2d = np.zeros((xl, zl, 3), dtype=np.uint8)

        for x, z in loop2d(xl, zl):
            for y in range(yl - 1, -1, -1):
                if template[y][x][z] is None:
                    continue
                blockID = template[y][x][z]
                hex_color = self._get_hex_color_for_id(blockID)
                rgbc = self.hex_to_int_rgb(hex_color)
                self._render_2d[x, z] = rgbc
                break
        return self

    def make_3d_template_render(self, template, color_map=None, xs=0, ys=0, zs=0):
        self._setup_template_render(color_map)

        yl = len(template)
        xl = len(template[0])
        zl = len(template[0][0])

        self._render_3d = o3d.geometry.TriangleMesh()
        for x, y, z in loop3d(xl, yl, zl):
            blockID = template[y][x][z]
            if blockID is None:
                continue
            hex_color = self._get_hex_color_for_id(blockID)
            rgbc = self.bgr_hex_to_float_rgb(hex_color)
            cube = o3d.geometry.TriangleMesh.create_box(width=1, height=1, depth=1)
            cube.paint_uniform_color(rgbc)
            cube.translate([x + x * xs, y + y * ys, z + z * zs], relative=False)
            self._render_3d += cube
        return self

    def make_3d_vox_render(self, vox_model, palette, xs=0, ys=0, zs=0):
        yl, xl, zl = vox_model.shape

        self._render_3d = o3d.geometry.TriangleMesh()
        for x, y, z in loop3d(xl, yl, zl):
            color_index = vox_model[y][x][z]
            hex_color = palette[color_index]
            if hex_color == 0x00:
                continue
            print('%X' % hex_color)
            rgbc = self.rgb_hex_to_float_rgb(hex_color)
            cube = o3d.geometry.TriangleMesh.create_box(width=1, height=1, depth=1)
            cube.paint_uniform_color(rgbc)
            cube.translate([x + x * xs, y + y * ys, z + z * zs], relative=False)
            self._render_3d += cube
        return self