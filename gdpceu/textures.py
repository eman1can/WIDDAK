import numpy as np

# A list of blocks that are the same on all sides
SIMPLE_TEXTURES = [
    'minecraft:dirt',
    'minecraft:coarse_dirt',
    'minecraft:gravel',
    'minecraft:sand',
    'minecraft:red_sand',

    'minecraft:cobblestone',
    'minecraft:stone',
    'minecraft:smooth_stone',
    'minecraft:stone_bricks',
    'minecraft:mossy_stone_bricks',
    'minecraft:cracked_stone_bricks',
    'minecraft:chiseled_stone_bricks',
    'minecraft:infested_stone',
    'minecraft:infested_cobblestone',
    'minecraft:infested_stone_bricks',
    'minecraft:infested_mossy_stone_bricks',
    'minecraft:infested_cracked_stone_bricks',
    'minecraft:infested_chiseled_stone_bricks',

    'minecraft:granite',
    'minecraft:polished_granite',
    'minecraft:diorite',
    'minecraft:polished_diorite',
    'minecraft:andesite',
    'minecraft:polished_andesite',

    'minecraft:bedrock',

    'minecraft:oak_planks',
    'minecraft:spruce_planks',
    'minecraft:birch_planks',
    'minecraft:jungle_planks',
    'minecraft:acacia_planks',
    'minecraft:dark_oak_planks',

    'minecraft:oak_leaves',
    'minecraft:spruce_leaves',
    'minecraft:birch_leaves',
    'minecraft:jungle_leaves',
    'minecraft:acacia_leaves',
    'minecraft:dark_oak_leaves',

    'minecraft:brown_mushroom_block',
    'minecraft:red_mushroom_block',

    'minecraft:coal_ore',
    'minecraft:coal_block',
    'minecraft:iron_ore',
    'minecraft:iron_block',
    'minecraft:copper_ore',
    'minecraft:copper_block',
    'minecraft:gold_ore',
    'minecraft:gold_block',
    'minecraft:lapis_ore',
    'minecraft:lapis_block',
    'minecraft:diamond_ore',
    'minecraft:diamond_block',
    'minecraft:redstone_ore',
    'minecraft:redstone_block',
    'minecraft:emerald_ore',
    'minecraft:emerald_block',

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

    'minecraft:sponge',
    'minecraft:wet_sponge',
    'minecraft:glass',
    'minecraft:note_block',

    'minecraft:smooth_quartz',
    'minecraft:quartz_block',

    'minecraft:bricks',
    'minecraft:mossy_cobblestone',
    'minecraft:obsidian',
    'minecraft:purpur_block',
    'minecraft:spawner',

    'minecraft:ice',
    'minecraft:snow_block',
    'minecraft:clay',

    'minecraft:netherrack',
    'minecraft:soul_sand',
    'minecraft:glowstone',
    'minecraft:nether_bricks',
    'minecraft:red_nether_bricks',

    'minecraft:end_stone',
    'minecraft:end_stone_bricks',
    'minecraft:redstone_lamp',  # NBT: lit = true | false


]


# Slabs
# Pressure Plates
# Stairs
# Trapdoors
# Flowers / Plants
# Torches
# Textures that have a top, and four sides

# Textures that have a side and a top

# Textures that are unique

IDENTIFIER_TO_TEXTURES = {
    'minecraft:oak_trapdoor': {
        'size': [1, 0.2, 1],
        'textures': ['oak_trapdoor.png'],
        'texture_ids': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32),
        'facing': {
            'north': {
                'rotation': [0, 0, np.pi / 2],
                'translate': [-0.4, 0, 0]
            },
            'south': {
                'rotation': [0, 0, np.pi / 2],
                'translate': [0.4, 0, 0]
            },
            'east': {
                'rotation': [np.pi / 2, 0, 0],
                'translate': [0, 0, 0.4]
            },
            'west': {
                'rotation': [np.pi / 2, 0, 0],
                'translate': [0, 0, -0.4]
            }
        },
        'open': {

        }
    },
    'minecraft:grass_block': {
        'size': [1, 1, 1],
        'textures': ['grass_block_side.png', 'grass_block_top.png', 'grass_block_bottom.png'],
        'texture_ids': np.array([1, 1, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0], dtype=np.int32)
    },  # Top, ?, Bottom, ?, ?, ?
    'minecraft:poppy': {
        'size': [0.4, 0.6, 0.4],
        'translate': [0, -0.2, 0],
        'textures': ['poppy.png'],
        'texture_ids': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32)
    },
    'minecraft:dandelion': {
        'size': [0.4, 0.6, 0.4],
        'translate': [0, -0.2, 0],
        'textures': ['dandelion.png'],
        'texture_ids': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32)
    },
    'minecraft:oxeye_daisy': {
        'size': [0.4, 1, 0.4],
        'textures': ['oxeye_daisy.png'],
        'texture_ids': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32)
    },
    'minecraft:oak_fence': {
        'size': [0.4, 1, 1],
        'textures': ['oak_planks.png'],
        'texture_ids': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32),
        'facing': {
            'east': {
                'rotation': [0, np.pi / 2, 0]
            },
            'west': {
                'rotation': [0, np.pi / 2, 0]
            }
        }
    },
    'minecraft:oak_fence_gate': {
        'size': [0.4, 0.8, 1],
        'textures': ['oak_planks.png'],
        'texture_ids': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32),
        'facing': {
            'east': {
                'rotation': [0, np.pi / 2, 0]
            },
            'west': {
                'rotation': [0, np.pi / 2, 0]
            }
        }
    },
    'minecraft:tall_grass': {
        'size': [1, 2, 1],
        'textures': ['grass.png'],
        'texture_ids': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32),
    },
    'minecraft:hay_block': {
        'size': [1, 1, 1],
        'textures': ['hay_block_side.png', 'hay_block_top.png'],
        'texture_ids': np.array([1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], dtype=np.int32),
    },
    'minecraft:torch': {
        'size': [0.1, 0.8, 0.1],
        'translate': [0, -0.1, 0],
        'textures': ['torch.png'],
        'texture_ids': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32),
    },
    'minecraft:water': {
        'size': [1, 1, 1],
        'textures': ['water_still.png'],
        'texture_ids': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32)
    },
}