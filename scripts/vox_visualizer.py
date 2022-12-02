from fix_file_path import *
from os import listdir, makedirs
from os.path import join, exists

from gdpc.renderer import Renderer
from src.vox import VoxFile

vox_render_path = join('local', 'renders', 'vox')
if not exists(vox_render_path):
    makedirs(vox_render_path)

renderer = Renderer()
renderer.set_default_viewer()

vox_file_directory = join('blueprints', 'vox')
for vox_file_name in listdir(vox_file_directory):
    vox_file = VoxFile.from_file(join(vox_file_directory, vox_file_name))

    palette = vox_file.get_color_palette()
    for model in vox_file.get_models():
        renderer.make_3d_vox_render(model, palette)
        renderer.save_3d_render(join(vox_render_path, vox_file_name[:-3] + 'ply'))
        renderer.save_3d_render_as_image(join(vox_render_path, vox_file_name[:-3] + 'png'))
