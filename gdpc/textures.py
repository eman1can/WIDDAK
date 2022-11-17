from os import listdir
from os.path import exists

import numpy as np

# TODO: Finish me after completing OpenGL Renderer

all_block_ids = ['Acacia Button', 'Acacia Door', 'Acacia Fence', 'Acacia Fence Gate', 'Acacia Hanging Sign', 'Acacia Leaves', 'Acacia Log', 'Acacia Planks', 'Acacia Pressure Plate', 'Acacia Sapling', 'Acacia Sign', 'Acacia Slab', 'Acacia Stairs', 'Acacia Trapdoor', 'Acacia Wood', 'Activator Rail', 'Allium', 'Amethyst Cluster', 'Ancient Debris', 'Andesite', 'Andesite Slab', 'Andesite Stairs', 'Andesite Wall', 'Anvil', 'Azalea', 'Azalea Leaves', 'Azure Bluet', 'Bamboo', 'Bamboo Button', 'Bamboo Door', 'Bamboo Fence', 'Bamboo Fence Gate', 'Bamboo Hanging Sign', 'Bamboo Mosaic', 'Bamboo Mosaic Slab', 'Bamboo Mosaic Stairs', 'Bamboo Planks', 'Bamboo Pressure Plate', 'Bamboo Shoot', 'Bamboo Sign', 'Bamboo Slab', 'Bamboo Stairs', 'Bamboo Trapdoor', 'Barrel', 'Barrier', 'Basalt', 'Beacon', 'Bedrock', 'Bee Nest', 'Beehive', 'Beetroots', 'Bell', 'Big Dripleaf', 'Birch Button', 'Birch Door', 'Birch Fence', 'Birch Fence Gate', 'Birch Hanging Sign', 'Birch Leaves', 'Birch Log', 'Birch Planks', 'Birch Pressure Plate', 'Birch Sapling', 'Birch Sign', 'Birch Slab', 'Birch Stairs', 'Birch Trapdoor', 'Birch Wood', 'Black Banner', 'Black Bed', 'Black Candle', 'Black Carpet', 'Black Concrete', 'Black Concrete Powder', 'Black Glazed Terracotta', 'Black Shulker Box', 'Black Stained Glass', 'Black Stained Glass Pane', 'Black Terracotta', 'Black Wool', 'Blackstone', 'Blackstone Slab', 'Blackstone Stairs', 'Blackstone Wall', 'Blast Furnace', 'Block of Amethyst', 'Block of Bamboo', 'Block of Coal', 'Block of Copper', 'Block of Diamond', 'Block of Emerald', 'Block of Gold', 'Block of Iron', 'Block of Lapis Lazuli', 'Block of Netherite', 'Block of Quartz', 'Block of Raw Copper', 'Block of Raw Gold', 'Block of Raw Iron', 'Block of Redstone', 'Block of Stripped Bamboo', 'Blue Banner', 'Blue Bed', 'Blue Candle', 'Blue Carpet', 'Blue Concrete', 'Blue Concrete Powder', 'Blue Glazed Terracotta', 'Blue Ice', 'Blue Orchid', 'Blue Shulker Box', 'Blue Stained Glass', 'Blue Stained Glass Pane', 'Blue Terracotta', 'Blue Wool', 'Bone Block', 'Bookshelf', 'Brain Coral', 'Brain Coral Block', 'Brain Coral Fan', 'Brewing Stand', 'Brick Slab', 'Brick Stairs', 'Brick Wall', 'Bricks', 'Brown Banner', 'Brown Bed', 'Brown Candle', 'Brown Carpet', 'Brown Concrete', 'Brown Concrete Powder', 'Brown Glazed Terracotta', 'Brown Mushroom', 'Brown Mushroom Block', 'Brown Shulker Box', 'Brown Stained Glass', 'Brown Stained Glass Pane', 'Brown Terracotta', 'Brown Wool', 'Bubble Coral', 'Bubble Coral Block', 'Bubble Coral Fan', 'Budding Amethyst', 'Cactus', 'Cake', 'Calcite', 'Campfire', 'Candle', 'Carrots', 'Cartography Table', 'Carved Pumpkin', 'Cauldron', 'Cave Vines', 'Chain', 'Chain Command Block', 'Chest', 'Chipped Anvil', 'Chiseled Bookshelf', 'Chiseled Deepslate', 'Chiseled Nether Bricks', 'Chiseled Polished Blackstone', 'Chiseled Quartz Block', 'Chiseled Red Sandstone', 'Chiseled Sandstone', 'Chiseled Stone Bricks', 'Chorus Flower', 'Chorus Plant', 'Clay', 'Coal Ore', 'Coarse Dirt', 'Cobbled Deepslate', 'Cobbled Deepslate Slab', 'Cobbled Deepslate Stairs', 'Cobbled Deepslate Wall', 'Cobblestone', 'Cobblestone Slab', 'Cobblestone Stairs', 'Cobblestone Wall', 'Cobweb', 'Cocoa', 'Command Block', 'Composter', 'Conduit', 'Copper Ore', 'Cornflower', 'Cracked Deepslate Bricks', 'Cracked Deepslate Tiles', 'Cracked Nether Bricks', 'Cracked Polished Blackstone Bricks', 'Cracked Stone Bricks', 'Crafting Table', 'Creeper Head', 'Crimson Button', 'Crimson Door', 'Crimson Fence', 'Crimson Fence Gate', 'Crimson Fungus', 'Crimson Hanging Sign', 'Crimson Hyphae', 'Crimson Nylium', 'Crimson Planks', 'Crimson Pressure Plate', 'Crimson Roots', 'Crimson Sign', 'Crimson Slab', 'Crimson Stairs', 'Crimson Stem', 'Crimson Trapdoor', 'Crying Obsidian', 'Cut Copper', 'Cut Copper Slab', 'Cut Copper Stairs', 'Cut Red Sandstone', 'Cut Red Sandstone Slab', 'Cut Sandstone', 'Cut Sandstone Slab', 'Cyan Banner', 'Cyan Bed', 'Cyan Candle', 'Cyan Carpet', 'Cyan Concrete', 'Cyan Concrete Powder', 'Cyan Glazed Terracotta', 'Cyan Shulker Box', 'Cyan Stained Glass', 'Cyan Stained Glass Pane', 'Cyan Terracotta', 'Cyan Wool', 'Damaged Anvil', 'Dandelion', 'Dark Oak Button', 'Dark Oak Door', 'Dark Oak Fence', 'Dark Oak Fence Gate', 'Dark Oak Hanging Sign', 'Dark Oak Leaves', 'Dark Oak Log', 'Dark Oak Planks', 'Dark Oak Pressure Plate', 'Dark Oak Sapling', 'Dark Oak Sign', 'Dark Oak Slab', 'Dark Oak Stairs', 'Dark Oak Trapdoor', 'Dark Oak Wood', 'Dark Prismarine', 'Dark Prismarine Slab', 'Dark Prismarine Stairs', 'Daylight Detector', 'Dead Brain Coral', 'Dead Brain Coral Block', 'Dead Brain Coral Fan', 'Dead Bubble Coral', 'Dead Bubble Coral Block', 'Dead Bubble Coral Fan', 'Dead Bush', 'Dead Fire Coral', 'Dead Fire Coral Block', 'Dead Fire Coral Fan', 'Dead Horn Coral', 'Dead Horn Coral Block', 'Dead Horn Coral Fan', 'Dead Tube Coral', 'Dead Tube Coral Block', 'Dead Tube Coral Fan', 'Deepslate', 'Deepslate Bricks', 'Deepslate Brick Slab', 'Deepslate Brick Stairs', 'Deepslate Brick Wall', 'Deepslate Coal Ore', 'Deepslate Copper Ore', 'Deepslate Diamond Ore', 'Deepslate Emerald Ore', 'Deepslate Gold Ore', 'Deepslate Iron Ore', 'Deepslate Lapis Lazuli Ore', 'Deepslate Redstone Ore', 'Deepslate Tiles', 'Deepslate Tile Slab', 'Deepslate Tile Stairs', 'Deepslate Tile Wall', 'Detector Rail', 'Diamond Ore', 'Diorite', 'Diorite Slab', 'Diorite Stairs', 'Diorite Wall', 'Dirt', 'Dirt Path', 'Dispenser', 'Dragon Egg', 'Dragon Head', 'Dried Kelp Block', 'Dripstone Block', 'Dropper', 'Emerald Ore', 'Enchanting Table', 'End Portal Frame', 'End Rod', 'End Stone', 'End Stone Brick Slab', 'End Stone Brick Stairs', 'End Stone Brick Wall', 'End Stone Bricks', 'Ender Chest', 'Exposed Copper', 'Exposed Cut Copper', 'Exposed Cut Copper Slab', 'Exposed Cut Copper Stairs', 'Farmland', 'Fern', 'Fire', 'Fire Coral', 'Fire Coral Block', 'Fire Coral Fan', 'Fletching Table', 'Flower Pot', 'Flowering Azalea', 'Flowering Azalea Leaves', 'Frogspawn', 'Furnace', 'Gilded Blackstone', 'Glass', 'Glass Pane', 'Glow Item Frame', 'Bedrock Edition', 'Glow Lichen', 'Glowstone', 'Gold Ore', 'Granite', 'Granite Slab', 'Granite Stairs', 'Granite Wall', 'Grass', 'Grass Block', 'Gravel', 'Gray Banner', 'Gray Bed', 'Gray Candle', 'Gray Carpet', 'Gray Concrete', 'Gray Concrete Powder', 'Gray Glazed Terracotta', 'Gray Shulker Box', 'Gray Stained Glass', 'Gray Stained Glass Pane', 'Gray Terracotta', 'Gray Wool', 'Green Banner', 'Green Bed', 'Green Candle', 'Green Carpet', 'Green Concrete', 'Green Concrete Powder', 'Green Glazed Terracotta', 'Green Shulker Box', 'Green Stained Glass', 'Green Stained Glass Pane', 'Green Terracotta', 'Green Wool', 'Grindstone', 'Hanging Roots', 'Hay Bale', 'Heavy Weighted Pressure Plate', 'Honey Block', 'Honeycomb Block', 'Hopper', 'Horn Coral', 'Horn Coral Block', 'Horn Coral Fan', 'Ice', 'Infested Chiseled Stone Bricks', 'Infested Cobblestone', 'Infested Cracked Stone Bricks', 'Infested Deepslate', 'Infested Mossy Stone Bricks', 'Infested Stone', 'Infested Stone Bricks', 'Iron Bars', 'Iron Door', 'Iron Ore', 'Iron Trapdoor', 'Item Frame', 'Bedrock Edition', "Jack o'Lantern", 'Jigsaw Block', 'Jukebox', 'Jungle Button', 'Jungle Door', 'Jungle Fence', 'Jungle Fence Gate', 'Jungle Hanging Sign', 'Jungle Leaves', 'Jungle Log', 'Jungle Planks', 'Jungle Pressure Plate', 'Jungle Sapling', 'Jungle Sign', 'Jungle Slab', 'Jungle Stairs', 'Jungle Trapdoor', 'Jungle Wood', 'Kelp', 'Ladder', 'Lantern', 'Lapis Lazuli Ore', 'Large Amethyst Bud', 'Large Fern', 'Lava', 'Lectern', 'Lever', 'Light Block', 'Light Blue Banner', 'Light Blue Bed', 'Light Blue Candle', 'Light Blue Carpet', 'Light Blue Concrete', 'Light Blue Concrete Powder', 'Light Blue Glazed Terracotta', 'Light Blue Shulker Box', 'Light Blue Stained Glass', 'Light Blue Stained Glass Pane', 'Light Blue Terracotta', 'Light Blue Wool', 'Light Gray Banner', 'Light Gray Bed', 'Light Gray Candle', 'Light Gray Carpet', 'Light Gray Concrete', 'Light Gray Concrete Powder', 'Light Gray Glazed Terracotta', 'Light Gray Shulker Box', 'Light Gray Stained Glass', 'Light Gray Stained Glass Pane', 'Light Gray Terracotta', 'Light Gray Wool', 'Light Weighted Pressure Plate', 'Lightning Rod', 'Lilac', 'Lily of the Valley', 'Lily Pad', 'Lime Banner', 'Lime Bed', 'Lime Candle', 'Lime Carpet', 'Lime Concrete', 'Lime Concrete Powder', 'Lime Glazed Terracotta', 'Lime Shulker Box', 'Lime Stained Glass', 'Lime Stained Glass Pane', 'Lime Terracotta', 'Lime Wool', 'Lodestone', 'Loom', 'Magenta Banner', 'Magenta Bed', 'Magenta Candle', 'Magenta Carpet', 'Magenta Concrete', 'Magenta Concrete Powder', 'Magenta Glazed Terracotta', 'Magenta Shulker Box', 'Magenta Stained Glass', 'Magenta Stained Glass Pane', 'Magenta Terracotta', 'Magenta Wool', 'Magma Block', 'Mangrove Button', 'Mangrove Door', 'Mangrove Fence', 'Mangrove Fence Gate', 'Mangrove Hanging Sign', 'Mangrove Leaves', 'Mangrove Log', 'Mangrove Pressure Plate', 'Mangrove Propagule', 'Mangrove Planks', 'Mangrove Roots', 'Mangrove Sign', 'Mangrove Slab', 'Mangrove Stairs', 'Mangrove Trapdoor', 'Mangrove Wood', 'Medium Amethyst Bud', 'Melon', 'Melon Stem', 'Moss Block', 'Moss Carpet', 'Mossy Cobblestone', 'Mossy Cobblestone Slab', 'Mossy Cobblestone Stairs', 'Mossy Cobblestone Wall', 'Mossy Stone Brick Slab', 'Mossy Stone Brick Stairs', 'Mossy Stone Brick Wall', 'Mossy Stone Bricks', 'Mud', 'Mud Brick Slab', 'Mud Brick Stairs', 'Mud Brick Wall', 'Mud Bricks', 'Muddy Mangrove Roots', 'Mushroom Stem', 'Mycelium', 'Nether Brick Fence', 'Nether Brick Slab', 'Nether Brick Stairs', 'Nether Brick Wall', 'Nether Bricks', 'Nether Gold Ore', 'Nether Quartz Ore', 'Nether Sprouts', 'Nether Wart', 'Nether Wart Block', 'Netherrack', 'Note Block', 'Oak Button', 'Oak Door', 'Oak Fence', 'Oak Fence Gate', 'Oak Hanging Sign', 'Oak Leaves', 'Oak Log', 'Oak Planks', 'Oak Pressure Plate', 'Oak Sapling', 'Oak Sign', 'Oak Slab', 'Oak Stairs', 'Oak Trapdoor', 'Oak Wood', 'Observer', 'Obsidian', 'Ochre Froglight', 'Ominous Banner', 'Orange Banner', 'Orange Bed', 'Orange Candle', 'Orange Carpet', 'Orange Concrete', 'Orange Concrete Powder', 'Orange Glazed Terracotta', 'Orange Shulker Box', 'Orange Stained Glass', 'Orange Stained Glass Pane', 'Orange Terracotta', 'Orange Tulip', 'Orange Wool', 'Oxeye Daisy', 'Oxidized Copper', 'Oxidized Cut Copper', 'Oxidized Cut Copper Slab', 'Oxidized Cut Copper Stairs', 'Packed Ice', 'Packed Mud', 'Pearlescent Froglight', 'Peony', 'Petrified Oak Slab', 'File:Piglin Head.png', 'Piglin Head', 'Pink Banner', 'Pink Bed', 'Pink Candle', 'Pink Carpet', 'Pink Concrete', 'Pink Concrete Powder', 'Pink Glazed Terracotta', 'Pink Shulker Box', 'Pink Stained Glass', 'Pink Stained Glass Pane', 'Pink Terracotta', 'Pink Tulip', 'Pink Wool', 'Piston', 'Player Head', 'Podzol', 'Pointed Dripstone', 'Polished Andesite', 'Polished Andesite Slab', 'Polished Andesite Stairs', 'Polished Basalt', 'Polished Blackstone', 'Polished Blackstone Brick Slab', 'Polished Blackstone Brick Stairs', 'Polished Blackstone Brick Wall', 'Polished Blackstone Bricks', 'Polished Blackstone Button', 'Polished Blackstone Pressure Plate', 'Polished Blackstone Slab', 'Polished Blackstone Stairs', 'Polished Blackstone Wall', 'Polished Diorite', 'Polished Diorite Slab', 'Polished Diorite Stairs', 'Polished Granite', 'Polished Granite Slab', 'Polished Granite Stairs', 'Polished Deepslate', 'Polished Deepslate Slab', 'Polished Deepslate Stairs', 'Polished Deepslate Wall', 'Poppy', 'Potatoes', 'Powder Snow', 'Powered Rail', 'Prismarine', 'Prismarine Brick Slab', 'Prismarine Brick Stairs', 'Prismarine Bricks', 'Prismarine Slab', 'Prismarine Stairs', 'Prismarine Wall', 'Pumpkin', 'Pumpkin Stem', 'Purple Banner', 'Purple Bed', 'Purple Candle', 'Purple Carpet', 'Purple Concrete', 'Purple Concrete Powder', 'Purple Glazed Terracotta', 'Purple Shulker Box', 'Purple Stained Glass', 'Purple Stained Glass Pane', 'Purple Terracotta', 'Purple Wool', 'Purpur Block', 'Purpur Pillar', 'Purpur Slab', 'Purpur Stairs', 'Quartz Bricks', 'Quartz Pillar', 'Quartz Slab', 'Quartz Stairs', 'Rail', 'Red Banner', 'Red Bed', 'Red Candle', 'Red Carpet', 'Red Concrete', 'Red Concrete Powder', 'Red Glazed Terracotta', 'Red Mushroom', 'Red Mushroom Block', 'Red Nether Brick Slab', 'Red Nether Brick Stairs', 'Red Nether Brick Wall', 'Red Nether Bricks', 'Red Sand', 'Red Sandstone', 'Red Sandstone Slab', 'Red Sandstone Stairs', 'Red Sandstone Wall', 'Red Shulker Box', 'Red Stained Glass', 'Red Stained Glass Pane', 'Red Terracotta', 'Red Tulip', 'Red Wool', 'Redstone Comparator', 'Redstone Lamp', 'Redstone Ore', 'Redstone Repeater', 'Redstone Torch', 'Redstone Wire', 'Reinforced Deepslate', 'Repeating Command Block', 'Respawn Anchor', 'Rooted Dirt', 'Rose Bush', 'Sand', 'Sandstone', 'Sandstone Slab', 'Sandstone Stairs', 'Sandstone Wall', 'Scaffolding', 'Sculk', 'Sculk Catalyst', 'Sculk Sensor', 'Sculk Shrieker', 'Sculk Vein', 'Sea Lantern', 'Sea Pickle', 'Seagrass', 'Shroomlight', 'Shulker Box', 'Skeleton Skull', 'Slime Block', 'Small Amethyst Bud', 'Small Dripleaf', 'Smithing Table', 'Smoker', 'Smooth Basalt', 'Smooth Quartz Block', 'Smooth Quartz Slab', 'Smooth Quartz Stairs', 'Smooth Red Sandstone', 'Smooth Red Sandstone Slab', 'Smooth Red Sandstone Stairs', 'Smooth Sandstone', 'Smooth Sandstone Slab', 'Smooth Sandstone Stairs', 'Smooth Stone', 'Smooth Stone Slab', 'Snow', 'Snow Block', 'Soul Campfire', 'Soul Fire', 'Soul Lantern', 'Soul Sand', 'Soul Soil', 'Soul Torch', 'Spawner', 'Sponge', 'Spore Blossom', 'Spruce Button', 'Spruce Door', 'Spruce Fence', 'Spruce Fence Gate', 'Spruce Hanging Sign', 'Spruce Leaves', 'Spruce Log', 'Spruce Planks', 'Spruce Pressure Plate', 'Spruce Sapling', 'Spruce Sign', 'Spruce Slab', 'Spruce Stairs', 'Spruce Trapdoor', 'Spruce Wood', 'Sticky Piston', 'Stone', 'Stone Brick Slab', 'Stone Brick Stairs', 'Stone Brick Wall', 'Stone Bricks', 'Stone Button', 'Stone Pressure Plate', 'Stone Slab', 'Stone Stairs', 'Stonecutter', 'Stripped Acacia Log', 'Stripped Acacia Wood', 'Stripped Birch Log', 'Stripped Birch Wood', 'Stripped Crimson Hyphae', 'Stripped Crimson Stem', 'Stripped Dark Oak Log', 'Stripped Dark Oak Wood', 'Stripped Jungle Log', 'Stripped Jungle Wood', 'Stripped Mangrove Log', 'Stripped Mangrove Wood', 'Stripped Oak Log', 'Stripped Oak Wood', 'Stripped Spruce Log', 'Stripped Spruce Wood', 'Stripped Warped Hyphae', 'Stripped Warped Stem', 'Structure Block', 'Structure Void', 'Sugar Cane', 'Sunflower', 'Sweet Berry Bush', 'Tall Grass', 'Tall Seagrass', 'Target', 'Terracotta', 'Tinted Glass', 'TNT', 'Torch', 'Trapped Chest', 'Tripwire', 'Tripwire Hook', 'Tube Coral', 'Tube Coral Block', 'Tube Coral Fan', 'Tuff', 'Turtle Egg', 'Twisting Vines', 'Verdant Froglight', 'Vines', 'Warped Button', 'Warped Door', 'Warped Fence', 'Warped Fence Gate', 'Warped Fungus', 'Warped Hanging Sign', 'Warped Hyphae', 'Warped Nylium', 'Warped Planks', 'Warped Pressure Plate', 'Warped Roots', 'Warped Sign', 'Warped Slab', 'Warped Stairs', 'Warped Stem', 'Warped Trapdoor', 'Warped Wart Block', 'Water', 'Waxed Block of Copper', 'Waxed Cut Copper', 'Waxed Cut Copper Slab', 'Waxed Cut Copper Stairs', 'Waxed Exposed Copper', 'Waxed Exposed Cut Copper', 'Waxed Exposed Cut Copper Slab', 'Waxed Exposed Cut Copper Stairs', 'Waxed Oxidized Copper', 'Waxed Oxidized Cut Copper', 'Waxed Oxidized Cut Copper Slab', 'Waxed Oxidized Cut Copper Stairs', 'Waxed Weathered Copper', 'Waxed Weathered Cut Copper', 'Waxed Weathered Cut Copper Slab', 'Waxed Weathered Cut Copper Stairs', 'Weathered Copper', 'Weathered Cut Copper', 'Weathered Cut Copper Slab', 'Weathered Cut Copper Stairs', 'Weeping Vines', 'Wet Sponge', 'Wheat Crops', 'White Banner', 'White Bed', 'White Candle', 'White Carpet', 'White Concrete', 'White Concrete Powder', 'White Glazed Terracotta', 'White Shulker Box', 'White Stained Glass', 'White Stained Glass Pane', 'White Terracotta', 'White Tulip', 'White Wool', 'Wither Rose', 'Wither Skeleton Skull', 'Yellow Banner', 'Yellow Bed', 'Yellow Candle', 'Yellow Carpet', 'Yellow Concrete', 'Yellow Concrete Powder', 'Yellow Glazed Terracotta', 'Yellow Shulker Box', 'Yellow Stained Glass', 'Yellow Stained Glass Pane', 'Yellow Terracotta', 'Yellow Wool', 'Zombie Head']

# A list of blocks that are the same on all sides
SIMPLE_TEXTURES = [
    'minecraft:oak_wood',
    'minecraft:birch_wood',
    'minecraft:spruce_wood',
    'minecraft:jungle_wood',
    'minecraft:acacia_wood',
    'minecraft:dark_oak_wood',

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

    'minecraft:terracotta',
    'minecraft:white_terracotta',
    'minecraft:white_glazed_terracotta',
    'minecraft:yellow_terracotta',
    'minecraft:yellow_glazed_terracotta',
    'minecraft:red_terracotta',
    'minecraft:red_glazed_terracotta',
    'minecraft:light_blue_terracotta',
    'minecraft:light_blue_glazed_terracotta',
    'minecraft:light_gray_terracotta',
    'minecraft:light_gray_glazed_terracotta',
    'minecraft:lime_terracotta',
    'minecraft:lime_glazed_terracotta',
    'minecraft:magenta_terracotta',
    'minecraft:magenta_glazed_terracotta',
    'minecraft:orange_terracotta',
    'minecraft:orange_glazed_terracotta',
    'minecraft:pink_terracotta',
    'minecraft:pink_glazed_terracotta',
    'minecraft:purple_terracotta',
    'minecraft:purple_glazed_terracotta',
    'minecraft:cyan_terracotta',
    'minecraft:cyan_glazed_terracotta',
    'minecraft:gray_terracotta',
    'minecraft:gray_glazed_terracotta',
    'minecraft:green_terracotta',
    'minecraft:green_glazed_terracotta',
    'minecraft:black_terracotta',
    'minecraft:black_glazed_terracotta',
    'minecraft:blue_terracotta',
    'minecraft:blue_glazed_terracotta',
    'minecraft:brown_terracotta',
    'minecraft:brown_glazed_terracotta',

    'minecraft:shulker_box',
    'minecraft:white_shulker_box',
    'minecraft:yellow_shulker_box',
    'minecraft:red_shulker_box',
    'minecraft:light_blue_shulker_box',
    'minecraft:light_gray_shulker_box',
    'minecraft:lime_shulker_box',
    'minecraft:magenta_shulker_box',
    'minecraft:orange_shulker_box',
    'minecraft:pink_shulker_box',
    'minecraft:purple_shulker_box',
    'minecraft:cyan_shulker_box',
    'minecraft:gray_shulker_box',
    'minecraft:green_shulker_box',
    'minecraft:black_shulker_box',
    'minecraft:blue_shulker_box',
    'minecraft:brown_shulker_box',

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

    'minecraft:cut_copper',
    'minecraft:weathered_copper',
    'minecraft:oxidized_copper',
    'minecraft:exposed_copper',
    'minecraft:weathered_cut_copper',
    'minecraft:oxidized_cut_copper',
    'minecraft:exposed_cut_copper',
    'minecraft:waxed_copper',
    'minecraft:waxed_weathered_copper',
    'minecraft:waxed_oxidized_copper',
    'minecraft:waxed_exposed_copper',
    'minecraft:waxed_cut_copper',
    'minecraft:waxed_weathered_cut_copper',
    'minecraft:waxed_oxidized_cut_copper',
    'minecraft:waxed_exposed_cut_copper',

    'minecraft:dirt',
    'minecraft:coarse_dirt',
    'minecraft:rooted_dirt',
    'minecraft:stone',
    'minecraft:smooth_stone',
    'minecraft:stone_bricks',
    'minecraft:mossy_stone_bricks',
    'minecraft:chiseled_stone_bricks',
    'minecraft:cracked_stone_bricks',
    'minecraft:end_stone',
    'minecraft:end_stone_bricks',
    'minecraft:cobblestone',
    'minecraft:mossy_cobblestone',
    'minecraft:bedrock',
    'minecraft:bricks',
    'minecraft:clay',
    'minecraft:quartz_bricks',
    'minecraft:mud',
    'minecraft:gravel',

    'minecraft:sand',
    'minecraft:red_sand',
    'minecraft:soul_sand',

    'minecraft:deepslate_bricks',
    'minecraft:deepslate_tiles',
    'minecraft:cracked_deepslate_bricks',
    'minecraft:cracked_deepslate_tiles',
    'minecraft:cobbled_deepslate',
    'minecraft:chiseled_deepslate',

    'minecraft:diorite',
    'minecraft:granite',
    'minecraft:andesite',
    'minecraft:calcite',
    'minecraft:tuff',
    'minecraft:dripstone_block',
    'minecraft:purpur_block',

    'minecraft:polished_blackstone',
    'minecraft:polished_blackstone_bricks',
    'minecraft:polished_deepslate',
    'minecraft:polished_diorite',
    'minecraft:polished_granite',
    'minecraft:polished_andesite',

    'minecraft:glowstone',
    'minecraft:amethyst_block',
    'minecraft:budding_amethyst',
    'minecraft:netherrack',
    'minecraft:netherite_block',
    'minecraft:nether_bricks',
    'minecraft:red_nether_bricks',
]

MULTI_TEXTURE_WITH_CROSS = {
    # Sources, Sides, Side to Cross
    'minecraft:mangrove_roots': [['mangrove_roots_side.png', 'mangrove_roots_top.png'], [0, 1, 0, 1, 0, 0], 0]
}

SIMPLE_ANIMATED_TEXTURES = {
    # Source Image, Frames
    'minecraft:warped_hyphae': ['warped_stem.png', 5],
    'minecraft:crimson_hyphae': ['crimson_stem.png', 5],
}

MULTI_ANIMATION_TEXTURES = {
    # Sources, Sides, Animated Texture Index, Frames
    'minecraft:warped_stem': [['warped_stem.png', 'warped_stem_top.png'], [0, 1, 0, 1, 0, 0], 0, 5],
    'minecraft:crimson_stem': [['crimson_stem.png', 'crimson_stem_top.png'], [0, 1, 0, 1, 0, 0], 0, 5],
}

MULTI_TEXTURES = {  # Front, Top, Left, Bottom, Right, Back
    'minecraft:oak_log':                  [['oak_log.png', 'oak_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_oak_log':         [['stripped_oak_log.png', 'stripped_oak_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:birch_log':                [['birch_log.png', 'birch_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_birch_log':       [['stripped_birch_log.png', 'stripped_birch_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:spruce_log':               [['spruce_log.png', 'spruce_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_spruce_log':      [['stripped_spruce_log.png', 'stripped_spruce_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:jungle_log':               [['jungle_log.png', 'jungle_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_jungle_log':      [['stripped_jungle_log.png', 'stripped_jungle_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:acacia_log':               [['acacia_log.png', 'acacia_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_acacia_log':      [['stripped_acacia_log.png', 'stripped_acacia_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:dark_oak_log':             [['dark_oak_log.png', 'dark_oak_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_dark_oak_log':    [['stripped_dark_oak_log.png', 'stripped_dark_oak_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:mangrove_log':             [['mangrove_log.png', 'mangrove_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:muddy_mangrove_roots':     [['muddy_mangrove_roots_side.png', 'muddy_mangrove_roots_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_mangrove_log':    [['stripped_mangrove_log.png', 'stripped_mangrove_log_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_warped_stem':     [['stripped_warped_stem.png', 'stripped_warped_stem_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:stripped_crimson_stem':    [['stripped_crimson_stem.png', 'stripped_crimson_stem_top.png'], [0, 1, 0, 1, 0, 0]],

    'minecraft:grass_block':              [['dirt.png', 'grass_block_side.png', 'grass_block_top.png'], [1, 2, 1, 0, 1, 1]],
    'minecraft:podzol':                   [['dirt.png', 'podzol_side.png', 'podzol_top.png'], [1, 2, 1, 0, 1, 1]],
    'minecraft:crimson_nylium':           [['netherrack.png', 'crimson_nylium_side.png', 'crimson_nylium.png'], [1, 2, 1, 0, 1, 1]],
    'minecraft:warped_nylium':            [['netherrack.png', 'warped_nylium_side.png', 'warped_nylium.png'], [1, 2, 1, 0, 1, 1]],
    'minecraft:quartz_block':             [['quartz_block_bottom.png', 'quartz_block_side.png', 'quartz_block_top.png'], [1, 2, 1, 0, 1, 1]],
    'minecraft:quartz_pillar':            [['quartz_pillar_top.png', 'quartz_pillar.png'], [1, 0, 1, 0, 1, 1]],
    'minecraft:purpur_pillar':            [['purpur_pillar_top.png', 'purpur_pillar.png'], [1, 0, 1, 0, 1, 1]],
    'minecraft:chiseled_quartz':          [['chiseled_quartz_block.png', 'chiseled_quartz_block_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:blackstone':               [['blackstone.png', 'blackstone_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:bone_block':               [['bone_block_side.png', 'bone_block_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:sandstone':                [['sandstone.png', 'sandstone_bottom.png', 'sandstone_top.png'], [0, 2, 0, 1, 0, 0]],
    'minecraft:cut_sandstone':            [['cut_sandstone.png', 'sandstone_bottom.png', 'sandstone_top.png'], [0, 2, 0, 1, 0, 0]],
    'minecraft:chiseled_sandstone':       [['chiseled_sandstone.png', 'sandstone_bottom.png', 'sandstone_top.png'], [0, 2, 0, 1, 0, 0]],
    'minecraft:red_sandstone':            [['red_sandstone.png', 'red_sandstone_bottom.png', 'red_sandstone_top.png'], [0, 2, 0, 1, 0, 0]],
    'minecraft:cut_red_sandstone':        [['cut_red_sandstone.png', 'red_sandstone_bottom.png', 'red_sandstone_top.png'], [0, 2, 0, 1, 0, 0]],
    'minecraft:chiseled_red_sandstone':   [['chiseled_red_sandstone.png', 'red_sandstone_bottom.png', 'red_sandstone_top.png'], [0, 2, 0, 1, 0, 0]],
    'minecraft:double_smooth_stone_slab': [['smooth_stone_slab_side.png', 'smooth_stone.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:deepslate':                [['deepslate.png', 'deepslate_top.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:reinforced_deepslate':     [['reinforced_deepslate_side.png', 'reinforced_deepslate_top.png', 'reinforced_deepslate_bottom.png'], [0, 1, 0, 2, 0, 0]],
    'minecraft:chiseled_nether_bricks':   [['chiseled_nether_bricks.png', 'nether_bricks.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:cracked_nether_bricks':    [['cracked_nether_bricks.png', 'nether_bricks.png'], [0, 1, 0, 1, 0, 0]],
    'minecraft:ancient_debris':           [['ancient_debris_side.png', 'ancient_debris_top.png'], [0, 1, 0, 1, 0, 0]],
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
    0.5:  {
        'minecraft:oak_slab': 'minecraft:oak_planks',
        'minecraft:spruce_slab': 'minecraft:spruce_planks',
        'minecraft:birch_slab': 'minecraft:birch_planks',
        'minecraft:jungle_slab': 'minecraft:jungle_planks',
        'minecraft:acacia_slab': 'minecraft:acacia_planks',
        'minecraft:dark_oak_slab': 'minecraft:dark_oak_planks',
        'minecraft:crimson_slab': 'minecraft:crimson_planks',
        'minecraft:warped_slab': 'minecraft:warped_planks',
        'minecraft:stone_slab': 'minecraft:stone',
        'minecraft:smooth_stone_slab': 'minecraft:smooth_stone',
        'minecraft:sandstone_slab': 'minecraft:sandstone',
        'minecraft:cut_sandstone_slab': 'minecraft:cut_sandstone',
        'minecraft:petrified_oak_slab': 'minecraft:oak_planks',
        'minecraft:cobblestone_slab': 'minecraft:cobblestone',
        'minecraft:bricks': 'minecraft:bricks',
        'minecraft:stone_brick_slab': 'minecraft:stone_bricks',
        'minecraft:nether_brick_slab': 'minecraft:nether_bricks',
        'minecraft:quartz_slab': 'minecraft:quartz_block',
        'minecraft:red_sandstone_slab': 'minecraft:red_sandstone',
        'minecraft:cut_red_sandstone_slab': 'minecraft:cut_red_sandstone',
        'minecraft:purpur_slab': 'minecraft:purpur_block',
        'minecraft:prismarine_slab': 'minecraft:prismarine',
        'minecraft:prismarine_brick_slab': 'minecraft:prismarine_bricks',
        'minecraft:dark_prismarine_slab': 'minecraft:dark_prismarine',
        'minecraft:polished_granite_slab': 'minecraft:polished_granite',
        'minecraft:smooth_red_sandstone_slab': 'minecraft:smooth_red_sandstone',
        'minecraft:mossy_stone_brick_slab': 'minecraft:mossy_stone_bricks',
        'minecraft:polished_diorite_slab': 'minecraft:polished_diorite',
        'minecraft:mossy_cobblestone_slab': 'minecraft:mossy_cobblestone',
        'minecraft:end_stone_brick_slab': 'minecraft:end_stone_bricks',
        'minecraft:smooth_sandstone_slab': 'minecraft:smooth_sandstone',
        'minecraft:smooth_quartz_slab': 'minecraft:smooth_quartz_block',
        'minecraft:granite_slab': 'minecraft:granite',
        'minecraft:andesite_slab': 'minecraft:andesite',
        'minecraft:red_nether_brick_slab': 'minecraft:red_nether_bricks',
        'minecraft:polished_andesite_slab': 'minecraft:polished_andesite',
        'minecraft:diorite_slab': 'minecraft:diorite',
        'minecraft:blackstone_slab': 'minecraft:blackstone',
        'minecraft:polished_blackstone_slab': 'minecraft:polished_blackstone',
        'minecraft:polished_blackstone_brick_slab': 'minecraft:polished_blackstone_bricks',
        'minecraft:cobbled_deepslate_slab': 'minecraft:cobbled_deepslate',
        'minecraft:cut_copper_slab': 'minecraft:cut_copper',
        'minecraft:deepslate_brick_slab': 'minecraft:deepslate_bricks',
        'minecraft:deepslate_tile_slab': 'minecraft:deepslate_tiles',
        'minecraft:exposed_cut_copper_slab': 'minecraft:exposed_cut_copper',
        'minecraft:oxidized_cut_copper_slab': 'minecraft:oxidized_cut_copper',
        'minecraft:polished_deepslate_slab': 'minecraft:polished_deepslate',
        'minecraft:waxed_cut_copper_slab': 'minecraft:waxed_cut_copper',
        'minecraft:waxed_exposed_cut_copper_slab': 'minecraft:waxed_exposed_cut_copper',
        'minecraft:waxed_oxidized_cut_copper_slab': 'minecraft:waxed_oxidized_cut_copper',
        'minecraft:waxed_weathered_cut_copper_slab': 'minecraft:waxed_weathered_cut_copper',
        'minecraft:weathered_cut_copper_slab': 'minecraft:weathered_cut_copper'},
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

STAIR_TEXTURES = {
    'minecraft:purpur_stairs': 'minecraft:purpur_block',
    'minecraft:oak_stairs': 'minecraft:oak_planks',
    'minecraft:cobblestone_stairs': 'minecraft:cobblestone',
    'minecraft:brick_stairs': 'minecraft:bricks',
    'minecraft:stone_brick_stairs': 'minecraft:stone_bricks',
    'minecraft:nether_brick_stairs': 'minecraft:nether_bricks',
    'minecraft:sandstone_stairs': 'minecraft:sandstone',
    'minecraft:spruce_stairs': 'minecraft:spruce_planks',
    'minecraft:birch_stairs': 'minecraft:birch_planks',
    'minecraft:jungle_stairs': 'minecraft:jungle_planks',
    'minecraft:quartz_stairs': 'minecraft:quartz_block',
    'minecraft:acacia_stairs': 'minecraft:acacia_planks',
    'minecraft:dark_oak_stairs': 'minecraft:dark_oak_planks',
    'minecraft:prismarine_stairs': 'minecraft:prismarine',
    'minecraft:prismarine_brick_stairs': 'minecraft:prismarine_bricks',
    'minecraft:dark_prismarine_stairs': 'minecraft:dark_prismarine',
    'minecraft:red_sandstone_stairs': 'minecraft:red_sandstone',
    'minecraft:polished_granite_stairs': 'minecraft:polished_granite',
    'minecraft:cut_red_sandstone_stairs': 'minecraft:red_sandstone',
    'minecraft:mossy_stone_brick_stairs': 'minecraft:stone_bricks',
    'minecraft:polished_diorite_stairs': 'minecraft:polished_diorite',
    'minecraft:mossy_cobblestone_stairs': 'minecraft:mossy_cobblestone',
    'minecraft:end_stone_brick_stairs': 'minecraft:end_stone_bricks',
    'minecraft:stone_stairs': 'minecraft:stone',
    'minecraft:smooth_sandstone_stairs': 'minecraft:smooth_sandstone',
    'minecraft:smooth_quartz_stairs': 'minecraft:smooth quartz',
    'minecraft:granite_stairs': 'minecraft:granite',
    'minecraft:andesite_stairs': 'minecraft:andesite',
    'minecraft:red_nether_brick_stairs': 'minecraft:red_nether_bricks',
    'minecraft:polished_andesite_stairs': 'minecraft:polished_andesite',
    'minecraft:diorite_stairs': 'minecraft:diorite',
    'minecraft:crimson_stairs': 'minecraft:crimson_planks',
    'minecraft:warped_stairs': 'minecraft:warped_planks',
    'minecraft:blackstone_stairs': 'minecraft:blackstone',
    'minecraft:polished_blackstone_stairs': 'minecraft:polished_blackstone',
    'minecraft:polished_blackstone_brick_stairs': 'minecraft:polished_blackstone_bricks',
    'minecraft:cobbled_deepslate_stairs': 'minecraft:cobbled_deepslate',
    'minecraft:cut_copper_stairs': 'minecraft:cut_copper',
    'minecraft:deepslate_brick_stairs': 'minecraft:deepslate',
    'minecraft:deepslate_tile_stairs': 'minecraft:deepslate_tiles',
    'minecraft:exposed_cut_copper_stairs': 'minecraft:cut_copper',
    'minecraft:oxidized_cut_copper_stairs': 'minecraft:oxidized_cut_copper',
    'minecraft:polished_deepslate_stairs': 'minecraft:polished_deepslate',
    'minecraft:waxed_cut_copper_stairs': 'minecraft:waxed_cut_copper',
    'minecraft:waxed_exposed_cut_copper_stairs': 'minecraft:waxed_exposed_cut_copper',
    'minecraft:waxed_oxidized_cut_copper_stairs': 'minecraft:waxed_oxidized_cut_copper',
    'minecraft:waxed_weathered_cut_copper_stairs': 'minecraft:waxed_weathered_cut_copper',
    'minecraft:weathered_cut_copper_stairs': 'minecraft:weathered_cut_copper',
}
STAIR_TEXTURES_LIST = list(STAIR_TEXTURES.keys())

CATEGORIES = [
    'SIMPLE',
    'SIMPLE_05',
    'SIMPLE_015',
    'SIMPLE_01',
    'SIMPLE_001',
    'MULTI_TEXTURE',
    'STAIRS',
]

if __name__ == "__main__":
    asset_files = list(listdir('local/block_assets'))

    # block_ids = [f'minecraft:' + x.lower().replace(' ', '_') for x in all_block_ids]
    # for block_id in SIMPLE_TEXTURES:
    #     if block_id in block_ids:
    #         block_ids.remove(block_id)
    # for block_id in MULTI_TEXTURES.keys():
    #     if block_id in block_ids:
    #         block_ids.remove(block_id)
    # if len(block_ids) > 0:
    #     print('Not all blocks found')
    #     for block in block_ids:
    #         print(block)
    #     exit(1)

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
        file.write('\n')
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
        file.write('typedef struct {\n')
        file.write('uint8_t category;\n')
        file.write('uint8_t index;\n')
        file.write('} LinkedTexture;\n')
        file.write('\n')
        file.write('LinkedTexture STAIR_TEXTURES[] = {\n')
        for ix, (blockID, materialID) in enumerate(STAIR_TEXTURES.items()):
            if materialID in SIMPLE_TEXTURES:
                category = 0
                index = SIMPLE_TEXTURES.index(materialID)
            elif materialID in MULTI_TEXTURES_LIST:
                category = 1
                index = MULTI_TEXTURES_LIST.index(materialID)
            else:
                print(f'MaterialID {materialID} not found')
                continue
            file.write(f' /* {ix} */ '.ljust(11) + ('{' + f'{category}, {index}').ljust(7) + '}, // ' + blockID + '\n')
        file.write('};\n')
        file.write('\n')
        for vh_ix, (height, vh_list) in enumerate(VARIABLE_HEIGHT.items()):
            file.write('LinkedTexture SIMPLE_' + str(height)[2:] + '[] = {\n')
            for ix, (blockID, materialID) in enumerate(vh_list):
                if materialID in SIMPLE_TEXTURES:
                    category = 0
                    index = SIMPLE_TEXTURES.index(materialID)
                elif materialID in MULTI_TEXTURES_LIST:
                    category = 1
                    index = MULTI_TEXTURES_LIST.index(materialID)
                else:
                    print(f'MaterialID {materialID} not found')
                    continue
            file.write('};\n')
            file.write('\n')
        file.write('#endif //LIBVOXEL_TEXTURES_H')
