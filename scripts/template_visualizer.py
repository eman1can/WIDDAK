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

from sections.Blueprints.blueprints import BuildingParser
from gdpc.renderer import Renderer

renderer = Renderer()
renderer.set_default_viewer()

parser = BuildingParser()
parser.parse_json()
templates = parser.get_templates()

render_path = join('renders', 'buildings')
if not exists(render_path):
    makedirs(render_path)

for biome_index in templates.keys():
    for template_name in templates[biome_index].keys():
        for variation_index, template in templates[biome_index][template_name].items():
            renderer.make_3d_template_render(template)
            xl, yl, zl = template.shape
            # if int(biome_index) == 1 and template_name == 'Animal Pen' and int(variation_index) == 2:
            renderer.show_3d_render()  # .save_3d_render_as_image(join(render_path, template.get_id() + '.png'), x=xl*1.5, y=yl, z=zl*1.5)
