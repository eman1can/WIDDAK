import numpy as np

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
        'textures': ['grass_block_side.png', 'grass_block_top.png', 'grass_block_side.png'],
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
    'minecraft:grass': {
        'size': [1, 1, 1],
        'textures': ['grass.png'],
        'texture_ids': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32),
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
    'minecraft:cobblestone': {
        'size': [1, 1, 1],
        'textures': ['cobblestone.png'],
        'texture_ids': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32),
    },
    'minecraft:water': {
        'size': [1, 1, 1],
        'textures': ['water_still.png'],
        'texture_ids': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32),
    },
    'minecraft:torch': {
        'size': [0.1, 0.8, 0.1],
        'translate': [0, -0.1, 0],
        'textures': ['torch.png'],
        'texture_ids': np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.int32),
    }
}