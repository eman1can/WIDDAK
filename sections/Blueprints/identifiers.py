from os.path import exists, join

from bs4 import BeautifulSoup
from urllib.request import urlopen


ID_TO_NAME = None
NAME_TO_ID = None

name_data_file = join('blueprints', 'ID_Name_Data.html')

# https://minecraftitemids.com
def parse_items(debug=True):
    if not exists(name_data_file):
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
        # Add Slab Variants
        if 'Slab' in name:
            name_to_identifier[f'Double {name}'] = f'double_{identifier}'
            if debug:
                print(f'Double {name}'.ljust(30), '->', f'double_{identifier}')
        name_to_identifier[name] = identifier
        if debug:
            print(name.ljust(30), '->', identifier)
    # Add All the Potted Plants
    plants = ['Potted Cactus', 'Potted Dead Bush', 'Potted Dandelion', 'Potted Spruce Sapling', 'Potted Oak Sapling', 'Potted Poppy']
    for plant_name in plants:
        identifier = plant_name.lower().replace(' ', '_')
        name_to_identifier[plant_name] = identifier

    identifier_to_name = {v: k for k, v in name_to_identifier.items()}

    return name_to_identifier, identifier_to_name


if ID_TO_NAME is None or NAME_TO_ID is None:
    NAME_TO_ID, ID_TO_NAME = parse_items(False)
