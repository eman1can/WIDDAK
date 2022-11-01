//
// Created by Zoe on 10/31/2022.
//

#ifndef LIBVOXEL_TEXTURES_H
#define LIBVOXEL_TEXTURES_H

#include <stdint.h>

typedef enum {
    SIMPLE,
    MULTI_IMAGE,
    CUSTOM_SIZE,
    STAIR,
    FENCE_POST,
    FENCE_GATE,
    COMPLEX
} Category;

// Simple textures
// See /gdcp/textures.py for generator
const char* SIMPLE_TEXTURE_IMAGES[] = {
        "local/block_assets/dirt.png",
        "local/block_assets/coarse_dirt.png",
        "local/block_assets/gravel.png",
        "local/block_assets/sand.png",
        "local/block_assets/red_sand.png",
        "local/block_assets/cobblestone.png",
        "local/block_assets/stone.png",
        "local/block_assets/smooth_stone.png",
        "local/block_assets/stone_bricks.png",
        "local/block_assets/mossy_stone_bricks.png",
        "local/block_assets/cracked_stone_bricks.png",
        "local/block_assets/chiseled_stone_bricks.png",
        "local/block_assets/infested_stone.png",
        "local/block_assets/infested_cobblestone.png",
        "local/block_assets/infested_stone_bricks.png",
        "local/block_assets/infested_mossy_stone_bricks.png",
        "local/block_assets/infested_cracked_stone_bricks.png",
        "local/block_assets/infested_chiseled_stone_bricks.png",
        "local/block_assets/granite.png",
        "local/block_assets/polished_granite.png",
        "local/block_assets/diorite.png",
        "local/block_assets/polished_diorite.png",
        "local/block_assets/andesite.png",
        "local/block_assets/polished_andesite.png",
        "local/block_assets/bedrock.png",
        "local/block_assets/oak_planks.png",
        "local/block_assets/spruce_planks.png",
        "local/block_assets/birch_planks.png",
        "local/block_assets/jungle_planks.png",
        "local/block_assets/acacia_planks.png",
        "local/block_assets/dark_oak_planks.png",
        "local/block_assets/oak_leaves.png",
        "local/block_assets/spruce_leaves.png",
        "local/block_assets/birch_leaves.png",
        "local/block_assets/jungle_leaves.png",
        "local/block_assets/acacia_leaves.png",
        "local/block_assets/dark_oak_leaves.png",
        "local/block_assets/brown_mushroom_block.png",
        "local/block_assets/red_mushroom_block.png",
        "local/block_assets/coal_ore.png",
        "local/block_assets/coal_block.png",
        "local/block_assets/iron_ore.png",
        "local/block_assets/iron_block.png",
        "local/block_assets/copper_ore.png",
        "local/block_assets/copper_block.png",
        "local/block_assets/gold_ore.png",
        "local/block_assets/gold_block.png",
        "local/block_assets/lapis_ore.png",
        "local/block_assets/lapis_block.png",
        "local/block_assets/diamond_ore.png",
        "local/block_assets/diamond_block.png",
        "local/block_assets/redstone_ore.png",
        "local/block_assets/redstone_block.png",
        "local/block_assets/emerald_ore.png",
        "local/block_assets/emerald_block.png",
        "local/block_assets/white_wool.png",
        "local/block_assets/orange_wool.png",
        "local/block_assets/magenta_wool.png",
        "local/block_assets/light_blue_wool.png",
        "local/block_assets/yellow_wool.png",
        "local/block_assets/lime_wool.png",
        "local/block_assets/pink_wool.png",
        "local/block_assets/gray_wool.png",
        "local/block_assets/light_gray_wool.png",
        "local/block_assets/cyan_wool.png",
        "local/block_assets/purple_wool.png",
        "local/block_assets/blue_wool.png",
        "local/block_assets/brown_wool.png",
        "local/block_assets/green_wool.png",
        "local/block_assets/red_wool.png",
        "local/block_assets/black_wool.png",
        "local/block_assets/sponge.png",
        "local/block_assets/wet_sponge.png",
        "local/block_assets/glass.png",
        "local/block_assets/note_block.png",
        "local/block_assets/smooth_quartz.png",
        "local/block_assets/quartz_block.png",
        "local/block_assets/bricks.png",
        "local/block_assets/mossy_cobblestone.png",
        "local/block_assets/obsidian.png",
        "local/block_assets/purpur_block.png",
        "local/block_assets/spawner.png",
        "local/block_assets/ice.png",
        "local/block_assets/snow_block.png",
        "local/block_assets/clay.png",
        "local/block_assets/netherrack.png",
        "local/block_assets/soul_sand.png",
        "local/block_assets/glowstone.png",
        "local/block_assets/nether_bricks.png",
        "local/block_assets/red_nether_bricks.png",
        "local/block_assets/end_stone.png",
        "local/block_assets/end_stone_bricks.png",
        "local/block_assets/redstone_lamp.png",
};

typedef enum {
    UNKNOWN,
    NORTH,
    SOUTH,
    EAST,
    WEST
} Heading;

typedef struct {
    float size[3];
    const char* textures[6];
    uint8_t texture_ids[6];
    Heading facing;
} TextureDefinition;

TextureDefinition COMPLEX_TEXTURES[] = {
        {
            {1, 0.2,  1},
            {"local/block_assets/oak_trapdoor.png"},
            {0, 0, 0, 0, 0, 0},
            UNKNOWN,
        }, {
            {1, 1, 1},
            // TODO: Change to utilize color?
            {"local/block_assets/grass_block_side.png", "local/block_assets/grass_block_top.png", "grass_block_bottom"},
            {}
        }
};

#endif //LIBVOXEL_TEXTURES_H
