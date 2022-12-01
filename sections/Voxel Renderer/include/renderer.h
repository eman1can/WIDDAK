//
// Created by Zoe on 11/11/2022.
//

#ifndef LIBVOXEL_RENDERER_H
#define LIBVOXEL_RENDERER_H

#include <GL/glew.h>
#include <GLFW/glfw3.h>

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

#include "voxel.h"

class Renderer {
public:
    Renderer(int width, int height);

    int init();
    int open();

    void addVoxel(glm::fvec3 pos, uint8_t relation, uint8_t rotation, uint8_t category, uint32_t index);

    void setSize(int width, int height);

    void onResize(GLFWwindow* window, int width, int height);
    void onMouseButton(GLFWwindow* window, int button, int action, int mods);
    void onMouse(GLFWwindow*, float x, float y);
    void onKeyboard(GLFWwindow* window, int keycode, int scancode, int action, int mods);
private:
    int _init();
    void mainLoop(GLFWwindow* window);
    void destroy();

    // Core Functions
    void init_buffers();
    void render();
    void renderFPS();
    void logic();

    void updateProjection();
    void updateOrthographic();

    void applyMVP();
    void translate(glm::fvec3);
    void rotate(uint8_t rotation);
    void invTranslate(glm::fvec3);
    void invRotate(uint8_t rotation);
public:
private:
    int _width;
    int _height;

    bool _buffers;

    GLuint vbo;
    GLuint ebo;
    GLuint program;

    GLint att_pos;
    GLint att_uvs;
    GLint uni_mvp;
    GLint uni_tex;

    glm::fvec3 key_translate;
    glm::fvec3 camera_pos;
    glm::fvec3 camera_front;
    glm::fvec3 camera_up;

    bool first_mouse;
    bool _locked;

    float _last_x;
    float _last_y;

    float fov;
    float yaw;
    float pitch;

    float camera_speed;
    float camera_sensitivity;

    Shape* shape_stack;
    VoxelNode* voxel_stack;
    glm::mat4 mvp;

    void* input;
    GLFWwindow* _window;

    GLuint* _texture_ids;
};

#endif //LIBVOXEL_RENDERER_H
