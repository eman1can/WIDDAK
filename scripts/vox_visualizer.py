# Path Fixing Code - Must Be First
from os import getcwd, environ, chdir, listdir, makedirs
from os.path import split, join, exists

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

from gdpc.renderer import Renderer
from src.vox import VoxFile

vox_render_path = join('local', 'renders', 'vox')
if not exists(vox_render_path):
    makedirs(vox_render_path)

renderer = Renderer()
renderer.set_default_viewer()

vox_file_directory = join('blueprints', 'vox')
for vox_file_name in listdir(vox_file_directory):
    vox_file = VoxFile(join(vox_file_directory, vox_file_name))
    vox_file.read()
    vox_file.close()

    palette = vox_file.get_color_palette()
    for model in vox_file.get_models():
        renderer.make_3d_vox_render(model, palette)
        renderer.save_3d_render(join(vox_render_path, vox_file_name[:-3] + 'ply'))
        renderer.save_3d_render_as_image(join(vox_render_path, vox_file_name[:-3] + 'png'))
