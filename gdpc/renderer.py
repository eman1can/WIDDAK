import io
import json
from math import ceil, sqrt
import matplotlib.pyplot as plt

import cv2
import numpy as np

from PIL import Image, ImageShow
from glm import clamp, ivec3
from scipy.interpolate import interp1d

import gdpc.lookup as lookup
from .vector_util import Rect
from .color import Color
# from .textures import IDENTIFIER_TO_TEXTURES, SIMPLE_TEXTURES


class PhotoViewer(ImageShow.Viewer):
    """
    The default viewer is the default system application for PNG files.
    This allows you to set the photo viewer to the viewer of your choice

    @viewer_path This is the path to the executable you want to run
    Ex. C:/PhotoViewer.exe
    @img_format This is the PIL Format that you want to override
    Ex. PNG or JPEG or TIFF
    """
    def __init__(self, viewer_path, img_format, options=None, **kwargs):
        self._exe = viewer_path
        self.format = img_format
        if options is not None:
            self.options = options
        super().__init__(**kwargs)

    def get_command(self, file, **options):
        return f'{self._exe} "{file}" && ping -n 2 127.0.0.1 >NUL && del /f "{file}"'


class Renderer:
    def __init__(self):
        self._render = None
        self._color_map = Color({})
        self._palette = lookup.PALETTELOOKUP
        self._height_map = None
        self._xo, self._yo, self._zo = 0, 0, 0

        self._render_3d = None
        self._render_2d = None
        self._legend = None

        self._viewer = None
        self._name = 'Render'

        self._colors = set()

    def set_default_viewer(self, viewer='C:/IrfanView/i_view64.exe'):
        ImageShow.register(PhotoViewer(viewer, 'PNG'), 0)
        ImageShow.register(PhotoViewer(viewer, 'JPEG', {"compress_level": 1}), 0)
        self._viewer = PhotoViewer(viewer, 'TIFF')
        ImageShow.register(self._viewer, 0)

    def get_color_map(self):
        return self._color_map

    def _setup_render(self, world_slice, color_map):
        self._color_map = color_map if color_map is not None else Color({})
        self._height_map = world_slice.get_heightmap('MOTION_BLOCKING')

    def _setup_template_render(self, color_map):
        self._color_map = color_map if color_map is not None else Color({})

    def _apply_legend(self, image: Image):
        if self._legend is None:
            return
        colors = ['#' + hex(lookup.BIOME_COLORS[x] if x != -1 else 0xFF00C7)[2:] for x in self._legend]
        labels = [lookup.BIOMES[x].replace('_', ' ').title() if x != -1 else "Missing Color" for x in self._legend]
        f = lambda m, c: plt.plot([], [], marker=m, color=c, ls="none")[0]
        handles = [f("s", colors[i]) for i in range(len(labels))]
        legend = plt.legend(handles, labels, loc=3, framealpha=1, frameon=False)
        fig = legend.figure
        fig.canvas.draw()
        bbox = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png', dpi="figure", bbox_inches=bbox)
        im = Image.open(img_buf)
        new_width = image.width // 5
        image.paste(im.resize((new_width, int(new_width / im.width * im.height))), (0, 0))
        img_buf.close()

    def _apply_topography(self):
        if self._render_2d is None:
            print('2d render not created!')
            return self
        gradientX = cv2.Scharr(self._height_map, cv2.CV_16S, 1, 0)
        gradientY = cv2.Scharr(self._height_map, cv2.CV_16S, 0, 1)
        brightness = np.expand_dims((gradientX + gradientY), 2).clip(-64, 64)
        self._render_2d = (self._render_2d.astype('int16') + brightness).clip(0, 255)

    def show_2d_render(self):
        if self._render_2d is None:
            print('2d render not created!')
            return self
        pil_image = Image.fromarray(self._render_2d, mode='RGB')
        self._apply_legend(pil_image)
        ImageShow.show(pil_image, self._name)
        return self

    def save_2d_render(self, file_path='local/renders/output.tiff'):
        if self._render_2d is None:
            print('2d render not created!')
            return self
        pil_image = Image.fromarray(self._render_2d.astype('uint8'), mode='RGB')
        self._apply_legend(pil_image)
        pil_image.save(file_path)
        return self

    def _normalize(self, array):
        """**Normalize the array to contain values from 0 to 1**."""
        return (array - array.min()) / (array.max() - array.min())

    def make_2d_heatmap_render(self, arrays, title="2D Heatmap Render", panel_width=None, panel_height=None):
        """ Renders a collection of 2d arrays as a heatmap images. """
        heatmap_color = interp1d([0, 1], np.array([[255, 0, 0], [0, 255, 0]], np.uint8))
        # Create the base image
        if panel_height is None or panel_width is None:
            panel_height, panel_width = arrays[0].shape
        panel_count = ceil(sqrt(len(arrays)))
        total_width = panel_width * panel_count
        total_height = panel_height * panel_count
        self._render_2d =np.zeros((total_width, total_height), dtype=np.uint8)
        self._name = title

        for aix, array in enumerate(arrays):
            wo = (aix * panel_width) % total_width
            ho = (aix * panel_height) / total_height
            norm = self._normalize(array).astype(np.uint8)
            for y in range(norm.height):
                for x in range(norm.width):
                    self._render_2d[wo + y, ho + x] = heatmap_color(norm[y][x])
        return self

    def make_2d_surface_render(self, rect: Rect, world_slice, color_map=None, title="World Render"):
        self._setup_render(world_slice, color_map)
        self._render_2d = np.zeros((*rect.size, 3), dtype=np.uint32)
        self._name = title
        for xix, rx in enumerate(range(rect.dx)):
            for zix, rz in enumerate(range(rect.dz)):
                y = self._height_map[rx, rz]
                blockID = world_slice.get_relative_block_id_at(ivec3(rx, y, rz))
                self._render_2d[xix, zix] = self._color_map.get_int_rgb(blockID)
        return self

    def make_2d_topographic_render(self, rect: Rect, world_slice, color_map=None, title="Topographic World Render"):
        self.make_2d_surface_render(rect, world_slice, color_map, title)
        self._apply_topography()
        return self

    def make_2d_surface_biome_render(self, rect: Rect, world_slice, color_map=None, title="Biome Render"):
        self._setup_render(world_slice, color_map)
        self._render_2d = np.zeros((*rect.size, 3), dtype=np.uint32)
        self._name = title

        self._legend = []
        missing_biomes = set()
        for xix, rx in enumerate(range(rect.dx)):
            for zix, rz in enumerate(range(rect.dz)):
                y = self._height_map[rx, rz]
                biome_index = world_slice.get_relative_biome_at(ivec3(rx, y, rz))
                biome_color = lookup.BIOME_COLORS[biome_index]

                if biome_color == 0xFF00C7 and biome_index not in missing_biomes:
                    print(lookup.BIOMES[biome_index], 'has no color')
                    missing_biomes.add(biome_index)
                if biome_index not in self._legend and biome_color != 0xFF00C7:
                    self._legend.append(biome_index)
                self._render_2d[xix, zix] = self._color_map.bgr_hex_to_int_rgb(biome_color)
        if len(missing_biomes) > 0:
            self._legend.append(-1)
        return self

    def make_2d_topographic_biome_render(self, rect: Rect, world_slice, color_map=None, title="Topographic Biome Render"):
        self.make_2d_surface_biome_render(rect, world_slice, color_map, title)
        self._apply_topography()
        return self


    # def _render_cube(self, blockID, cx, cy, cz):
    #     nbt = {}
    #     if '[' in blockID:
    #         blockID, nbt_data = blockID[:-1].split('[')
    #         for nbt_value in nbt_data.split(','):
    #             k, v = nbt_value.split('=')
    #             nbt[k] = v
    #
    #     try:
    #         texture_data = IDENTIFIER_TO_TEXTURES[blockID]
    #     except KeyError:
    #         if not exists(join('block_assets', f'{blockID.split(":")[1]}.png')):
    #             raise Exception(f'{blockID.split(":")[1]}.png not found!')
    #         texture_data = {
    #             'size':        [1, 1, 1],
    #             'textures':    [f'{blockID.split(":")[1]}.png'],
    #             'texture_ids': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32)
    #         }
    #     cube = o3d.geometry.TriangleMesh.create_box(*texture_data['size'], True, True)
    #
    #     cube.textures = [o3d.io.read_image(join('block_assets', image_source)) for image_source in texture_data['textures']]
    #
    #     cube.triangle_material_ids = o3d.utility.IntVector(texture_data['texture_ids'])
    #     cube.compute_vertex_normals()
    #
    #     cube.translate([cx, cy, cz], relative=False)
    #
    #     if 'translate' in texture_data:
    #         cube.translate(texture_data['translate'])
    #
    #     # Do NBT data
    #     for k, v in nbt.items():
    #         if k in texture_data:
    #             for operation, values in texture_data[k][v].items():
    #                 if operation == 'rotation':
    #                     cube.rotate(cube.get_rotation_matrix_from_xyz(values), center=(cx, cy, cz))
    #                 elif operation == 'translate':
    #                     cube.translate(values)
    #     return cube
    #
    # def make_3d_render(self, rect, world_slice, color_map=None, xs=0, ys=0, zs=0, fill_mode='am', nn=2):
    #     self._setup_render(world_slice, color_map)
    #     self._render_3d = []
    #
    #     x1, z1 = rect.begin
    #     x2, z2 = rect.end
    #     xl, zl = x2 - x1, z2 - z1
    #     xo, zo = x1 - world_slice.rect.x1, z1 - world_slice.rect.z1
    #     by = 0
    #     if fill_mode == 'am':
    #         by = np.min(self._height_map[xo:xo + xl, zo:zo + zl])  # Height Map is Offset by 1
    #     elif fill_mode == 'ab':
    #         by = 0
    #     print(xl, zl)
    #     for x, z in loop2d(0, 0, xl, zl):  # Loop2D is [inclusive, inclusive]
    #         if fill_mode == 'rm':
    #             by = np.min(self._height_map[max(xo, xo + x - nn):min(xo + xl, xo + x + nn), max(zo, zo + z - nn):min(zo + zl, zo + z + nn)])  # Height Map is Offset by 1
    #         ty = self._height_map[xo + x, zo + z]
    #         for y in range(by, ty + 1):  # We want to include the top index, not exclude
    #             blockID = world_slice.get_block_id_at(x1 + x, y, z1 + z)
    #             if blockID in ('minecraft:air', 'minecraft:cave_air'):
    #                 continue
    #             if blockID not in IDENTIFIER_TO_TEXTURES and blockID not in SIMPLE_TEXTURES:
    #                 print(blockID, 'not textured')
    #                 continue
    #
    #             cube = self._render_cube(blockID, x + x * xs, y + y * ys, z + z * zs)
    #
    #             self._render_3d.append(cube)
    #     return self
    #
    # def show_3d_render(self):
    #     if self._render_3d is None:
    #         print('3d render not created!')
    #         return self
    #     vis = o3d.visualization.Visualizer()
    #     vis.create_window()
    #     opt = vis.get_render_option()
    #     opt.background_color = np.asarray([0, 0, 0])
    #     for cube in self._render_3d:
    #         cube.transform([[0.862, 0.011, -0.507, 0.0], [-0.139, 0.967, -0.215, 0.7], [0.487, 0.255, 0.835, -1.4], [0.0, 0.0, 0.0, 1.0]])
    #         vis.add_geometry(cube)
    #     vis.run()
    #     vis.destroy_window()
    #     return self
    #
    # def save_3d_render(self, file_path=join('renders', 'output.ply')):
    #     if self._render_3d is None:
    #         print('3d render not created!')
    #         return self
    #     o3d.io.write_triangle_mesh(file_path, self._render_3d)
    #     return self
    #
    # def save_3d_render_as_image(self, file_path=join('renders', 'output.png'), x=70, y=60, z=70):
    #     if self._render_3d is None:
    #         print('3d render not created!')
    #         return self
    #     offscreen_renderer = OffscreenRenderer(2560, 1440)
    #     offscreen_renderer.scene.scene.set_sun_light([-1, -1, -1], [1.0, 1.0, 1.0], 100000)
    #     offscreen_renderer.scene.set_background(np.array([0, 0, 0, 0]))
    #     offscreen_renderer.scene.camera.look_at([0, 0, 0], [x, y, z], [0, 1, 0])
    #     material = rendering.MaterialRecord()
    #     material.aspect_ratio = 1.0
    #     material.shader = "defaultUnlit"
    #     offscreen_renderer.scene.add_geometry('Building', self._render_3d, material)
    #     image = offscreen_renderer.render_to_image()
    #     o3d.io.write_image(file_path, image)
    #     return self

    # def make_2d_template_render(self, template, color_map=None):
    #     self._setup_template_render(color_map)
    #
    #     yl = len(template)
    #     xl = len(template[0])
    #     zl = len(template[0][0])
    #
    #     self._render_2d = np.zeros((xl, zl, 3), dtype=np.uint8)
    #
    #     for x, z in loop2d(xl, zl):
    #         for y in range(yl - 1, -1, -1):
    #             if template[y][x][z] is None:
    #                 continue
    #             blockID = template[y][x][z]
    #             hex_color = self._get_hex_color_for_id(blockID)
    #             rgbc = self.hex_to_int_rgb(hex_color)
    #             self._render_2d[x, z] = rgbc
    #             break
    #     return self

    # def make_3d_template_render(self, template, color_map=None, xs=0, ys=0, zs=0):
    #     self._setup_template_render(color_map)
    #
    #     yl, xl, zl = template.shape
    #
    #     self._render_3d = []
    #
    #     for x, y, z in loop3d(xl, yl, zl):
    #         blockID = template.get_block(x, y, z)
    #         if blockID is None:
    #             continue
    #         if blockID not in IDENTIFIER_TO_TEXTURES and blockID not in SIMPLE_TEXTURES:
    #             print(blockID, 'not textured')
    #             continue
    #
    #         cube = self._render_cube(blockID, x + x * xs, y + y * ys, z + z * zs)
    #
    #         self._render_3d.append(cube)
    #     return self
    #
    # def make_3d_vox_render(self, vox_model, palette, xs=0, ys=0, zs=0):
    #     yl, xl, zl = vox_model.shape
    #
    #     self._render_3d = o3d.geometry.TriangleMesh()
    #     for x, y, z in loop3d(xl, yl, zl):
    #         color_index = vox_model[y][x][z]
    #         hex_color = palette[color_index]
    #         if hex_color == 0x00:
    #             continue
    #         rgbc = self.rgb_hex_to_float_rgb(hex_color)
    #         cube = o3d.geometry.TriangleMesh.create_box(width=1, height=1, depth=1)
    #         cube.paint_uniform_color(rgbc)
    #         cube.translate([x + x * xs, y + y * ys, z + z * zs], relative=False)
    #         self._render_3d += cube
    #     return self

