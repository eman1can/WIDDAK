# Path Fixing Code - Must Be First
from os import getcwd, environ, chdir, makedirs
from os.path import exists, split, join

from gdpc.vector_util import Box, Rect

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

from gdpc.interface import getBuildArea, getWorldSlice
from gdpc.renderer import Renderer

save_world = False
path = join('local', 'worlds')  # This is the location the world will be saved
world_name = 'TestWorld1763'  # This is what the world will be named on disk
world_name_minecraft = 'Test World'  # This is what you named the world in minecraft

build_area = Box.from_box(0, 0, 0, 512, 256, 512)  # Optionally, Use build_area = Box.from_box(0, 0, 0, 128, 256, 128)
world_slice = getWorldSlice(build_area.toRect())

# If the world slice does not exist, then save it
if save_world and not exists(join(path, world_name)):
    world_slice.to_file(world_name, world_name_minecraft, path, 64)

render_path = join('local', 'renders', 'world')
if not exists(render_path):
    makedirs(render_path)

# Send data to renderer
renderer = Renderer()
if exists('C:/IrfanView/i_view64.exe'):
    renderer.set_default_viewer()  # Set to Irfanview by default

renderer.make_2d_world_render(build_area.toRect(), world_slice)
renderer.save_2d_render(join(render_path, 'surface.tiff')).show_2d_render()

renderer.make_2d_topographic_render(build_area.toRect(), world_slice)
renderer.save_2d_render(join(render_path, 'topographic.tiff')).show_2d_render()

renderer.make_2d_surface_biome_render(build_area.toRect(), world_slice)
renderer.save_2d_render(join(render_path, 'biome.tiff')).show_2d_render()