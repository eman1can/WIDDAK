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

from bs4 import BeautifulSoup
from urllib.request import urlopen

from gdpc.lookup import BIOMES_NAME_TO_INDEX
from gdpc.template import Template

from .identifiers import NAME_TO_ID

import json



"""
On HTML Page

buttons = document.getElementsByClassName('load-page-button')
for (let index = 43; index < 183; index++) {
    buttons[index].children[0].click()
}
# Wait for page to load, and download
# Village_Plains.html
location.reload()
buttons = document.getElementsByClassName('load-page-button')
for (let index = 43; index < 77; index++) {
    buttons[index].children[0].click()
}

"""

TRAPDOORS = ['minecraft:acacia_trapdoor', 'minecraft:birch_trapdoor', 'minecraft:dark_oak_trapdoor', 'minecraft:oak_trapdoor', 'minecraft:spruce_trapdoor', 'minecraft:warped_trapdoor', 'minecraft:crimson_trapdoor',
                                         'minecraft:iron_trapdoor', 'minecraft:jungle_trapdoor']
FENCES = ['minecraft:acacia_fence', 'minecraft:birch_fence', 'minecraft:dark_oak_fence', 'minecraft:oak_fence', 'minecraft:spruce_fence', 'minecraft:warped_fence', 'minecraft:crimson_fence', 'minecraft:jungle_fence']
FENCE_GATES = ['minecraft:acacia_fence_gate', 'minecraft:birch_fence_gate', 'minecraft:dark_oak_fence_gate', 'minecraft:oak_fence_gate', 'minecraft:spruce_fence_gate', 'minecraft:warped_fence_gate',
               'minecraft:crimson_fence_gate', 'minecraft:jungle_fence_gate']

facing_fences = []
for fence in FENCES:
    facing_fences.append(f'{fence}[facing=north]')
    facing_fences.append(f'{fence}[facing=south]')
    facing_fences.append(f'{fence}[facing=east]')
    facing_fences.append(f'{fence}[facing=west]')
FENCES += facing_fences
facing_fence_gates = []
for fence_gate in FENCE_GATES:
    facing_fence_gates.append(f'{fence_gate}[facing=north]')
    facing_fence_gates.append(f'{fence_gate}[facing=south]')
    facing_fence_gates.append(f'{fence_gate}[facing=east]')
    facing_fence_gates.append(f'{fence_gate}[facing=west]')
FENCE_GATES += facing_fence_gates

# TODO: Detect Templates that are identical by block placement, but vary with style
# Ex. The same 3x3 house but with spruce instead of oak
# And add a section to the Template class to have variations stores as indexes, and accessed with array accessors
# With the default template being variation 0


class BuildingParser:
    def __init__(self):
        self.not_found = []
        self.templates = []

    def parse_json(self):
        # Load Building Templates from JSON
        with open(join('blueprints', 'building_templates.json'), "r") as file:
            self.templates = json.load(file)
        return self.templates

    def parse_wiki_pages(self):
        # Parse All Building Templates
        self.templates = self.parse_building_list(NAME_TO_ID, False)
        # Save Templates to JSON
        with open(join('blueprints', 'building_templates.json'), "w") as file:
            json_string = json.dumps(self.templates)
            indent = 0
            for ix, char in enumerate(json_string):
                if char == ' ' and json_string[ix + 1] == '[' and json_string[ix - 1] == ',' and json_string[ix - 3] != ']':
                    continue
                if char == ' ' and json_string[ix - 1] == ',' and json_string[ix + 1] == '"' and json_string[ix - 2] in ('}', ']'):
                    continue
                file.write(char)
                if ix == len(json_string) - 1:
                    continue
                if char == '{':
                    file.write('\n')
                    indent += 1
                    file.write('\t' * indent)
                if char == '[' and json_string[ix + 1] == '[':
                    file.write('\n')
                    indent += 1
                    file.write('\t' * indent)
                if char == ',' and json_string[ix - 1] == ']' and json_string[ix - 2] != ']':
                    file.write('\n')
                    file.write('\t' * indent)
                if char == ']' and json_string[ix + 1] in (']', '}'):
                    file.write('\n')
                    indent -= 1
                    file.write('\t' * indent)
                if char == ',' and json_string[ix + 2] == '"' and json_string[ix - 1] in ('}', ']'):
                    file.write('\n')
                    file.write('\t' * indent)

        return self.templates

    def get_templates(self):
        templates = {}
        for biome_index, template_list in self.templates.items():
            templates[biome_index] = {}
            for template_name, variation_list in template_list.items():
                templates[biome_index][template_name] = {}
                for variation_index, building_template in variation_list.items():
                    templates[biome_index][template_name][variation_index] = Template(template_name, biome_index, variation_index, building_template)
        return templates

    def get_tname(self, tile):
        if tile is None:
            return '-'
        output = ''
        for c in tile:
            if 'A' < c < 'Z':
                output += c
        return output

    def parse_material_table(self, table, debug=True):
        headers = table.find_all('th')
        data = table.find_all('td')

        columns = len(headers)
        rows = len(data) // columns

        # Generate the output Dict
        table_data = {}
        for cix in range(columns):
            header = headers[cix].text.strip()
            values = [data[rix * columns + cix].text.strip() for rix in range(rows)]
            table_data[header] = values

        output = {}
        for rix, block_name in enumerate(table_data['Name']):
            layer_counts = []
            for lix in range(0, columns - 1):
                if lix == columns - 2:
                    v = table_data['Total'][rix]
                else:
                    if 'Layer 0' in table_data:
                        v = table_data[f'Layer {lix}'][rix]
                    else:
                        v = table_data[f'Layer {lix + 1}'][rix]
                if '\u200c' in v or '\\u200c' in v:
                    count = int(v[:v.replace('\\u200c', '\u200c').index('\u200c')])
                elif v in ('—', '-', ''):
                    count = 0
                elif '.' in v:
                    count = int(float(v))
                else:
                    count = int(v)
                layer_counts.append(count)
            output[block_name] = layer_counts

        if debug:
            # Get printing spacing
            spacing = [0 for _ in range(columns)]
            for cix, header in enumerate(table_data.keys()):
                spacing[cix] = max(spacing[cix], len(header))
                for value in table_data[header]:
                    spacing[cix] = max(spacing[cix], len(value))
                spacing[cix] += 2

            # Print to a table
            for cix, header in enumerate(table_data.keys()):
                print(header.ljust(spacing[cix]), end='')
            print()
            for rix in range(rows):
                for cix, values in enumerate(table_data.values()):
                    print(values[rix].ljust(spacing[cix]), end='')
                print()
        return output

    def parse_layered_blueprint(self, blueprint, debug=True):
        layer_blocks = blueprint.find_all('div', attrs={'class': 'layered-blueprint-layer'})

        rows = 0
        cols = 0

        output = {}
        for lix, layer in enumerate(layer_blocks):
            layer_name = f'Layer {lix + 1}'
            output[layer_name] = []
            for row in layer.find_all('tr'):
                output[layer_name].append([])
                for col in row.find_all('td'):
                    tile = col.find('a')
                    output[layer_name][-1].append(tile['title'] if tile is not None else None)

            rows = max(rows, len(output[layer_name]))
            for row in output[layer_name]:
                cols = max(cols, len(row))

            if debug:
                print(layer_name)
                for row in output[layer_name]:
                    print(end='\t')
                    for col in row:
                        print(self.get_tname(col).ljust(3), end=' ')
                    print()
                print()

        # Ensure all rows and columns are square
        for layer_name in output.keys():
            while len(output[layer_name]) != rows:
                output[layer_name].append([None for _ in range(cols)])
            for rix in range(rows):
                while len(output[layer_name][rix]) != cols:
                    output[layer_name][rix].append(None)

        return output

    def get_material_name(self, item_dictionary, material):
        if material[:-1] in item_dictionary:
            return material[:-1]  # Detect Plurals
        if material.replace('Wood ', '') in item_dictionary:
            return material.replace('Wood ', '')  # Detect Woods
        if material.replace('Wood ', '')[:-1] in item_dictionary:
            return material.replace('Wood ', '')[:-1]  # Detect Plural Woods
        if material.replace('Wood', 'Log') in item_dictionary:
            return material.replace('Wood', 'Log')  # Detect Mislabeled Logs
        if material + ' Block' in item_dictionary:
            return material + ' Block'
        if 'Block of ' + material in item_dictionary:
            return 'Block of ' + material
        if '\u200c' in material or '\\u200c' in material:
            return material[:material.replace('\\u200c', '\u200c').index('\u200c')]
        if f'minecraft:{material.lower().replace(" ", "_")}' in item_dictionary.values():
            key = f'minecraft:{material.lower().replace(" ", "_")}'
            index = list(item_dictionary.values()).index(key)
            return list(item_dictionary.keys())[index]
        if material == 'Wall Torch':
            return 'Torch'
        if material == 'Hay Block':
            return 'Hay Bale'
        if material == 'Grass Path':
            return 'Dirt Path'
        if material == 'Waterlogged Smooth Sandstone Stairs':
            return 'Smooth Sandstone Stairs'
        if material == 'Crafting':
            return 'Crafting Table'
        if material not in self.not_found:
            print(f'[WARN] {material} not found')
            self.not_found.append(material)
        return None

    def parse_building_list(self, item_dictionary, debug=True):
        with open('blueprints/Village_Structure_Blueprints.html', 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')

        blueprint_data = soup.find('div', attrs={'class': 'mw-parser-output'})
        titles = blueprint_data.find_all('h2', recursive=False)
        # block_lists = {}

        building_templates = {}
        for biome in titles:
            biome_name = biome_key = str(biome.text[:-2])
            if ' ' in biome_name:
                biome_key = biome_name[:biome_name.index(' ')]
            buildings = [b for b in blueprint_data.find_all('div', attrs={'class': 'load-page'}) if str(biome_key) in b['data-page']]
            if debug:
                print(biome_name, '-', len(buildings))

            biome_index = BIOMES_NAME_TO_INDEX[biome_name.lower().replace(' ', '_')]

            building_templates[biome_index] = {}
            for building in buildings:
                key = building['data-page'][building['data-page'].rindex('/') + 1:]
                name = key[:-len(' blueprint')].title()
                key = key.replace(' ', '_')
                if not exists(f'blueprints/buildings/{key}.html'):
                    link = f'https://minecraft.fandom.com/wiki/Village/Structure/Blueprints/{key}'
                    print('\t' + name, link)
                    with urlopen(link) as page_stream:
                        page = page_stream.read()
                    with open(f'blueprints/buildings/{key}.html', 'wb') as building_file:
                        building_file.write(page)
                else:
                    with open(f'blueprints/buildings/{key}.html', 'rb') as building_file:
                        page = building_file.read()

                building_data = BeautifulSoup(page, 'html.parser')

                building_name = name[len(biome_key) + 1:]
                try:
                    variation_index = building_name.rindex(' ')
                    variation = int(building_name[variation_index + 1:]) - 1
                    building_name = building_name[:variation_index]
                except ValueError:
                    variation = 0

                # material_table = building_data.find('table', attrs={'class': 'wikitable'})
                #
                # materials = self.parse_material_table(material_table, False)
                #
                # material_ids = []
                # for material in list(materials.keys()):
                #     material_key = self.get_material_name(item_dictionary, material)
                #     if material_key is None:
                #         continue
                #     material_ids.append(item_dictionary[material_key])
                # block_lists[key] = material_ids

                layered_blueprint = building_data.find('div', attrs={'class': 'layered-blueprint'})
                layers = self.parse_layered_blueprint(layered_blueprint, False)

                layer_template = []
                for layer_key in list(layers.keys()):
                    layer_blocks = layers[layer_key]
                    for i in range(len(layer_blocks)):
                        for j in range(len(layer_blocks[i])):
                            if layer_blocks[i][j] is None:
                                continue
                            title = layer_blocks[i][j].title()
                            material_name = self.get_material_name(item_dictionary, title)
                            layer_blocks[i][j] = item_dictionary.get(material_name)

                    # Do NBT Data
                    for i in range(len(layer_blocks)):
                        for j in range(len(layer_blocks[i])):
                            if layer_blocks[i][j] is None:
                                continue
                            blockID = layer_blocks[i][j]

                            # Add NBT Data to edge items
                            if i == 0:
                                if blockID in TRAPDOORS:
                                    layer_blocks[i][j] = f'{blockID}[facing=south]'
                            elif i == len(layer_blocks) - 1:
                                if blockID in TRAPDOORS:
                                    layer_blocks[i][j] = f'{blockID}[facing=north]'
                            elif j == 0:
                                if blockID in TRAPDOORS:
                                    layer_blocks[i][j] = f'{blockID}[facing=east]'
                            elif j == len(layer_blocks[i]) - 1:
                                if blockID in TRAPDOORS:
                                    layer_blocks[i][j] = f'{blockID}[facing=west]'

                            # Add NBT Data for Fences
                            if blockID in FENCES + FENCE_GATES:
                                if 0 < i < len(layer_blocks) - 1:
                                    if layer_blocks[i + 1][j] in FENCES + FENCE_GATES and layer_blocks[i - 1][j] in FENCES + FENCE_GATES:
                                        layer_blocks[i][j] = f'{blockID}[facing=east]'


                    layer_template.append(layer_blocks)
                if building_name not in building_templates[biome_index]:
                    building_templates[biome_index][building_name] = {}
                building_templates[biome_index][building_name][variation] = layer_template

        return building_templates
