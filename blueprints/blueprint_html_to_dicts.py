from os.path import exists

from bs4 import BeautifulSoup
from urllib.request import urlopen
from buildings import *
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

NOT_FOUND = []

def parse_material_table(table, debug=True):
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


def get_tname(tile):
    if tile is None:
        return '-'
    output = ''
    for c in tile:
        if 'A' < c < 'Z':
            output += c
    return output


def parse_layered_blueprint(blueprint, debug=True):
    layer_blocks = blueprint.find_all('div', attrs={'class': 'layered-blueprint-layer'})
    output = {}
    for lix, layer in enumerate(layer_blocks):
        layer_name = f'Layer {lix + 1}'
        output[layer_name] = []
        for row in layer.find_all('tr'):
            output[layer_name].append([])
            for col in row.find_all('td'):
                tile = col.find('a')
                output[layer_name][-1].append(tile['title'] if tile is not None else None)
        rows = len(output[layer_name])
        cols = 0
        for row in output[layer_name]:
            cols = max(cols, len(row))
        for rix in range(rows):
            while len(output[layer_name][rix]) != cols:
                output[layer_name][rix].append(None)
        if debug:
            print(layer_name)
            for row in output[layer_name]:
                print(end='\t')
                for col in row:
                    print(get_tname(col).ljust(3), end=' ')
                print()
            print()
    return output


def get_material_key(item_dictionary, material):
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
    if material not in NOT_FOUND:
        print(f'[WARN] {material} not found')
        NOT_FOUND.append(material)
    return None

def parse_building_list(item_dictionary):
    with open('blueprints/Village_Structure_Blueprints.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')

    blueprint_data = soup.find('div', attrs={'class': 'mw-parser-output'})
    titles = blueprint_data.find_all('h2', recursive=False)
    block_lists = {}
    for biome in titles:
        biome_name = str(biome.text[:-2])
        if ' ' in biome_name:
            biome_name = biome_name[:biome_name.index(' ')]
        buildings = [b for b in blueprint_data.find_all('div', attrs={'class': 'load-page'}) if str(biome_name) in b['data-page']]
        print(biome_name, '-', len(buildings))

        building_templates = {}
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

            material_table = building_data.find('table', attrs={'class': 'wikitable'})
            layered_blueprint = building_data.find('div', attrs={'class': 'layered-blueprint'})

            materials = parse_material_table(material_table, False)
            layers = parse_layered_blueprint(layered_blueprint, False)

            # TODO: If Want to Use Blueprints, access layers and materials
            material_ids = []
            for material in list(materials.keys()):
                material_key = get_material_key(item_dictionary, material)
                if material_key is None:
                    continue
                material_ids.append(item_dictionary[material_key])
            block_lists[key] = material_ids

            # TODO: If Want to Use Blueprints, access layers and materials
            material_ids = []
            for material in list(materials.keys()):
                material_key = get_material_key(item_dictionary, material)
                if material_key is None:
                    continue
                material_ids.append(item_dictionary[material_key])
            block_lists[key] = material_ids

            layer_template = []
            for layer_key in list(layers.keys()):
                layer_blocks = layers[layer_key]
                for i in range(len(layer_blocks)):
                    for j in range(len(layer_blocks[i])):
                        if (layer_blocks[i][j] is None): continue
                        title = layer_blocks[i][j].title()
                        if title == 'Double Smooth Stone Slab':
                            material_key = 'double_stone_slab'
                        elif 'Cauldron' in title:
                            material_key = 'cauldron'
                        else:
                            material_key = item_dictionary.get(get_material_key(item_dictionary, title))   
                        material_key = material_key.replace('dirt_path', 'grass_path')
                        layer_blocks[i][j] = material_key
                layer_template.append(layer_blocks)
            building_templates[key] = layer_template
        return building_templates


            

    # Fold Buildings into single lists
    output = {}
    for key in block_lists.keys():
        biome_name = key[:key.index('_')].lower()
        simple_name = key[key.index('_') + 1:].lower()  # Skip Biome Name
        if simple_name.startswith('small') or simple_name.startswith('medium') or simple_name.startswith('large'):
            simple_name = simple_name[simple_name.index('_') + 1:]
        if simple_name.endswith('blueprint'):
            simple_name = simple_name[:simple_name.rindex('_')]
        if simple_name[-2] == '_' or simple_name[-3] == '_':
            simple_name = simple_name[:simple_name.rindex('_')]
        okey = f'{biome_name}_village_{simple_name}'
        if okey in output:
            output[okey] += block_lists[key]
        else:
            output[okey] = block_lists[key]
    return output

# https://minecraftitemids.com
def parse_items(debug=True):
    if not exists('ID_Name_Data.html'):
        with urlopen('https://minecraftitemids.com') as page_stream:
            page = page_stream.read()
        page_soup = BeautifulSoup(page, 'html.parser')
        table_data = page_soup.find('table', attrs={'class': 'rd-table'}).find('tbody')
        page_count = page_soup.find_all('a', attrs={'class': 'rd-pagination__button'})[-2].text.strip()
        with open('ID_Name_Data.html', 'w') as file:
            file.write('<html>')
            file.write(f'<!-- 1 -->{table_data}')
            for pix in range(2, int(page_count) + 1):
                with urlopen(f'https://minecraftitemids.com/{pix}') as page_stream:
                    page = page_stream.read()
                page_soup = BeautifulSoup(page, 'html.parser')
                table_data = page_soup.find('table', attrs={'class': 'rd-table'}).find('tbody')
                file.write(f'<!-- {pix} -->{table_data}')
            file.write('</html>')

    with open('ID_Name_Data.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')

    items = soup.find_all('tr')
    name_to_identifier = {}
    identifier_to_name = {}
    for item in items[1:]:
        elements = item.find_all('a')
        if len(elements) == 1:
            name = elements[0].text.strip()
        else:
            name = elements[1].text.strip()
        identifier = item.find('span').text.strip()
        if name == 'Clay' and identifier == 'minecraft:clay':
            name = 'Clay Block'
        name_to_identifier[name] = identifier
        identifier_to_name[identifier] = name
        if debug:
            print(name.ljust(30), '->', identifier)
    # Add All the Potted Plants
    plants = ['Potted Cactus', 'Potted Dead Bush', 'Potted Dandelion', 'Potted Spruce Sapling', 'Potted Oak Sapling', 'Potted Poppy']
    for plant_name in plants:
        identifier = plant_name.lower().replace(' ', '_')
        name_to_identifier[plant_name] = identifier
        identifier_to_name[identifier] = plant_name
    return name_to_identifier, identifier_to_name


def output_code(buildings):
    buildings_by_biome = {}
    for building, materials in buildings.items():
        biome_name = building[:building.index('_')]
        building_name = building[building.index('_') + 1:]
        if biome_name in buildings_by_biome:
            buildings_by_biome[biome_name][building_name] = materials
        else:
            buildings_by_biome[biome_name] = {building_name: materials}

    # for biome_name, buildings in buildings_by_biome.items():
    #     for building_name, materials in buildings.items():
    #         key = f'{biome_name}_{building_name}'.upper()
    #         if 'minecraft:water' in materials:
    #             materials.remove('minecraft:water')
    #             print(key + ' = {"' + '", "'.join(set(materials)) + '"} | WATERS')
    #         else:
    #             print(key + ' = {"' + '", "'.join(set(materials)) + '"}')
    #     print(f'{biome_name}_village_blocks'.upper() + ' = ' + ' | '.join([f'{biome_name}_{b}'.upper() for b in buildings.keys()]))
    # print('VILLAGE_BLOCKS = PLAINS_VILLAGE_BLOCKS | DESERT_VILLAGE_BLOCKS | SAVANNA_VILLAGE_BLOCKS | TAIGA_VILLAGE_BLOCKS | SNOWY_VILLAGE_BLOCKS')


# if __name__ == "__main__":
#     print('Parsing Names and Identifiers')
#     name_to_id, id_to_name = parse_items(False)
#     print('Parsing Structures')
#     building_list = parse_building_list(name_to_id)
#     print(building_list)
#     # print('Building Code')
#     # output_code(building_list)

def get_building_templates():
    name_to_id, id_to_name = parse_items(False)
    building_list = parse_building_list(name_to_id)
    return building_list

templates = get_building_templates()
print('templates', templates)

# save building templates 
with open("blueprints/building_templates.json", "w") as outfile:
    outfile.write(json.dumps(templates))