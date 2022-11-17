from os.path import join

from glm import ivec3

from gdpc.interface import getBuildArea, getWorldSlice
from gdpc.template import Template

build_area = getBuildArea()
world_slice = getWorldSlice(build_area.toRect())

for x, y, z in build_area.loop():
    block = world_slice.get_block_data_at(ivec3(x, y, z))

    print(f'Block Name: ', block.namespaced_name)

template_name = 'Rustic Cabin'
template = Template.from_world_slice(template_name, world_slice, build_area)

# Ensure that you have the right bounds!
print(template.to_string())

template_path = join('local', 'templates', template_name.lower().replace(' ', '_'))
template.to_file(template_path)

# Example of loading
# rustic_cabin = Template.from_file(template_path)
