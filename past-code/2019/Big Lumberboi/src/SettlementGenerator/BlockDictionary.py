class Block:

    def __init__(self, type, direction=None, verticalAllignment=None):
        self.type = type
        self.direction = direction
        self.verticalAllignment = verticalAllignment


def getBlockIdentifier(block):
    if not blockTypes.get(block.type):
        return None
    identifier = None
    if not block.direction and not block.verticalAllignment:
        identifier = blockTypes[block.type]['default']
    elif not block.direction and block.verticalAllignment and blockTypes[block.type].get('slabs'):
        identifier = blockTypes[block.type]['slabs'][block.verticalAllignment]
    elif blockTypes[block.type].get('directions') and blockTypes[block.type]['directions'].get(block.direction):
        identifier = blockTypes[block.type]['directions'][block.direction][block.verticalAllignment]
    if not identifier:
        identifier = blockTypes[block.type]['default']
    return identifier


def getBlock(id, data):
    identifier = (id, data)
    for _, blockType in blockTypes.iteritems():
        # checking default
        if blockType['default'] == identifier:
            return Block(blockType['type'], None, None)
        # checking slabs if the blocktype includes slabs
        if blockType.get('slabs'):
            if blockType['slabs']['top'] == identifier:
                return Block(blockType['type'], None, 'top')
            if blockType['slabs']['bottom'] == identifier:
                return Block(blockType['type'], None, 'bottom')
        # checking directions if the blocktype includes directions
        if blockType.get('directions'):
            # north
            if blockType['directions']['north']['top'] == identifier:
                return Block(blockType['type'], 'north', 'top')
            if blockType['directions']['north']['bottom'] == identifier:
                return Block(blockType['type'], 'north', 'bottom')
            # east
            if blockType['directions']['east']['top'] == identifier:
                return Block(blockType['type'], 'east', 'top')
            if blockType['directions']['east']['bottom'] == identifier:
                return Block(blockType['type'], 'east', 'bottom')
            # south
            if blockType['directions']['south']['top'] == identifier:
                return Block(blockType['type'], 'south', 'top')
            if blockType['directions']['south']['bottom'] == identifier:
                return Block(blockType['type'], 'south', 'bottom')
            # west
            if blockType['directions']['west']['top'] == identifier:
                return Block(blockType['type'], 'west', 'top')
            if blockType['directions']['west']['bottom'] == identifier:
                return Block(blockType['type'], 'west', 'bottom')
    return None


blockTypes = {
    'stone': {
        'type': 'stone',
        'default': (1, 0),
        'slabs': {
            'top': (44, 8),
            'bottom': (44, 0)
        }
    },
    'cobblestone': {
        'type': 'cobblestone',
        'default': (4, 0),
        'directions': {
            'north': {
                'top': (67, 7),
                'bottom': (67, 3)
            },
            'east': {
                'top': (67, 4),
                'bottom': (67, 0)
            },
            'south': {
                'top': (67, 6),
                'bottom': (67, 2)
            },
            'west': {
                'top': (67, 5),
                'bottom': (67, 1)
            }
        },
        'slabs': {
            'top': (44, 11),
            'bottom': (44, 3)
        }
    },
    'stone_brick': {
        'type': 'stone_brick',
        'default': (98, 0),
        'directions': {
            'north': {
                'top': (109, 7),
                'bottom': (109, 3)
            },
            'east': {
                'top': (109, 4),
                'bottom': (109, 0)
            },
            'south': {
                'top': (109, 6),
                'bottom': (109, 2)
            },
            'west': {
                'top': (109, 5),
                'bottom': (109, 1)
            }
        },
        'slabs': {
            'top': (44, 13),
            'bottom': (44, 5)
        }
    },
    'brick': {
        'type': 'brick',
        'default': (45, 0),
        'directions': {
            'north': {
                'top': (108, 7),
                'bottom': (108, 3)
            },
            'east': {
                'top': (108, 4),
                'bottom': (108, 0)
            },
            'south': {
                'top': (108, 6),
                'bottom': (108, 2)
            },
            'west': {
                'top': (108, 5),
                'bottom': (108, 1)
            }
        },
        'slabs': {
            'top': (44, 12),
            'bottom': (44, 4)
        }
    },
    'oak_wood': {
        'type': 'oak_wood',
        'default': (17, 0),
        'directions': {
            'north': {
                'top': (17, 8),
                'bottom': (17, 8)
            },
            'east': {
                'top': (17, 4),
                'bottom': (17, 4)
            },
            'south': {
                'top': (17, 8),
                'bottom': (17, 8)
            },
            'west': {
                'top': (17, 4),
                'bottom': (17, 4)
            }
        }
    },
    'spruce_wood': {
        'type': 'spruce_wood',
        'default': (17, 1),
        'directions': {
            'north': {
                'top': (17, 9),
                'bottom': (17, 9)
            },
            'east': {
                'top': (17, 5),
                'bottom': (17, 5)
            },
            'south': {
                'top': (17, 9),
                'bottom': (17, 9)
            },
            'west': {
                'top': (17, 5),
                'bottom': (17, 5)
            }
        }
    },
    'birch_wood': {
        'type': 'birch_wood',
        'default': (17, 2),
        'directions': {
                'north': {
                    'top': (17, 10),
                    'bottom': (17, 10)
                },
            'east': {
                    'top': (17, 6),
                    'bottom': (17, 6)
                },
            'south': {
                    'top': (17, 10),
                    'bottom': (17, 10)
                },
            'west': {
                    'top': (17, 6),
                    'bottom': (17, 6)
                }
        }
    },
    'jungle_wood': {
        'type': 'jungle_wood',
        'default': (17, 3),
        'directions': {
                'north': {
                    'top': (17, 11),
                    'bottom': (17, 11)
                },
            'east': {
                    'top': (17, 7),
                    'bottom': (17, 7)
                },
            'south': {
                    'top': (17, 11),
                    'bottom': (17, 11)
                },
            'west': {
                    'top': (17, 7),
                    'bottom': (17, 7)
                }
        }
    },
    'acacia_wood': {
        'type': 'acacia_wood',
        'default': (162, 0),
        'directions': {
            'north': {
                'top': (162, 8),
                'bottom': (162, 8)
            },
            'east': {
                'top': (162, 4),
                'bottom': (162, 4)
            },
            'south': {
                'top': (162, 8),
                'bottom': (162, 8)
            },
            'west': {
                'top': (162, 4),
                'bottom': (162, 4)
            }
        }
    },
    'dark_oak_wood': {
        'type': 'dark_oak_wood',
        'default': (162, 1),
        'directions': {
            'north': {
                'top': (162, 9),
                'bottom': (162, 9)
            },
            'east': {
                'top': (162, 5),
                'bottom': (162, 5)
            },
            'south': {
                'top': (162, 9),
                'bottom': (162, 9)
            },
            'west': {
                'top': (162, 5),
                'bottom': (162, 5)
            }
        }
    },
    'oak_wood_planks': {
        'type': 'oak_wood_planks',
        'default': (5, 0),
        'directions': {
            'north': {
                'top': (53, 7),
                'bottom': (53, 3)
            },
            'east': {
                'top': (53, 4),
                'bottom': (53, 0)
            },
            'south': {
                'top': (53, 6),
                'bottom': (53, 2)
            },
            'west': {
                'top': (53, 5),
                'bottom': (53, 1)
            }
        },
        'slabs': {
            'top': (126, 8),
            'bottom': (126, 0)
        }
    },
    'spruce_wood_planks': {
        'type': 'spruce_wood_planks',
        'default': (5, 1),
        'directions': {
            'north': {
                'top': (134, 7),
                'bottom': (134, 3)
            },
            'east': {
                'top': (134, 4),
                'bottom': (134, 0)
            },
            'south': {
                'top': (134, 6),
                'bottom': (134, 2)
            },
            'west': {
                'top': (134, 5),
                'bottom': (134, 1)
            }
        },
        'slabs': {
            'top': (126, 9),
            'bottom': (126, 1)
        }
    },
    'birch_wood_planks': {
        'type': 'birch_wood_planks',
        'default': (5, 2),
        'directions': {
            'north': {
                'top': (135, 7),
                'bottom': (135, 3)
            },
            'east': {
                'top': (135, 4),
                'bottom': (135, 0)
            },
            'south': {
                'top': (135, 6),
                'bottom': (135, 2)
            },
            'west': {
                'top': (135, 5),
                'bottom': (135, 1)
            }
        },
        'slabs': {
            'top': (126, 10),
            'bottom': (126, 2)
        }
    },
    'jungle_wood_planks': {
        'type': 'jungle_wood_planks',
        'default': (5, 3),
        'directions': {
            'north': {
                'top': (136, 7),
                'bottom': (136, 3)
            },
            'east': {
                'top': (136, 4),
                'bottom': (136, 0)
            },
            'south': {
                'top': (136, 6),
                'bottom': (136, 2)
            },
            'west': {
                'top': (136, 5),
                'bottom': (136, 1)
            }
        },
        'slabs': {
            'top': (126, 11),
            'bottom': (126, 3)
        }
    },
    'acacia_wood_planks': {
        'type': 'acacia_wood_planks',
        'default': (5, 4),
        'directions': {
            'north': {
                'top': (163, 7),
                'bottom': (163, 3)
            },
            'east': {
                'top': (163, 4),
                'bottom': (163, 0)
            },
            'south': {
                'top': (163, 6),
                'bottom': (163, 2)
            },
            'west': {
                'top': (163, 5),
                'bottom': (163, 1)
            }
        },
        'slabs': {
            'top': (126, 12),
            'bottom': (126, 4)
        }
    },
    'dark_oak_wood_planks': {
        'type': 'dark_oak_wood_planks',
        'default': (5, 5),
        'directions': {
            'north': {
                'top': (164, 7),
                'bottom': (164, 3)
            },
            'east': {
                'top': (164, 4),
                'bottom': (164, 0)
            },
            'south': {
                'top': (164, 6),
                'bottom': (164, 2)
            },
            'west': {
                'top': (164, 5),
                'bottom': (164, 1)
            }
        },
        'slabs': {
            'top': (126, 13),
            'bottom': (126, 5)
        }
    },
    'oak_door': {
        'type': 'oak_door',
        'default': (64, 3),
        'directions': {
            'north': {
                'top': (64, 3),
                'bottom': (64, 3)
            },
            'east': {
                'top': (64, 0),
                'bottom': (64, 0)
            },
            'south': {
                'top': (64, 1),
                'bottom': (64, 1)
            },
            'west': {
                'top': (64, 2),
                'bottom': (64, 2)
            }
        }
    },
    'wooden_trapdoor': {
        'type': 'wooden_trapdoor',
        'default': (96, 0),
        'directions': {
            'north': {
                'top': (96, 8),
                'bottom': (96, 0)
            },
            'east': {
                'top': (96, 11),
                'bottom': (96, 3)
            },
            'south': {
                'top': (96, 9),
                'bottom': (96, 1)
            },
            'west': {
                'top': (96, 10),
                'bottom': (96, 2)
            }
        },
        'slabs': {
            'top': (96, 8),
            'bottom': (96, 0)
        }
    },
    'ladder': {
        'type': 'ladder',
        'default': (65, 2),
        'directions': {
            'north': {
                'top': (65, 2),
                'bottom': (65, 2)
            },
            'east': {
                'top': (65, 5),
                'bottom': (65, 5)
            },
            'south': {
                'top': (65, 3),
                'bottom': (65, 3)
            },
            'west': {
                'top': (65, 4),
                'bottom': (65, 4)
            }
        }
    },
    'torch': {
        'type': 'torch',
        'default': (50, 5),
        'directions': {
            'north': {
                'top': (50, 4),
                'bottom': (50, 4)
            },
            'east': {
                'top': (50, 1),
                'bottom': (50, 1)
            },
            'south': {
                'top': (50, 3),
                'bottom': (50, 3)
            },
            'west': {
                'top': (50, 2),
                'bottom': (50, 2)
            }
        }
    },
    'sandstone': {
        'type': 'sandstone',
        'default': (24, 0),
        'directions': {
            'north': {
                'top': (128, 7),
                'bottom': (128, 3)
            },
            'east': {
                'top': (128, 4),
                'bottom': (128, 0)
            },
            'south': {
                'top': (128, 6),
                'bottom': (128, 2)
            },
            'west': {
                'top': (128, 5),
                'bottom': (128, 1)
            }
        },
        'slabs': {
            'top': (44, 9),
            'bottom': (44, 1)
        }
    },
    'smooth_sandstone': {
        'type': 'smooth_sandstone',
        'default': (24, 2)
    },
    'chiseled_sandstone': {
        'type': 'chiseled_sandstone',
        'default': (24, 1)
    },
    'red_sandstone': {
        'type': 'red_sandstone',
        'default': (179, 0),
        'directions': {
            'north': {
                'top': (180, 7),
                'bottom': (180, 3)
            },
            'east': {
                'top': (180, 4),
                'bottom': (180, 0)
            },
            'south': {
                'top': (180, 6),
                'bottom': (180, 2)
            },
            'west': {
                'top': (180, 5),
                'bottom': (180, 1)
            }
        },
        'slabs': {
            'top': (44, 8),
            'bottom': (44, 0)
        }
    },
    'red_smooth_sandstone': {
        'type': 'smooth_sandstone',
        'default': (179, 2)
    },
    'red_chiseled_sandstone': {
        'type': 'chiseled_sandstone',
        'default': (179, 1)
    },
    'oak_wood_fence': {
        'type': 'oak_wood_fence',
        'default': (85, 0)
    },
    'spruce_wood_fence': {
        'type': 'spruce_wood_fence',
        'default': (188, 0)
    },
    'birch_wood_fence': {
        'type': 'birch_wood_fence',
        'default': (189, 0)
    },
    'jungle_wood_fence': {
        'type': 'jungle_wood_fence',
        'default': (190, 0)
    },
    'dark_oak_wood_fence': {
        'type': 'dark_oak_wood_fence',
        'default': (191, 0)
    },
    'acacia_wood_fence': {
        'type': 'acacia_wood_fence',
        'default': (192, 0)
    },
    'glass': {
        'type': 'glass',
        'default': (20, 0)
    },
    'glass_pane': {
        'type': 'glass_pane',
        'default': (102, 0)
    },
    'oak_wood_door': {
        'type': 'oak_wood_door',
        'default': (64, 0),
        'directions': {
            'north': {
                'top': (64, 9),
                'bottom': (64, 3)
            },
            'east': {
                'top': (64, 9),
                'bottom': (64, 0)
            },
            'south': {
                'top': (64, 9),
                'bottom': (64, 1)
            },
            'west': {
                'top': (64, 9),
                'bottom': (64, 2)
            }
        }
    },
    'spruce_wood_door': {
        'type': 'spruce_wood_door',
        'default': (193, 0),
        'directions': {
            'north': {
                'top': (193, 9),
                'bottom': (193, 3)
            },
            'east': {
                'top': (193, 9),
                'bottom': (193, 0)
            },
            'south': {
                'top': (193, 9),
                'bottom': (193, 1)
            },
            'west': {
                'top': (193, 9),
                'bottom': (193, 2)
            }
        }
    },
    'birch_wood_door': {
        'type': 'birch_wood_door',
        'default': (194, 0),
        'directions': {
            'north': {
                'top': (194, 9),
                'bottom': (194, 3)
            },
            'east': {
                'top': (194, 9),
                'bottom': (194, 0)
            },
            'south': {
                'top': (194, 9),
                'bottom': (194, 1)
            },
            'west': {
                'top': (194, 9),
                'bottom': (194, 2)
            }
        }
    },
    'jungle_wood_door': {
        'type': 'jungle_wood_door',
        'default': (195, 0),
        'directions': {
            'north': {
                'top': (195, 9),
                'bottom': (195, 3)
            },
            'east': {
                'top': (195, 9),
                'bottom': (195, 0)
            },
            'south': {
                'top': (195, 9),
                'bottom': (195, 1)
            },
            'west': {
                'top': (195, 9),
                'bottom': (195, 2)
            }
        }
    },
    'acacia_wood_door': {
        'type': 'acacia_wood_door',
        'default': (196, 0),
        'directions': {
            'north': {
                'top': (196, 9),
                'bottom': (196, 3)
            },
            'east': {
                'top': (196, 9),
                'bottom': (196, 0)
            },
            'south': {
                'top': (196, 9),
                'bottom': (196, 1)
            },
            'west': {
                'top': (196, 9),
                'bottom': (196, 2)
            }
        }
    },
    'dark_oak_wood_door': {
        'type': 'dark_oak_wood_door',
        'default': (197, 0),
        'directions': {
            'north': {
                'top': (197, 9),
                'bottom': (197, 3)
            },
            'east': {
                'top': (197, 9),
                'bottom': (197, 0)
            },
            'south': {
                'top': (197, 9),
                'bottom': (197, 1)
            },
            'west': {
                'top': (197, 9),
                'bottom': (197, 2)
            }
        }
    }
}
