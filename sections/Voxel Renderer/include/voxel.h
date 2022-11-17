//
// Created by Zoe on 11/11/2022.
//

#ifndef LIBVOXEL_VOXEL_H
#define LIBVOXEL_VOXEL_H

#include <cstdint>
#include <GL/glew.h>
#include <glm/glm.hpp>

#include "shape.h"

/*
 * Rotation:
 * 0 - North
 * 1 - East
 * 2 - South
 * 3 - West
 * 4 - North - Upside Down
 * 5 - East - Upside Down
 * 6 - South - Upside Down
 * 7 - West - Upside Down
 */

struct VoxelNode {
    glm::fvec3 pos;
    Shape* shape;
    GLuint* tex_ids;
    uint8_t category;
    uint32_t index;
    uint8_t relation;
    uint8_t rotation;
    VoxelNode* next;
};

#endif //LIBVOXEL_VOXEL_H
