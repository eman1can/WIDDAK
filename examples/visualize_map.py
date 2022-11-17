# Path Fixing Code - Must Be First
from os import getcwd, environ, chdir, listdir, makedirs
from os.path import exists, isdir, split, join

# Start Path Fixing Code
# Ensure that no local imports are before this!
script_path = getcwd()
while not script_path.endswith('WIDDAK'):
    script_path = split(script_path)[0]
    chdir(script_path)
if 'PYTHONPATH' in environ:
    if script_path + ';' not in environ['PYTHONPATH']:
        environ['PYTHONPATH'] += script_path + ';'
else:
    environ['PYTHONPATH'] = script_path
# End Path Fixing Code

from gdpc.vector_util import Box, Rect
from gdpc.interface import getWorldSlice
from gdpc.renderer import Renderer

build_area = Box.from_box(0, 0, 0, 512, 256, 512)  # Optionally, Use build_area = getBuildArea()
use_saved_world = True
if use_saved_world:
    if not exists(join('local', 'worlds')):
        print('You have no saved worlds! Use scripts/create_saved_world.pv')
        exit(1)
    print(listdir(join('local', 'worlds')))
    worlds = [join('local', 'worlds', x, 'edit') for x in listdir(join('local', 'worlds')) if isdir(join('local', 'worlds', x))]
    if len(worlds) == 0:
        print('You have no saved worlds! Use scripts/create_saved_world.pv')
        exit(1)
    world_slice = getWorldSlice(build_area.toRect(), worlds[-1])
else:
    world_slice = getWorldSlice(build_area.toRect())

render_path = join('local', 'renders', 'world')
if not exists(render_path):
    makedirs(render_path)

# Send data to renderer
renderer = Renderer()
if exists('C:/IrfanView/i_view64.exe'):
    renderer.set_default_viewer()  # Set to Irfanview by default

renderer.make_2d_surface_render(build_area.toRect(), world_slice)
renderer.save_2d_render(join(render_path, 'surface.tiff')) # .show_2d_render()
#
renderer.make_2d_topographic_render(build_area.toRect(), world_slice)
renderer.save_2d_render(join(render_path, 'topographic.tiff')) # .show_2d_render()

renderer.make_2d_surface_biome_render(build_area.toRect(), world_slice)
renderer.save_2d_render(join(render_path, 'biome.tiff')) # .show_2d_render()

renderer.make_2d_topographic_biome_render(build_area.toRect(), world_slice)
renderer.save_2d_render(join(render_path, 'biome_topographic.tiff')) # .show_2d_render()