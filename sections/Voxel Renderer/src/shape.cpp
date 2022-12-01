//
// Created by Zoe on 11/11/2022.
//

#include "shape.h"

#include <cstring>
#include <cstdlib>

Shape::Shape() {
    next = nullptr;
    vertices = nullptr;
    indices = nullptr;
    sides = nullptr;
    vertex_count = 0;
    index_count = 0;
    side_count = 0;
    ebo_offset = 0;
}

Shape* Shape::makeCube(float edge) {
    float hEdge = edge / 2;
    GLfloat vertices[] = {
            // front
            -hEdge, -hEdge, +hEdge, +0.0, +0.0,
            +hEdge, -hEdge, +hEdge, +1.0, +0.0,
            +hEdge, +hEdge, +hEdge, +1.0, +1.0,
            -hEdge, +hEdge, +hEdge, +0.0, +1.0,
            // top
            -hEdge, +hEdge, +hEdge, +0.0, +0.0,
            +hEdge, +hEdge, +hEdge, +1.0, +0.0,
            +hEdge, +hEdge, -hEdge, +1.0, +1.0,
            -hEdge, +hEdge, -hEdge, +0.0, +1.0,
            // back
            +hEdge, -hEdge, -hEdge, +0.0, +0.0,
            -hEdge, -hEdge, -hEdge, +1.0, +0.0,
            -hEdge, +hEdge, -hEdge, +1.0, +1.0,
            +hEdge, +hEdge, -hEdge, +0.0, +1.0,
            // bottom
            -hEdge, -hEdge, -hEdge, +0.0, +0.0,
            +hEdge, -hEdge, -hEdge, +1.0, +0.0,
            +hEdge, -hEdge, +hEdge, +1.0, +1.0,
            -hEdge, -hEdge, +hEdge, +0.0, +1.0,
            // left
            -hEdge, -hEdge, -hEdge, +0.0, +0.0,
            -hEdge, -hEdge, +hEdge, +1.0, +0.0,
            -hEdge, +hEdge, +hEdge, +1.0, +1.0,
            -hEdge, +hEdge, -hEdge, +0.0, +1.0,
            // right
            +hEdge, -hEdge, +hEdge, +0.0, +0.0,
            +hEdge, -hEdge, -hEdge, +1.0, +0.0,
            +hEdge, +hEdge, -hEdge, +1.0, +1.0,
            +hEdge, +hEdge, +hEdge, +0.0, +1.0,
    };

    GLushort indices[] = {
            // front
            0, 1, 2, 2, 3, 0,
            // top
            4, 5, 6, 6, 7, 4,
            // back
            8, 9, 10, 10, 11, 8,
            // bottom
            12, 13, 14, 14, 15, 12,
            // left
            16, 17, 18, 18, 19, 16,
            // right
            20, 21, 22, 22, 23, 20
    };

    uint8_t sides[] = {6, 6, 6, 6, 6, 6};

    auto cube = new Shape();
    cube->type = CUBE;
    cube->next = nullptr;
    cube->vertices = (GLfloat*) malloc(sizeof(vertices));
    cube->indices = (GLushort*) malloc(sizeof(indices));
    cube->sides = (uint8_t*) malloc(sizeof(sides));

    cube->vertex_count = 24 * 5;
    cube->index_count = 36;
    cube->side_count = 6;

    memcpy(cube->vertices, vertices, sizeof(vertices));
    memcpy(cube->indices, indices, sizeof(indices));
    memcpy(cube->sides, sides, sizeof(sides));

    return cube;
}

Shape* Shape::makeStair(float edge) {
    float hEdge = edge / 2;
    GLfloat vertices[] = {
            // front
            -hEdge, -hEdge, +hEdge, +0.0, +0.0,
            +hEdge, -hEdge, +hEdge, +1.0, +0.0,
            +hEdge, +0.0,   +hEdge, +1.0, +0.5,
            -hEdge, +0.0,   +hEdge, +0.0, +0.5,
            +hEdge, +0.0,   +0.0,   +1.0, +0.5,
            -hEdge, +0.0,   +0.0,   +0.0, +0.5,
            -hEdge, +hEdge, +0.0,   +0.0, +1.0,
            +hEdge, +hEdge, +0.0,   +1.0, +1.0,
            // top
            +hEdge, +hEdge, -hEdge, +1.0, +0.0,
            -hEdge, +hEdge, -hEdge, +0.0, +0.0,
            -hEdge, +hEdge, +0.0,   +0.0, +0.5,
            +hEdge, +hEdge, +0.0,   +1.0, +0.5,
            -hEdge, +0.0,   +0.0,   +0.0, +0.5,
            +hEdge, +0.0,   +0.0,   +1.0, +0.5,
            +hEdge, +0.0,   +hEdge, +1.0, +1.0,
            -hEdge, +0.0,   +hEdge, +0.0, +1.0,
            // back
            +hEdge, -hEdge, -hEdge, +0.0, +0.0,
            -hEdge, -hEdge, -hEdge, +1.0, +0.0,
            -hEdge, +hEdge, -hEdge, +1.0, +1.0,
            +hEdge, +hEdge, -hEdge, +0.0, +1.0,
            // bottom
            -hEdge, -hEdge, -hEdge, +0.0, +0.0,
            +hEdge, -hEdge, -hEdge, +1.0, +0.0,
            +hEdge, -hEdge, +hEdge, +1.0, +1.0,
            -hEdge, -hEdge, +hEdge, +0.0, +1.0,
            // left
            -hEdge, -hEdge, -hEdge, +0.0, +0.0,
            -hEdge, -hEdge, +hEdge, +1.0, +0.0,
            -hEdge, +0.0,   +hEdge, +1.0, +0.5,
            -hEdge, +0.0,   -hEdge, +0.0, +0.5,
            -hEdge, +0.0,   +0.0,   +0.5, +0.5,
            -hEdge, +hEdge, -hEdge, +0.0, +1.0,
            -hEdge, +hEdge, +0.0,   +0.5, +1.0,
            // right
            +hEdge, -hEdge, +hEdge, +0.0, +0.0,
            +hEdge, -hEdge, -hEdge, +1.0, +0.0,
            +hEdge, +0.0,   -hEdge, +1.0, +0.5,
            +hEdge, +0.0,   +hEdge, +0.0, +0.5,
            +hEdge, +0.0,   +0.0,   +0.5, +0.5,
            +hEdge, +hEdge, +0.0,   +0.5, +1.0,
            +hEdge, +hEdge, -hEdge, +1.0, +1.0,
    };

    GLushort indices[] = {
            // front
            0, 1, 2, 2, 3, 0, 4, 5, 6, 6, 7, 4,
            // top
            8, 9, 10, 10, 11, 8, 12, 13, 14, 14, 15, 12,
            // back
            16, 17, 18, 18, 19, 16,
            // bottom
            20, 21, 22, 22, 23, 20,
            // left
            24, 25, 26, 26, 27, 24, 27, 28, 29, 29, 30, 28,
            // right
            31, 32, 33, 33, 34, 31, 33, 35, 36, 36, 37, 33
    };

    uint8_t sides[] = {12, 12, 6, 6, 12, 12};

    auto stair = new Shape();
    stair->type = STAIR;
    stair->next = nullptr;
    stair->vertices = (GLfloat*) malloc(sizeof(vertices));
    stair->indices = (GLushort*) malloc(sizeof(indices));
    stair->sides = (uint8_t*) malloc(sizeof(sides));

    stair->vertex_count = 38 * 5;
    stair->index_count = 60;
    stair->side_count = 6;

    memcpy(stair->vertices, vertices, sizeof(vertices));
    memcpy(stair->indices, indices, sizeof(indices));
    memcpy(stair->sides, sides, sizeof(sides));

    return stair;
}