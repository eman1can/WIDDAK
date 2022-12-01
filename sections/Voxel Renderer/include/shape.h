//
// Created by Zoe on 11/11/2022.
//

#ifndef LIBVOXEL_SHAPE_H
#define LIBVOXEL_SHAPE_H

#include <cstdint>
#include <GL/glew.h>

enum SHAPE_TYPE : uint8_t {
    CUBE,
    SLAB,
    STAIR
};

class Shape {
public:
    static Shape* makeCube(float w=1.0, float h=1.0, float l=1.0);
    static Shape* makeSlab(float edge=1.0);

    GLintptr vsize() const { return vertex_count * sizeof(GLfloat); }
    GLintptr esize() const { return index_count * sizeof(GLushort); }
private:
    Shape();
public:
    Shape* next;
    GLfloat* vertices;
    GLushort* indices;
    uint8_t* sides;
    uint16_t vertex_count;
    uint16_t index_count;
    uint8_t side_count;
    uint8_t type;
    uint32_t ebo_offset;
    uint32_t vbo_offset;
};


#endif //LIBVOXEL_SHAPE_H
