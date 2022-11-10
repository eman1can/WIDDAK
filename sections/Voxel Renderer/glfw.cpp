//
// Created by Zoe on 10/25/2022.
//

#include <iostream>

#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include "shader_utils.h"

static const int width = 1920;
static const int height = 1080;

struct Cube {
    GLfloat* vertices;
    GLushort* indices;
    GLushort index;
    Cube* next;
};

Cube* makeCube() {
    GLfloat vertices[] = {
            // front
            -1.0, -1.0, +1.0, +0.0, +0.0, 0.0, 0.0, 0.0, 1.0, +1.0, -1.0, +1.0, +1.0, +0.0, 0.0, 0.0, 0.0, 1.0, +1.0,
            +1.0, +1.0, +1.0, +1.0, 0.0, 0.0, 0.0, 1.0, -1.0, +1.0, +1.0, +0.0, +1.0, 0.0, 0.0, 0.0, 1.0,
            // top
            -1.0, +1.0, +1.0, +0.0, +0.0, 0.0, 0.0, 0.0, 1.0, +1.0, +1.0, +1.0, +1.0, +0.0, 0.0, 0.0, 0.0, 1.0, +1.0,
            +1.0, -1.0, +1.0, +1.0, 0.0, 0.0, 0.0, 1.0, -1.0, +1.0, -1.0, +0.0, +1.0, 0.0, 0.0, 0.0, 1.0,
            // back
            +1.0, -1.0, -1.0, +0.0, +0.0, 0.0, 0.0, 0.0, 1.0, -1.0, -1.0, -1.0, +1.0, +0.0, 0.0, 0.0, 0.0, 1.0, -1.0,
            +1.0, -1.0, +1.0, +1.0, 0.0, 0.0, 0.0, 1.0, +1.0, +1.0, -1.0, +0.0, +1.0, 0.0, 0.0, 0.0, 1.0,
            // bottom
            -1.0, -1.0, -1.0, +0.0, +0.0, 0.0, 0.0, 0.0, 1.0, +1.0, -1.0, -1.0, +1.0, +0.0, 0.0, 0.0, 0.0, 1.0, +1.0,
            -1.0, +1.0, +1.0, +1.0, 0.0, 0.0, 0.0, 1.0, -1.0, -1.0, +1.0, +0.0, +1.0, 0.0, 0.0, 0.0, 1.0,
            // left
            -1.0, -1.0, -1.0, +0.0, +0.0, 0.0, 0.0, 0.0, 1.0, -1.0, -1.0, +1.0, +1.0, +0.0, 0.0, 0.0, 0.0, 1.0, -1.0,
            +1.0, +1.0, +1.0, +1.0, 0.0, 0.0, 0.0, 1.0, -1.0, +1.0, -1.0, +0.0, +1.0, 0.0, 0.0, 0.0, 1.0,
            // right
            +1.0, -1.0, +1.0, +0.0, +0.0, 0.0, 0.0, 0.0, 1.0, +1.0, -1.0, -1.0, +1.0, +0.0, 0.0, 0.0, 0.0, 1.0, +1.0,
            +1.0, -1.0, +1.0, +1.0, 0.0, 0.0, 0.0, 1.0, +1.0, +1.0, +1.0, +0.0, +1.0, 0.0, 0.0, 0.0, 1.0,};

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
            20, 21, 22, 22, 23, 20};

    Cube* cube = (Cube*) malloc(sizeof(Cube));
    cube->vertices = (GLfloat*) malloc(sizeof(vertices));
    cube->indices = (GLushort*) malloc(sizeof(indices));
    cube->next = nullptr;
    cube->index = 0;

    printf("%llu", sizeof(vertices));
    memcpy(cube->vertices, vertices, sizeof(vertices));
    printf("%llu", sizeof(indices));
    memcpy(cube->indices, indices, sizeof(indices));

    return cube;
}

int main() {
    GLFWwindow* window;

    if (!glfwInit())
        return -1;

    window = glfwCreateWindow(width, height, "Voxel Renderer", nullptr, nullptr);
    if (!window) {
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);

    if (glewInit() != GLEW_OK)
        return -1;

    std::cout << glGetString(GL_VERSION) << std::endl;

    // Do Resource Setup Here
//    GLuint program = glCreateProgram();
//    GLuint vs, fs;
//    GLint link_ok = GL_FALSE;
//
//    if ((vs = create_shader("cube.v.glsl", GL_VERTEX_SHADER)) == 0) return -1;
//    if ((fs = create_shader("cube.f.glsl", GL_FRAGMENT_SHADER)) == 0) return -1;
//
//    glBindAttribLocation(program, 0, "position");
//    glBindAttribLocation(program, 1, "tex_coords");
//
//    glAttachShader(program, vs);
//    glAttachShader(program, fs);
//    glGetProgramiv(program, GL_LINK_STATUS, &link_ok);

//    if (link_ok != GLEW_OK) {
//        std::cerr << "glLinkProgram: Error Linking";
//        return -1;
//    }

    float positions[6] = {
            -0.5, -0.5,
            0.0, 0.5,
            0.5, -0.5
    };

    unsigned int buffer;
    glGenBuffers(1, &buffer);
    glBindBuffer(GL_ARRAY_BUFFER, buffer);
    glBufferData(GL_ARRAY_BUFFER, 6 * sizeof(float), positions, GL_STATIC_DRAW);

    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, sizeof(float) * 2, (void*) nullptr);

    glBindBuffer(GL_ARRAY_BUFFER, 0);
    //glEnableVertexArrayAttrib(0);

    // Do Rendering Here
    while (!glfwWindowShouldClose(window)) {
        glClear(GL_COLOR_BUFFER_BIT);

        //glDrawElements(GL_TRIANGLES, 1, GL_FLOAT, 0);

        glfwSwapBuffers(window);

        glfwPollEvents();
    }

    glfwTerminate();
    return 0;
}