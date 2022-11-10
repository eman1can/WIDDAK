
import sys
from os import getcwd, environ, chdir, listdir, makedirs
from os.path import split, join, exists

script_path = getcwd()
sys.path.append(script_path)
while not script_path.endswith('WIDDAK'):
    script_path = split(script_path)[0]
    chdir(script_path)
if 'PYTHONPATH' in environ:
    if script_path + ';' not in environ['PYTHONPATH']:
        environ['PYTHONPATH'] += script_path + ';'
else:
    environ['PYTHONPATH'] = script_path

from bs4 import BeautifulSoup as bs
import requests
from gdpc.lookup import PALETTE

PALETTELOOKUP = {}
for hexval, blocks in PALETTE.items():
    for block in blocks:
        PALETTELOOKUP[block] = hex(hexval)


HEX_COLORS = {}
TAKEN_COLORS = set()
ALT_COLORS = {}

# Get a similar color to the provided hexcode that isn't already taken
def get_similar_color(color):
    try:
        # If the html page was already loaded, use it
        alternative_colors = []
        if ALT_COLORS.get(color):
            alternative_colors = ALT_COLORS[color]
        # Else, scrape the colorhexa website for similar colors
        else:
            color_code = color.split('x')[1].zfill(6)
            url = 'https://www.colorhexa.com/' + color_code
            html = requests.get(url).text
            soup = bs(str(html), 'html')

            # Get similar colors
            similar = soup.find('div', {'class': 'similar'})
            similar = similar.find_all('li')
            similar_hex = [color.find('a').text for color in similar]

            # Get similar monochromatic colors
            monochromatic = soup.find('div', {'id': 'monochromatic'})
            monochromatic = monochromatic.find_all('li')
            monochromatic_hex = [color.find('a').text for color in monochromatic]

            alternative_colors = similar_hex + monochromatic_hex
            ALT_COLORS[color] = alternative_colors
            # print(alternative_colors)

        # Select an unused hex color
        for alt in alternative_colors:
            if alt not in TAKEN_COLORS:
                return alt

    except Exception as e:
        print(e)
        print(color)

# For each Minecraft block, generate a unique hex color
def generate_unique_colors():
    for block, color in PALETTELOOKUP.items():
        if color not in TAKEN_COLORS:
            color = get_similar_color(color)
        HEX_COLORS[block] = color
        TAKEN_COLORS.add(color)

# Save the color mappings to a file
def save_color_mappings():
    filepath = join('gdpc', 'vox_lookup.py')
    with open(filepath, 'w') as f:
        # Save the MINECRAFT_TO_HEX dictionary
        f.write('MINECRAFT_TO_HEX = {\n')
        for block, color in HEX_COLORS.items():
            f.write(f'    "{block}": "{color}",\n')
        f.write('}\n\n')

        # Save the HEX_TO_MINECRAFT dictionary
        HEX_TO_MINECRAFT = {v: k for k, v in HEX_COLORS.items()}
        f.write('HEX_TO_MINECRAFT = {\n')
        for block, color in HEX_TO_MINECRAFT.items():
            f.write(f'    "{block}": "{color}",\n')
        f.write('}')

# For each Minecraft block, generate a unique hex color and save the mappings to a file
# Will be used to convert Minecraft blocks to voxels and vice versa
def generate_vox_lookup():
    generate_unique_colors()
    save_color_mappings()

generate_vox_lookup()

