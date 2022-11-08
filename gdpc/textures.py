from os import listdir
from os.path import exists

import numpy as np

# TODO: Finish me after completing OpenGL Renderer

SIMPLE_TEXTURES = [
    'minecraft:oak_planks',
    'minecraft:birch_planks',
    'minecraft:spruce_planks',
    'minecraft:jungle_planks',
    'minecraft:acacia_planks',
    'minecraft:dark_oak_planks',
    'minecraft:warped_planks',
    'minecraft:crimson_planks',
    'minecraft:bamboo_planks',
    'minecraft:mangrove_planks',

    'minecraft:white_wool',
    'minecraft:orange_wool',
    'minecraft:magenta_wool',
    'minecraft:light_blue_wool',
    'minecraft:yellow_wool',
    'minecraft:lime_wool',
    'minecraft:pink_wool',
    'minecraft:gray_wool',
    'minecraft:light_gray_wool',
    'minecraft:cyan_wool',
    'minecraft:purple_wool',
    'minecraft:blue_wool',
    'minecraft:brown_wool',
    'minecraft:green_wool',
    'minecraft:red_wool',
    'minecraft:black_wool',

    'minecraft:white_concrete',
    'minecraft:orange_concrete',
    'minecraft:magenta_concrete',
    'minecraft:light_blue_concrete',
    'minecraft:yellow_concrete',
    'minecraft:lime_concrete',
    'minecraft:pink_concrete',
    'minecraft:gray_concrete',
    'minecraft:light_gray_concrete',
    'minecraft:cyan_concrete',
    'minecraft:purple_concrete',
    'minecraft:blue_concrete',
    'minecraft:brown_concrete',
    'minecraft:green_concrete',
    'minecraft:red_concrete',
    'minecraft:black_concrete',
    'minecraft:white_concrete_powder',
    'minecraft:orange_concrete_powder',
    'minecraft:magenta_concrete_powder',
    'minecraft:light_blue_concrete_powder',
    'minecraft:yellow_concrete_powder',
    'minecraft:lime_concrete_powder',
    'minecraft:pink_concrete_powder',
    'minecraft:gray_concrete_powder',
    'minecraft:light_gray_concrete_powder',
    'minecraft:cyan_concrete_powder',
    'minecraft:purple_concrete_powder',
    'minecraft:blue_concrete_powder',
    'minecraft:brown_concrete_powder',
    'minecraft:green_concrete_powder',
    'minecraft:red_concrete_powder',
    'minecraft:black_concrete_powder',

    'minecraft:glass',
    'minecraft:tinted_glass',
    'minecraft:white_stained_glass',
    'minecraft:orange_stained_glass',
    'minecraft:magenta_stained_glass',
    'minecraft:light_blue_stained_glass',
    'minecraft:yellow_stained_glass',
    'minecraft:lime_stained_glass',
    'minecraft:pink_stained_glass',
    'minecraft:gray_stained_glass',
    'minecraft:light_gray_stained_glass',
    'minecraft:cyan_stained_glass',
    'minecraft:purple_stained_glass',
    'minecraft:blue_stained_glass',
    'minecraft:brown_stained_glass',
    'minecraft:green_stained_glass',
    'minecraft:red_stained_glass',
    'minecraft:black_stained_glass',

    'minecraft:coal_ore',
    'minecraft:iron_ore',
    'minecraft:copper_ore',
    'minecraft:gold_ore',
    'minecraft:lapis_ore',
    'minecraft:redstone_ore',
    'minecraft:diamond_ore',
    'minecraft:emerald_ore',

    'minecraft:deepslate_coal_ore',
    'minecraft:deepslate_iron_ore',
    'minecraft:deepslate_copper_ore',
    'minecraft:deepslate_gold_ore',
    'minecraft:deepslate_lapis_ore',
    'minecraft:deepslate_redstone_ore',
    'minecraft:deepslate_diamond_ore',
    'minecraft:deepslate_emerald_ore',

    'minecraft:coal_block',
    'minecraft:iron_block',
    'minecraft:copper_block',
    'minecraft:gold_block',
    'minecraft:lapis_block',
    'minecraft:redstone_block',
    'minecraft:diamond_block',
    'minecraft:emerald_block',

    'minecraft:raw_iron_block',
    'minecraft:raw_copper_block',
    'minecraft:raw_gold_block',

    'minecraft:nether_gold_ore',
    'minecraft:nether_quartz_ore',

]
# A list of blocks that are the same on all sides

MULTI_TEXTURES = {  # Front, Top, Left, Bottom, Right, Back
    'minecraft:oak_log':               [['oak_log.png', 'oak_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_oak_log':      [['stripped_oak_log.png', 'stripped_oak_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:birch_log':             [['birch_log.png', 'birch_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_birch_log':    [['stripped_birch_log.png', 'stripped_birch_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:spruce_log':            [['spruce_log.png', 'spruce_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_spruce_log':   [['stripped_spruce_log.png', 'stripped_spruce_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:jungle_log':            [['jungle_log.png', 'jungle_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_jungle_log':   [['stripped_jungle_log.png', 'stripped_jungle_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:acacia_log':            [['acacia_log.png', 'acacia_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_acacia_log':   [['stripped_acacia_log.png', 'stripped_acacia_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:dark_oak_log':          [['dark_oak_log.png', 'dark_oak_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_dark_oak_log': [['stripped_dark_oak_log.png', 'stripped_dark_oak_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:mangrove_log':          [['mangrove_log.png', 'mangrove_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_mangrove_log': [['stripped_mangrove_log.png', 'stripped_mangrove_log_top.png'], [0, 1, 0, 1, 0, 0]],

}
MULTI_TEXTURES_LIST = list(MULTI_TEXTURES.keys())
# 'minecraft:warped_stem': [['warped_stem.png', 'warped_stem_top.png'], [0, 1, 0, 1, 0, 0]], TODO: Add Animated Blocks
# 'minecraft:crimson_stem': [['crimson_stem.png', 'crimson_stem_top.png'], [0, 1, 0, 1, 0, 0]],

DOORS = ['minecraft:iron_door', 'minecraft:oak_door', 'minecraft:spruce_door', 'minecraft:birch_door', 'minecraft:jungle_door', 'minecraft:acacia_door', 'minecraft:dark_oak_door', 'minecraft:crimson_door', 'minecraft:warped_door']
FENCES = ['minecraft:oak_fence', 'minecraft:spruce_fence', 'minecraft:birch_fence', 'minecraft:jungle_fence', 'minecraft:acacia_fence', 'minecraft:dark_oak_fence', 'minecraft:nether_brick_fence', 'minecraft:crimson_fence', 'minecraft:warped_fence']
FENCE_GATES = ['minecraft:oak_fence_gate', 'minecraft:spruce_fence_gate', 'minecraft:birch_fence_gate', 'minecraft:jungle_fence_gate', 'minecraft:acacia_fence_gate', 'minecraft:dark_oak_fence_gate', 'minecraft:end_gateway',
               'minecraft:crimson_fence_gate', 'minecraft:warped_fence_gate']
WALLS = ['minecraft:cobblestone_wall', 'minecraft:mossy_cobblestone_wall', 'minecraft:brick_wall', 'minecraft:prismarine_wall', 'minecraft:red_sandstone_wall', 'minecraft:mossy_stone_brick_wall', 'minecraft:granite_wall',
         'minecraft:stone_brick_wall', 'minecraft:nether_brick_wall', 'minecraft:andesite_wall', 'minecraft:red_nether_brick_wall', 'minecraft:sandstone_wall', 'minecraft:end_stone_brick_wall', 'minecraft:diorite_wall', 'minecraft:blackstone_wall',
         'minecraft:polished_blackstone_wall', 'minecraft:polished_blackstone_brick_wall', 'minecraft:cobbled_deepslate_wall', 'minecraft:deepslate_brick_wall', 'minecraft:deepslate_tile_wall', 'minecraft:polished_deepslate_wall']

PLANTS = [
    'minecraft:oak_sapling',
    'minecraft:birch_sapling',
    'minecraft:spruce_sapling',
    'minecraft:jungle_sapling',
    'minecraft:acacia_sapling',
    'minecraft:dark_oak_sapling',

]

VARIABLE_HEIGHT = {
    0.5:  ['minecraft:oak_slab', 'minecraft:spruce_slab', 'minecraft:birch_slab', 'minecraft:jungle_slab', 'minecraft:acacia_slab', 'minecraft:dark_oak_slab', 'minecraft:stone_slab', 'minecraft:sandstone_slab', 'minecraft:petrified_oak_slab',
           'minecraft:cobblestone_slab', 'minecraft:brick_slab', 'minecraft:stone_brick_slab', 'minecraft:nether_brick_slab', 'minecraft:quartz_slab', 'minecraft:red_sandstone_slab', 'minecraft:purpur_slab', 'minecraft:prismarine_slab',
           'minecraft:prismarine_brick_slab', 'minecraft:dark_prismarine_slab', 'minecraft:smooth_stone_slab', 'minecraft:cut_sandstone_slab', 'minecraft:cut_red_sandstone_slab', 'minecraft:polished_granite_slab',
           'minecraft:smooth_red_sandstone_slab', 'minecraft:mossy_stone_brick_slab', 'minecraft:polished_diorite_slab', 'minecraft:mossy_cobblestone_slab', 'minecraft:end_stone_brick_slab', 'minecraft:smooth_sandstone_slab',
           'minecraft:smooth_quartz_slab', 'minecraft:granite_slab', 'minecraft:andesite_slab', 'minecraft:red_nether_brick_slab', 'minecraft:polished_andesite_slab', 'minecraft:diorite_slab', 'minecraft:crimson_slab', 'minecraft:warped_slab',
           'minecraft:blackstone_slab', 'minecraft:polished_blackstone_slab', 'minecraft:polished_blackstone_brick_slab', 'minecraft:cobbled_deepslate_slab', 'minecraft:cut_copper_slab', 'minecraft:deepslate_brick_slab',
           'minecraft:deepslate_tile_slab', 'minecraft:exposed_cut_copper_slab', 'minecraft:oxidized_cut_copper_slab', 'minecraft:polished_deepslate_slab', 'minecraft:waxed_cut_copper_slab', 'minecraft:waxed_exposed_cut_copper_slab',
           'minecraft:waxed_oxidized_cut_copper_slab', 'minecraft:waxed_weathered_cut_copper_slab', 'minecraft:weathered_cut_copper_slab'],
    0.15: ['minecraft:stone_pressure_plate', 'minecraft:oak_pressure_plate', 'minecraft:spruce_pressure_plate', 'minecraft:birch_pressure_plate', 'minecraft:jungle_pressure_plate', 'minecraft:acacia_pressure_plate',
           'minecraft:dark_oak_pressure_plate', 'minecraft:light_weighted_pressure_plate', 'minecraft:heavy_weighted_pressure_plate', 'minecraft:crimson_pressure_plate', 'minecraft:warped_pressure_plate',
           'minecraft:polished_blackstone_pressure_plate'],
    0.1:  ['minecraft:white_carpet', 'minecraft:orange_carpet', 'minecraft:magenta_carpet', 'minecraft:light_blue_carpet', 'minecraft:yellow_carpet', 'minecraft:lime_carpet', 'minecraft:pink_carpet', 'minecraft:gray_carpet',
           'minecraft:light_gray_carpet', 'minecraft:cyan_carpet', 'minecraft:purple_carpet', 'minecraft:blue_carpet', 'minecraft:brown_carpet', 'minecraft:green_carpet', 'minecraft:red_carpet', 'minecraft:black_carpet', 'minecraft:moss_carpet'],
    0.01: ['minecraft:powered_rail', 'minecraft:detector_rail', 'minecraft:rail', 'minecraft:activator_rail']
}

GLASS_PANES = [
    'minecraft:glass',
    'minecraft:white_stained_glass',
    'minecraft:orange_stained_glass',
    'minecraft:magenta_stained_glass',
    'minecraft:light_blue_stained_glass',
    'minecraft:yellow_stained_glass',
    'minecraft:lime_stained_glass',
    'minecraft:pink_stained_glass',
    'minecraft:gray_stained_glass',
    'minecraft:light_gray_stained_glass',
    'minecraft:cyan_stained_glass',
    'minecraft:purple_stained_glass',
    'minecraft:blue_stained_glass',
    'minecraft:brown_stained_glass',
    'minecraft:green_stained_glass',
    'minecraft:red_stained_glass',
    'minecraft:black_stained_glass',
]

SIGNS = ['minecraft:sign', 'minecraft:oak_sign', 'minecraft:spruce_sign', 'minecraft:birch_sign', 'minecraft:jungle_sign', 'minecraft:acacia_sign', 'minecraft:dark_oak_sign', 'minecraft:crimson_sign', 'minecraft:warped_sign']
WALL_SIGNS = ['minecraft:wall_sign', 'minecraft:oak_wall_sign', 'minecraft:spruce_wall_sign', 'minecraft:birch_wall_sign', 'minecraft:acacia_wall_sign', 'minecraft:jungle_wall_sign', 'minecraft:dark_oak_wall_sign', 'minecraft:crimson_wall_sign',
              'minecraft:warped_wall_sign']

TRAPDOORS = [
    'minecraft:oak_trapdoor',
    'minecraft:spruce_trapdoor',
    'minecraft:birch_trapdoor',
    'minecraft:jungle_trapdoor',
    'minecraft:acacia_trapdoor',
    'minecraft:dark_oak_trapdoor',
    'minecraft:iron_trapdoor',
    'minecraft:crimson_trapdoor',
    'minecraft:warped_trapdoor'
]

STAIRS = ['minecraft:purpur_stairs', 'minecraft:oak_stairs', 'minecraft:cobblestone_stairs', 'minecraft:brick_stairs', 'minecraft:stone_brick_stairs', 'minecraft:nether_brick_stairs', 'minecraft:sandstone_stairs', 'minecraft:spruce_stairs',
          'minecraft:birch_stairs', 'minecraft:jungle_stairs', 'minecraft:quartz_stairs', 'minecraft:acacia_stairs', 'minecraft:dark_oak_stairs', 'minecraft:prismarine_stairs', 'minecraft:prismarine_brick_stairs', 'minecraft:dark_prismarine_stairs',
          'minecraft:red_sandstone_stairs', 'minecraft:polished_granite_stairs', 'minecraft:smooth_red_sandstone_stairs', 'minecraft:mossy_stone_brick_stairs', 'minecraft:polished_diorite_stairs', 'minecraft:mossy_cobblestone_stairs',
          'minecraft:end_stone_brick_stairs', 'minecraft:stone_stairs', 'minecraft:smooth_sandstone_stairs', 'minecraft:smooth_quartz_stairs', 'minecraft:granite_stairs', 'minecraft:andesite_stairs', 'minecraft:red_nether_brick_stairs',
          'minecraft:polished_andesite_stairs', 'minecraft:diorite_stairs', 'minecraft:crimson_stairs', 'minecraft:warped_stairs', 'minecraft:blackstone_stairs', 'minecraft:polished_blackstone_stairs', 'minecraft:polished_blackstone_brick_stairs',
          'minecraft:cobbled_deepslate_stairs', 'minecraft:cut_copper_stairs', 'minecraft:deepslate_brick_stairs', 'minecraft:deepslate_tile_stairs', 'minecraft:exposed_cut_copper_stairs', 'minecraft:oxidized_cut_copper_stairs',
          'minecraft:polished_deepslate_stairs', 'minecraft:waxed_cut_copper_stairs', 'minecraft:waxed_exposed_cut_copper_stairs', 'minecraft:waxed_oxidized_cut_copper_stairs', 'minecraft:waxed_weathered_cut_copper_stairs',
          'minecraft:weathered_cut_copper_stairs']

CATEGORIES = [
    'SIMPLE',
    'MULTI_TEXTURE',
]

if __name__ == "__main__":
    asset_files = list(listdir('local/block_assets'))

    with open('sections/Voxel Renderer/textures.h', 'w') as file:
        file.write('//\n')
        file.write('// Created by Zoe on 10/31/2022\n')
        file.write('// This file is AUTO GENERATED\n')
        file.write('// See gdcp/textures.py for generation\n')
        file.write('\n')
        file.write('#ifndef LIBVOXEL_TEXTURES_H\n')
        file.write('#define LIBVOXEL_TEXTURES_H\n')
        file.write('\n#include <cstdint>\n\n')
        file.write('typedef enum {\n')
        for category in CATEGORIES:
            file.write(f'     {category},\n')
        file.write('} Category;\n')
        file.write('const char* TEXTURE_ASSETS[] = {\n')
        for ix, file_name in enumerate(asset_files):
            file.write(f' /* {ix} */ "local/block_assets/{file_name}",\n')
        file.write('};\n')
        file.write('\n')
        file.write('uint16_t SIMPLE_TEXTURE_IMAGES[] = {\n')
        for ix, blockID in enumerate(SIMPLE_TEXTURES):
            name = blockID[len('minecraft:'):] + '.png'
            file.write(f' /* {ix} */ '.ljust(11) + f'{asset_files.index(name)},'.ljust(4) + f' // {blockID}\n')
        file.write('};\n')
        file.write('\n')
        file.write('typedef struct {\n')
        file.write('uint16_t textures[6];\n')
        file.write('uint8_t texture_ids[6];\n')
        file.write('} MultiTexture;\n')
        file.write('\n')
        file.write('MultiTexture MULTI_TEXTURES[] = {\n')
        for ix, (blockID, data) in enumerate(MULTI_TEXTURES.items()):
            textures = [str(asset_files.index(name)) for name in data[0]]
            texture_ids = [str(x) for x in data[1]]
            file.write(f' /* {ix} */ '.ljust(11) + ('{{' + ', '.join(textures) + '},').ljust(12) + ' {' + ', '.join(texture_ids) + '}}, // ' + blockID + '\n')
        file.write('};\n')
        file.write('\n')

        file.write('#endif //LIBVOXEL_TEXTURES_H')
