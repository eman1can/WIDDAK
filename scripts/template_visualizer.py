from os import mkdir
from os.path import exists, join

from gdpceu.blueprints import BuildingParser
from gdpceu.renderer import Renderer
from gdpceu.template import Template

renderer = Renderer()
renderer.set_default_viewer()

parser = BuildingParser()
parser.parse_wiki_pages()
templates = parser.get_templates()

if not exists('renders'):
    mkdir('renders')

render_path = join('renders', 'buildings')
if not exists(render_path):
    mkdir(render_path)

for biome_index in templates.keys():
    for template_name in templates[biome_index].keys():
        for variation_index, template in templates[biome_index][template_name].items():
            renderer.make_3d_template_render(template)
            xl, yl, zl = template.shape
            # if int(biome_index) == 1 and template_name == 'Animal Pen' and int(variation_index) == 2:
            renderer.show_3d_render()  # .save_3d_render_as_image(join(render_path, template.get_id() + '.png'), x=xl*1.5, y=yl, z=zl*1.5)
