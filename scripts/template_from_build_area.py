from os.path import join

from gdpc.interface import getBuildArea, getWorldSlice
from gdpc.template import Template

buildArea = getBuildArea()
world_slice = getWorldSlice(buildArea.toRect())

template_name = 'Rustic Cabin'
template = Template.from_world_slice(template_name, world_slice, buildArea)

# Ensure that you have the right bounds!
print(template.to_string())

template_path = join('local', 'templates', template_name.lower().replace(' ', '_'))
template.to_file(template_path)

# Example of loading
# rustic_cabin = Template.from_file(template_path)
