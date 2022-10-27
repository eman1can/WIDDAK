# Path Fixing Code - Must Be First
from os import getcwd, environ, chdir
from os.path import exists, split, join

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

build_area = getBuildArea()  # Optionally, Use build_area = Rect.from_rect(0, 0, 128, 128)
world_slice = getWorldSlice(build_area)

# If the world slice does not exist, then save it
if save_world and not exists(join(path, world_name)):
    world_slice.to_file(world_name, world_name_minecraft, path, 64)

# Send data to renderer
renderer = Renderer()
renderer.set_default_viewer()  # Set to Irfanview by default
renderer.make_2d_world_render(build_area, world_slice)
renderer.show_2d_render()

