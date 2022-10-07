from os import listdir, mkdir
from os.path import exists, join

from gdpceu.renderer import Renderer
from gdpceu.vox import VoxFile

renders_path = 'renders'
if not exists(renders_path):
    mkdir(renders_path)

vox_render_path = join(renders_path, 'vox')
if not exists(vox_render_path):
    mkdir(vox_render_path)

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
        renderer.save_3d_render(join(vox_render_path, vox_file_name))
