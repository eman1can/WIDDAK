//
// Created by Zoe on 11/11/2022.
//

#include <cstdlib>
#include <iostream>

#include <SDL_image.h>

#include "shape.h"
#include "renderer.h"
#undef main

using namespace std;

int main() {
    auto renderer = new Renderer(720, 640);
    if (renderer->init() != 0) {
        fprintf(stderr, "Failed to init renderer\n");
        return 1;
    }

    renderer->addVoxel(glm::fvec3(-3, -1, -8), 37, 2, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-3, -1, -7), 37, 2, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-3, -1, -6), 37, 2, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-3, -1, -5), 37, 2, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-3, -1, -4), 37, 2, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-3, 2, -10), 41, 2, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-3, 2, -2), 44, 0, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-3, 3, -9), 41, 4, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-3, 3, -8), 37, 8, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-3, 3, -7), 37, 8, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-3, 3, -6), 37, 8, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-3, 3, -5), 37, 8, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-3, 3, -4), 37, 8, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-3, 3, -3), 44, 0, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-2, 2, -10), 57, 4, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-2, 2, -2), 60, 0, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-2, 3, -9), 57, 4, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-2, 3, -3), 60, 0, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-1, 2, -10), 49, 4, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-1, 2, -2), 52, 0, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-1, 3, -9), 56, 4, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-1, 3, -3), 56, 0, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(0, -3, 0), 56, 0, 2, 3); // minecraft:brick_stairs
    renderer->addVoxel(glm::fvec3(0, -2, -1), 48, 0, 2, 3); // minecraft:brick_stairs
    renderer->addVoxel(glm::fvec3(0, 2, -10), 49, 4, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(0, 2, -2), 52, 0, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(0, 3, -9), 56, 4, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(0, 3, -3), 56, 0, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(1, -3, 0), 56, 0, 2, 3); // minecraft:brick_stairs
    renderer->addVoxel(glm::fvec3(1, -2, -1), 48, 0, 2, 3); // minecraft:brick_stairs
    renderer->addVoxel(glm::fvec3(1, -1, -2), 52, 0, 2, 3); // minecraft:brick_stairs
    renderer->addVoxel(glm::fvec3(1, 2, -10), 49, 4, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(1, 2, -2), 52, 0, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(1, 3, -9), 56, 4, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(1, 3, -3), 56, 0, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(2, -1, -9), 51, 10, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(1, -1, -9), 51, 10, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(-1, -1, -9), 51, 10, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(0, -1, -9), 51, 10, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(0, -1, -2), 52, 0, 2, 3); // minecraft:brick_stairs
    renderer->addVoxel(glm::fvec3(2, 2, -10), 49, 4, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(2, 2, -2), 52, 0, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(2, 3, -9), 56, 4, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(2, 3, -3), 56, 0, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(3, 2, -10), 57, 4, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(3, 2, -2), 60, 0, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(3, 3, -9), 25, 4, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(3, 3, -3), 28, 0, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(4, 2, -10), 25, 6, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(4, 2, -9), 29, 4, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(4, 2, -3), 29, 0, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(4, 2, -2), 28, 6, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(4, 3, -8), 25, 6, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(4, 3, -7), 29, 6, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(4, 3, -6), 29, 6, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(4, 3, -5), 29, 6, 2, 1); // minecraft:oak_stairs
    renderer->addVoxel(glm::fvec3(4, 3, -4), 28, 6, 2, 1); // minecraft:oak_stairs

    renderer->addVoxel(glm::fvec3(-5, -4, -10), 33, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-5, -4, -9), 37, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-5, -4, -8), 39, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-5, -4, -7), 37, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-5, -4, -6), 37, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-5, -4, -5), 37, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-5, -4, -4), 37, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-5, -4, -3), 39, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-5, -4, -2), 39, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-5, -4, -1), 39, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-5, -4, 0), 39, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-5, -4, 1), 36, 0, 1, 14); // minecraft:grass_block
// Skipping minecraft:white_tulip; Not found
// Skipping minecraft:pink_tulip; Not found
// Skipping minecraft:poppy; Not found
// Skipping minecraft:red_tulip; Not found
    renderer->addVoxel(glm::fvec3(-4, -4, -10), 49, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-4, -4, -9), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-4, -4, -8), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-4, -4, -7), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-4, -4, -6), 55, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-4, -4, -5), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-4, -4, -4), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-4, -4, -3), 55, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-4, -4, -2), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-4, -4, -1), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-4, -4, 0), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-4, -4, 1), 52, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-3, -4, -10), 49, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-3, -4, -9), 55, 0, 0, 162); // minecraft:dirt
    renderer->addVoxel(glm::fvec3(-3, -4, -8), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-3, -4, -7), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-3, -4, -6), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-3, -4, -5), 55, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-3, -4, -4), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-3, -4, -3), 55, 0, 0, 162); // minecraft:dirt
    renderer->addVoxel(glm::fvec3(-3, -4, -2), 55, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-3, -4, -1), 55, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-3, -4, 0), 55, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-3, -4, 1), 52, 0, 0, 175); // minecraft:bricks
    renderer->addVoxel(glm::fvec3(-3, -3, -9), 42, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-3, -3, -3), 59, 0, 1, 4); // minecraft:spruce_log
// Skipping minecraft:birch_leaves; Not found
    renderer->addVoxel(glm::fvec3(-3, -2, -9), 42, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-3, -2, -3), 42, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-3, -1, -9), 43, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-3, -1, -3), 46, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-3, 0, -9), 42, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-3, 0, -3), 42, 0, 1, 4); // minecraft:spruce_log
// Skipping minecraft:shroomlight; Not found
    renderer->addVoxel(glm::fvec3(-3, 1, -9), 46, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-3, 1, -3), 43, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-3, 2, -9), 46, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-3, 2, -3), 43, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-2, -4, -10), 51, 0, 0, 162); // minecraft:dirt
    renderer->addVoxel(glm::fvec3(-2, -4, -9), 55, 0, 0, 162); // minecraft:dirt
    renderer->addVoxel(glm::fvec3(-2, -4, -8), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-2, -4, -7), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-2, -4, -6), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-2, -4, -5), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-2, -4, -4), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-2, -4, -3), 55, 0, 0, 162); // minecraft:dirt
    renderer->addVoxel(glm::fvec3(-2, -4, -2), 55, 0, 0, 162); // minecraft:dirt
    renderer->addVoxel(glm::fvec3(-2, -4, -1), 55, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-2, -4, 0), 55, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-2, -4, 1), 52, 0, 0, 175); // minecraft:bricks
    renderer->addVoxel(glm::fvec3(-2, -3, -10), 11, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-2, -3, -9), 30, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-2, -3, -3), 27, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-2, -3, -2), 31, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-2, -2, -10), 11, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-2, -2, -9), 30, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-2, -2, -3), 27, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-2, -2, -2), 15, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-2, -1, -10), 11, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-2, -1, -8), 55, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(-2, -1, -7), 55, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(-2, -1, -6), 55, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(-2, -1, -5), 55, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(-2, -1, -4), 55, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(-2, -1, -2), 46, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-2, 0, -10), 11, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-2, 0, -8), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(-2, 0, -7), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(-2, 0, -6), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(-2, 0, -5), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(-2, 0, -4), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(-2, 0, -2), 14, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-2, 1, -10), 27, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-2, 1, -8), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(-2, 1, -7), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(-2, 1, -6), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(-2, 1, -5), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(-2, 1, -4), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(-2, 1, -2), 30, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(-2, 2, -8), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(-2, 2, -7), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(-2, 2, -6), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(-2, 2, -5), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(-2, 2, -4), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(-2, 3, -8), 31, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(-2, 3, -7), 31, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(-2, 3, -6), 31, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(-2, 3, -5), 31, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(-2, 3, -4), 31, 1, 1, 1); // minecraft:stripped_oak_log
// Skipping minecraft:oak_slab; Not found
    renderer->addVoxel(glm::fvec3(-1, -4, -10), 49, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-1, -4, -9), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-1, -4, -8), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-1, -4, -7), 55, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-1, -4, -6), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-1, -4, -5), 55, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-1, -4, -4), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-1, -4, -3), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-1, -4, -2), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-1, -4, -1), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(-1, -4, 0), 55, 0, 0, 175); // minecraft:bricks
    renderer->addVoxel(glm::fvec3(-1, -4, 1), 52, 0, 0, 175); // minecraft:bricks
// Skipping minecraft:spruce_trapdoor; Not found
    renderer->addVoxel(glm::fvec3(-1, -1, -8), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(-1, -1, -7), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(-1, -1, -6), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(-1, -1, -5), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(-1, -1, -4), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(-1, -1, -3), 55, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(-1, 0, -9), 58, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(-1, 0, -3), 58, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(-1, 1, -9), 58, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(-1, 1, -3), 58, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(-1, 2, -9), 62, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(-1, 2, -3), 59, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(0, -4, -10), 49, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(0, -4, -9), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(0, -4, -8), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(0, -4, -7), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(0, -4, -6), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(0, -4, -5), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(0, -4, -4), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(0, -4, -3), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(0, -4, -2), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(0, -4, -1), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(0, -4, 0), 55, 0, 0, 162); // minecraft:dirt
    renderer->addVoxel(glm::fvec3(0, -4, 1), 52, 0, 0, 175); // minecraft:bricks
    renderer->addVoxel(glm::fvec3(0, -1, -8), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(0, -1, -7), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(0, -1, -6), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(0, -1, -5), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(0, -1, -4), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(0, -1, -3), 55, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(0, 0, -9), 58, 0, 0, 0); // minecraft:oak_planks
// Skipping minecraft:spruce_door; Not found
    renderer->addVoxel(glm::fvec3(0, 1, -9), 58, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(0, 2, -9), 62, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(0, 2, -3), 59, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(1, -4, -10), 49, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(1, -4, -9), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(1, -4, -8), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(1, -4, -7), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(1, -4, -6), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(1, -4, -5), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(1, -4, -4), 55, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(1, -4, -3), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(1, -4, -2), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(1, -4, -1), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(1, -4, 0), 55, 0, 0, 162); // minecraft:dirt
    renderer->addVoxel(glm::fvec3(1, -4, 1), 52, 0, 0, 175); // minecraft:bricks
    renderer->addVoxel(glm::fvec3(1, -1, -8), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(1, -1, -7), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(1, -1, -6), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(1, -1, -5), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(1, -1, -4), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(1, -1, -3), 55, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(1, 0, -9), 58, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(1, 1, -9), 58, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(1, 2, -9), 62, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(1, 2, -3), 59, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(2, -4, -10), 49, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(2, -4, -9), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(2, -4, -8), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(2, -4, -7), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(2, -4, -6), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(2, -4, -5), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(2, -4, -4), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(2, -4, -3), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(2, -4, -2), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(2, -4, -1), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(2, -4, 0), 55, 0, 0, 175); // minecraft:bricks
    renderer->addVoxel(glm::fvec3(2, -4, 1), 52, 0, 0, 175); // minecraft:bricks
    renderer->addVoxel(glm::fvec3(2, -1, -8), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(2, -1, -7), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(2, -1, -6), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(2, -1, -5), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(2, -1, -4), 53, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(2, -1, -3), 55, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(2, 0, -9), 58, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(2, 0, -3), 58, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(2, 1, -9), 58, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(2, 1, -3), 58, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(2, 2, -9), 62, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(2, 2, -3), 59, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(2, 4, -7), 55, 0, 0, 175); // minecraft:bricks
    renderer->addVoxel(glm::fvec3(2, 5, -7), 10, 0, 0, 175); // minecraft:bricks
// Skipping minecraft:campfire; Not found
    renderer->addVoxel(glm::fvec3(3, -4, -10), 51, 0, 0, 162); // minecraft:dirt
    renderer->addVoxel(glm::fvec3(3, -4, -9), 55, 0, 0, 162); // minecraft:dirt
    renderer->addVoxel(glm::fvec3(3, -4, -8), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(3, -4, -7), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(3, -4, -6), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(3, -4, -5), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(3, -4, -4), 53, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(3, -4, -3), 55, 0, 0, 162); // minecraft:dirt
    renderer->addVoxel(glm::fvec3(3, -4, -2), 55, 0, 0, 162); // minecraft:dirt
    renderer->addVoxel(glm::fvec3(3, -4, -1), 55, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(3, -4, 0), 55, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(3, -4, 1), 54, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(3, -3, -10), 11, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(3, -3, -9), 46, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(3, -3, -3), 43, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(3, -3, -2), 15, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(3, -2, -10), 11, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(3, -2, -9), 46, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(3, -2, -3), 43, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(3, -2, -2), 15, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(3, -1, -10), 11, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(3, -1, -8), 23, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(3, -1, -7), 23, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(3, -1, -6), 23, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(3, -1, -5), 23, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(3, -1, -4), 23, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(3, -1, -2), 30, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(3, 0, -10), 11, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(3, 0, -8), 15, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 0, -7), 15, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 0, -6), 15, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 0, -5), 15, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 0, -4), 15, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 0, -2), 14, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(3, 1, -10), 43, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(3, 1, -8), 15, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 1, -7), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(3, 1, -6), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(3, 1, -5), 15, 0, 0, 58); // minecraft:glass
    renderer->addVoxel(glm::fvec3(3, 1, -4), 15, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 1, -2), 46, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(3, 2, -8), 47, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 2, -7), 47, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 2, -6), 47, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 2, -5), 47, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 2, -4), 47, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 3, -8), 47, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 3, -7), 47, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 3, -6), 47, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 3, -5), 47, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(3, 3, -4), 47, 0, 0, 0); // minecraft:oak_planks
    renderer->addVoxel(glm::fvec3(4, -4, -10), 17, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(4, -4, -9), 23, 0, 0, 162); // minecraft:dirt
    renderer->addVoxel(glm::fvec3(4, -4, -8), 21, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(4, -4, -7), 21, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(4, -4, -6), 21, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(4, -4, -5), 21, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(4, -4, -4), 21, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(4, -4, -3), 23, 0, 0, 162); // minecraft:dirt
    renderer->addVoxel(glm::fvec3(4, -4, -2), 21, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(4, -4, -1), 21, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(4, -4, 0), 21, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(4, -4, 1), 20, 0, 1, 14); // minecraft:grass_block
    renderer->addVoxel(glm::fvec3(4, -3, -9), 26, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(4, -3, -3), 26, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(4, -2, -9), 26, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(4, -2, -3), 26, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(4, -1, -9), 26, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(4, -1, -3), 26, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(4, 0, -9), 26, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(4, 0, -3), 26, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(4, 1, -9), 30, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(4, 1, -3), 27, 0, 1, 4); // minecraft:spruce_log
    renderer->addVoxel(glm::fvec3(4, 2, -8), 23, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(4, 2, -7), 23, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(4, 2, -6), 23, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(4, 2, -5), 23, 1, 1, 1); // minecraft:stripped_oak_log
    renderer->addVoxel(glm::fvec3(4, 2, -4), 23, 1, 1, 1); // minecraft:stripped_oak_log

    renderer->open();
}