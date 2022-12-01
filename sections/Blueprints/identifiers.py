from os.path import exists, join

from bs4 import BeautifulSoup
from urllib.request import urlopen


ID_TO_NAME = None
NAME_TO_ID = None

name_data_file = join('sections', 'Blueprints', 'ID_Name_Data.html')

# https://minecraftitemids.com
def parse_items(debug=True):
    print(exists(name_data_file))
    if not exists(name_data_file):
        print('Fix your pathing!!')
        exit(1)
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

    with open(name_data_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')

    items = soup.find_all('tr')
    name_to_identifier = {}
    for item in items[1:]:
        elements = item.find_all('a')
        if len(elements) == 1:
            name = elements[0].text.strip()
        else:
            name = elements[1].text.strip()
        identifier = item.find('span').text.strip()
        if name == 'Clay' and identifier == 'minecraft:clay':
            name = 'Clay Block'
        # Add Slab Variants
        if 'Slab' in name:
            name_to_identifier[f'Double {name}'] = 'minecraft:double_' + identifier[len('minecraft:'):]
            if debug:
                print(f'Double {name}'.ljust(30), '->', 'minecraft:double_' + identifier[len('minecraft:'):])
        name_to_identifier[name] = identifier
        if debug:
            print(name.ljust(30), '->', identifier)
    # Add All the Potted Plants
    plants = ['Potted Cactus', 'Potted Dead Bush', 'Potted Dandelion', 'Potted Spruce Sapling', 'Potted Oak Sapling', 'Potted Poppy']
    for plant_name in plants:
        identifier = plant_name.lower().replace(' ', '_')
        name_to_identifier[plant_name] = identifier

    # Add Air...
    name_to_identifier["Air"] = 'minecraft:air'

    identifier_to_name = {v: k for k, v in name_to_identifier.items()}

    return name_to_identifier, identifier_to_name


if ID_TO_NAME is None or NAME_TO_ID is None:
    NAME_TO_ID, ID_TO_NAME = parse_items(False)

# ids = list(ID_TO_NAME.keys())
# # Print Planks
# excluded = []
# wools = [x for x in ids if 'wool' in x]
# carpets = [x for x in ids if 'carpet' in x]
# slabs = [x for x in ids if 'slab' in x and 'double' not in x]
# pressure_plates = [x for x in ids if 'pressure_plate' in x]
# fences = [x for x in ids if 'fence' in x and 'gate' not in x]
# fence_gates = [x for x in ids if 'gate' in x]
# walls = [x for x in ids if 'wall' in x and 'sign' not in x and 'head' not in x and 'banner' not in x]
# signs = [x for x in ids if 'sign' in x and 'wall' not in x]
# heads = [x for x in ids if 'head' in x and 'wall' not in x and 'piston' not in x]
# banners = [x for x in ids if 'banner' in x and 'wall' not in x]
# wall_signs = [x for x in ids if 'sign' in x and 'wall' in x]
# wall_heads = [x for x in ids if 'head' in x and 'wall' in x]
# wall_banners = [x for x in ids if 'banner' in x and 'wall' in x]
# stairs = [x for x in ids if 'stairs' in x]
# rails = [x for x in ids if 'rail' in x]
# blocks = [x for x in ids if 'block' in x]
# buttons = [x for x in ids if 'button' in x]
# trapdoors = [x for x in ids if 'trapdoor' in x]
# doors = [x for x in ids if 'door' in x and 'trapdoor' not in x]
# concrete = [x for x in ids if 'concrete' in x]
# excluded += wools + carpets + slabs + fences + fence_gates + walls + signs + heads + banners
# excluded += wall_signs + wall_heads + wall_banners + rails + stairs + buttons + pressure_plates + trapdoors + doors + concrete
# other = [x for x in ids if x not in excluded]
#
# for wood in ['oak', 'birch', 'spruce', 'jungle', 'acacia', 'warped', 'crimson']:
#     wood_items = [x for x in ids if wood in x and x not in excluded]
#     print(wood_items)
#
# for ore in ['coal', 'iron', 'copper', 'gold', 'redstone', 'diamond', 'emerald', 'lapis', 'quartz']:
#     print([x for x in ids if ore in x])
#
# print(wools)
# print(carpets)
# print(pressure_plates)
# print(slabs)
# print(trapdoors)
# print(doors)
# print(fences)
# print(fence_gates)
# print(walls)
# print(heads)
# print(banners)
# print(signs)
# print(wall_signs)
# print(wall_heads)
# print(stairs)
# print(rails)
# print(blocks)
# print(concrete)
# print(other)
#
