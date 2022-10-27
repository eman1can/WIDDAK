/**
 * From the OpenGL Programming wikibook: http://en.wikibooks.org/wiki/OpenGL_Programming
 * This file is in the public domain.
 * Contributors: Sylvain Beucler
 */
#include <cstdlib>
#include <iostream>

using namespace std;

#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include <SDL_image.h>

#include "shader_utils.h"
#undef main

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

int screen_width = 800, screen_height = 600;
GLuint vbo_cube_vertices;
GLuint ibo_cube_elements;
GLuint program;
GLint att_coord3d = 0;
GLint att_tex_coord = 1;
GLint uni_mvp, uni_texture;

struct Cube {
    GLfloat* vertices;
    GLushort* indices;
    GLushort index;
    GLuint* textures;
    Cube* next;
};

Cube* root = nullptr;
int cubeCount = 0;

GLuint load_image(const char* path) {

    SDL_Surface* res_texture = IMG_Load(path);
    if (res_texture == nullptr) {
        cerr << "IMG_Load: " << SDL_GetError() << endl;
        return -1;
    }

    GLuint texture_id;
    glGenTextures(1, &texture_id);
    glBindTexture(GL_TEXTURE_2D, texture_id);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexImage2D(GL_TEXTURE_2D, // target
                 0,  // level, 0 = base, no minimap,
                 GL_RGBA, // internalformat
                 res_texture->w,  // width
                 res_texture->h,  // height
                 0,  // border, always 0 in OpenGL ES
                 GL_RGBA,  // format
                 GL_UNSIGNED_BYTE, // type
                 res_texture->pixels);
    SDL_FreeSurface(res_texture);
}

Cube* makeCube() {
    GLfloat vertices[] = {
            // front
            -1.0, -1.0, +1.0, +0.0, +0.0,
            +1.0, -1.0, +1.0, +1.0, +0.0,
            +1.0, +1.0, +1.0, +1.0, +1.0,
            -1.0, +1.0, +1.0, +0.0, +1.0,
            // top
            -1.0, +1.0, +1.0, +0.0, +0.0,
            +1.0, +1.0, +1.0, +1.0, +0.0,
            +1.0, +1.0, -1.0, +1.0, +1.0,
            -1.0, +1.0, -1.0, +0.0, +1.0,
            // back
            +1.0, -1.0, -1.0, +0.0, +0.0,
            -1.0, -1.0, -1.0, +1.0, +0.0,
            -1.0, +1.0, -1.0, +1.0, +1.0,
            +1.0, +1.0, -1.0, +0.0, +1.0,
            // bottom
            -1.0, -1.0, -1.0, +0.0, +0.0,
            +1.0, -1.0, -1.0, +1.0, +0.0,
            +1.0, -1.0, +1.0, +1.0, +1.0,
            -1.0, -1.0, +1.0, +0.0, +1.0,
            // left
            -1.0, -1.0, -1.0, +0.0, +0.0,
            -1.0, -1.0, +1.0, +1.0, +0.0,
            -1.0, +1.0, +1.0, +1.0, +1.0,
            -1.0, +1.0, -1.0, +0.0, +1.0,
            // right
            +1.0, -1.0, +1.0, +0.0, +0.0,
            +1.0, -1.0, -1.0, +1.0, +0.0,
            +1.0, +1.0, -1.0, +1.0, +1.0,
            +1.0, +1.0, +1.0, +0.0, +1.0,
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
            20, 21, 22, 22, 23, 20};

    Cube* cube = (Cube*) malloc(sizeof(Cube));
    cube->vertices = (GLfloat*) malloc(sizeof(vertices));
    cube->indices = (GLushort*) malloc(sizeof(indices));
    cube->next = nullptr;
    cube->index = 0;
    cube->textures = (GLuint*) malloc(sizeof(GLuint) * 1);
    *cube->textures = load_image("res_texture.png");

    printf("%llu\n", sizeof(vertices));
    memcpy(cube->vertices, vertices, sizeof(vertices));
    printf("%llu\n", sizeof(indices));
    memcpy(cube->indices, indices, sizeof(indices));

    return cube;
}

void freeVoxel(Cube* voxel) {
    voxel->next = nullptr;
    free(voxel->vertices);
    free(voxel->indices);
    free(voxel->textures);
    free(voxel);
}

int init_resources() {
    program = glCreateProgram();
    GLuint vs, fs;
    GLint link_ok = GL_FALSE;

    if ((vs = create_shader("cube.v.glsl", GL_VERTEX_SHADER)) == 0) return -1;
    if ((fs = create_shader("cube.f.glsl", GL_FRAGMENT_SHADER)) == 0) return -1;

    glBindAttribLocation(program, 0, "position");
    glBindAttribLocation(program, 1, "tex_coords");

    glAttachShader(program, vs);
    glAttachShader(program, fs);
    glLinkProgram(program);
    glGetProgramiv(program, GL_LINK_STATUS, &link_ok);

    if (link_ok == GL_FALSE) {
        std::cerr << "glLinkProgram: Error Linking";
        print_log(program);
        return -1;
    }

    glUseProgram(program);

    glGenBuffers(1, &vbo_cube_vertices);
    glGenBuffers(1, &ibo_cube_elements);

    const char* uniform_names[] = {"mvp", "tex"};
    GLint* uniforms[] = {&uni_mvp, &uni_texture};

    for (int uni_index = 0; uni_index < sizeof(uniform_names)/sizeof(uniform_names[0]); uni_index++) {
        (*uniforms[uni_index]) = glGetUniformLocation(program, uniform_names[uni_index]);
        if ((*uniforms[uni_index]) == -1) {
            cerr << "Could not bind uniform " << uniform_names[uni_index] << endl;
            return false;
        }
    }



    return true;
}

int init_vertex_buffer() {
    // Loop through cubes
    // For every face, get texture, then copy those triangles to an array
    // Sides: Ft Tp Bk Bt Lt Rt
    // Texture Index Map

    root = makeCube();
    cubeCount = 1;

    glBindBuffer(GL_ARRAY_BUFFER, vbo_cube_vertices);
    glBufferData(GL_ARRAY_BUFFER, 5 * 24 * sizeof(GLfloat), root->vertices, GL_STATIC_DRAW);
    glVertexAttribPointer(att_coord3d, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), (GLvoid*) nullptr);
    glVertexAttribPointer(att_tex_coord, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat),
                          (GLvoid*) (3 * sizeof(GLfloat)));

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo_cube_elements);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 36 * sizeof(GLushort), root->indices, GL_STATIC_DRAW);
    return 0;
}

void logic() {
    float angle = (float) glfwGetTime() * (float) glm::radians(15.0);  // base 15° per second
    glm::mat4 anim = glm::rotate(glm::mat4(1.0f), angle * 3.0f, glm::vec3(0, 1, 0));   // Z axis

    glm::mat4 model = glm::translate(glm::mat4(1.0f), glm::vec3(0.0, 0.0, -4.0));
    glm::mat4 view = glm::lookAt(glm::vec3(0.0, 2.0, 0.0), glm::vec3(0.0, 0.0, -4.0), glm::vec3(0.0, 1.0, 0.0));
    glm::mat4 projection = glm::perspective(45.0f, 1.0f * (float) screen_width / (float) screen_height, 0.1f, 10.0f);

    glm::mat4 mvp = projection * view * model * anim;
    glUniformMatrix4fv(uni_mvp, 1, GL_FALSE, glm::value_ptr(mvp));
}

void render() {
    glActiveTexture(GL_TEXTURE0);
    glUniform1i(uni_texture, /*GL_TEXTURE*/0);
    glBindTexture(GL_TEXTURE_2D, *root->textures);

    glEnableVertexAttribArray(att_coord3d);
    glEnableVertexAttribArray(att_tex_coord);

    glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_SHORT, nullptr);

    glDisableVertexAttribArray(att_coord3d);
    glDisableVertexAttribArray(att_tex_coord);
}

void onResize(int width, int height) {
    screen_width = width;
    screen_height = height;
    glViewport(0, 0, screen_width, screen_height);
}

void free_resources() {
    glDeleteProgram(program);
    glDeleteBuffers(1, &vbo_cube_vertices);
    glDeleteBuffers(1, &ibo_cube_elements);
    freeVoxel(root);
}

void mainLoop(GLFWwindow* window) {
    init_vertex_buffer();

    while (!glfwWindowShouldClose(window)) {
        glClearColor(1.0, 1.0, 1.0, 1.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        glUseProgram(program);
        logic();
        render();

        glfwSwapBuffers(window);

        glfwPollEvents();
    }
}

int main() {
    GLFWwindow* window;
    if (!glfwInit())
        return -1;

    window = glfwCreateWindow(screen_width, screen_height, "Voxel Renderer", nullptr, nullptr);
    if (!window) {
        glfwTerminate();
        cerr << "Error: can't create window" << endl;
        return -1;
    }

    glfwMakeContextCurrent(window);

    if (glewInit() != GLEW_OK)
        return -1;

    std::cout << glGetString(GL_VERSION) << std::endl;

    if (init_resources() < 0)
        return EXIT_FAILURE;

    glEnable(GL_BLEND);
    glEnable(GL_DEPTH_TEST);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    mainLoop(window);

    free_resources();
    glfwTerminate();

    return EXIT_SUCCESS;
}

