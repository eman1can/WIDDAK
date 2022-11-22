//
// Created by Zoe on 11/11/2022.
//

#include <SDL_image.h>
#include <iostream>

#include "renderer.h"
#include "shape.h"
#include "textures.h"
#include "input.h"

using namespace std;

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

    int format = GL_RGBA;
    if (res_texture->format->format == SDL_PIXELFORMAT_RGB24)
        format = GL_RGB;
    glTexImage2D(GL_TEXTURE_2D, // target
                 0,  // level, 0 = base, no minimap,
                 GL_RGBA, // internalformat
                 res_texture->w,  // width
                 res_texture->h,  // height
                 0,  // border, always 0 in OpenGL ES
                 format,  // format
                 GL_UNSIGNED_BYTE, // type
                 res_texture->pixels);
    SDL_FreeSurface(res_texture);
    return texture_id;
}

Renderer::Renderer(int width, int height) {
    _width = width;
    _height = height;

    vbo = -1;
    ebo = -1;
    program = -1;

    att_pos = 0;
    att_uvs = 1;
    uni_mvp = -1;
    uni_tex = -1;

    key_translate = glm::fvec3(0, 0, 0);
    camera_pos = glm::fvec3(0, 0, 3);
    camera_front = glm::fvec3(0, 0, -1);
    camera_up = glm::fvec3(0, 1, 0);

    camera_speed = 0.02;
    camera_sensitivity = 1.0;

    _last_x = (float) width / 2;
    _last_y = (float) height / 2;

    yaw = -90;
    pitch = 0;
    fov = 60;

    first_mouse = true;
    _locked = true;

    shape_stack = nullptr;
    voxel_stack = nullptr;
    mvp = glm::mat4(1.0f);

    _buffers = false;

    input = (void*) &Input::getInstance(this);
    _window = nullptr;

    size_t asset_count = sizeof(TEXTURE_ASSETS) / sizeof(const char*);
    printf("%llu\n", asset_count);
    _texture_ids = (GLuint*) calloc(asset_count, sizeof(GLuint));
}

void Renderer::logic() {
    if (key_translate.z != 0)
        camera_pos += key_translate.z * camera_speed * camera_front;
    if (key_translate.x != 0)
        camera_pos += key_translate.x * camera_speed * glm::normalize(glm::cross(camera_front, camera_up));
    if (key_translate.y != 0)
        camera_pos += key_translate.y * camera_speed * camera_up;
    updateProjection();
    applyMVP();
}

void Renderer::updateProjection() {
    glm::mat4 view = glm::lookAt(camera_pos, camera_pos + camera_front, camera_up);
    glm::mat4 projection = glm::perspective(glm::radians(fov), (float) _width / (float) _height, 0.1f, 100.0f);
    mvp = projection * view;
}

void Renderer::updateOrthographic() {
    glm::mat4 view = glm::lookAt(glm::vec3(0,0,1), glm::vec3(0,0,0), glm::vec3(0,1,0));
    glm::mat4 projection = glm::ortho(0, _width, 0, _height);
    mvp = projection * view;
}

void Renderer::applyMVP() {
    glUniformMatrix4fv(uni_mvp, 1, GL_FALSE, glm::value_ptr(mvp));
}

void Renderer::translate(glm::fvec3 pos) {
    mvp *= glm::translate(glm::mat4(1.0f), pos);
}

void Renderer::invTranslate(glm::fvec3 pos) {
    mvp *= glm::translate(glm::mat4(1.0f), glm::vec3(-pos.x, -pos.y, -pos.z));
}

/*
 * 0  - No Rotation
 * 1  - Rotate 90°  on axis X
 * 2  - Rotate 90°  on axis Y
 * 3  - Rotate 180° on axis X
 * 4  - Rotate 180° on axis Y
 * 5  - Rotate -90° on axis X
 * 6  - Rotate -90° on axis Y
 * 7  - Rotate 90°  on axis X & 180° on axis Y
 * 8  - Rotate 90°  on axis Y & 180° on axis X
 * 9  - Rotate 180° on axis X & 180° on axis Y
 * 10 - Rotate 180° on axis Y & 90° on axis X
 * 11 - Rotate -90° on axis X & 180° on axis Y
 * 12 - Rotate -90° on axis Y & 180° on axis X
 */
void Renderer::rotate(uint8_t rotation) {
    if (rotation == 0)
        return;
    glm::mat4 rot;
    switch (rotation) {
        case 1:
            rot = glm::mat4(1, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 1);
            break;
        case 2:
            rot = glm::mat4(0, 0, 1, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 1);
            break;
        case 4:
            rot = glm::mat4(-1, 0, 0, 0, 0, 1, 0, 0,  0, 0, -1, 0, 0, 0, 0, 1);
            break;
        case 5:
            rot = glm::mat4(1, 0, 0, 0, 0, -1, -1, 0, 0, 1, 0, -1, 0, 0, 0, 1);
            break;
        case 6:
            rot = glm::mat4(0, 0, -1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1);
            break;
        case 8:
            rot = glm::mat4(0, 0, -1, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 1);
            break;
        case 10:
            rot = glm::mat4(-1, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 1);
            break;
        default:
            printf("Rotation %d unhandled\n", rotation);
            return;
    }
    mvp *= rot;
}

void Renderer::invRotate(uint8_t rotation) {
    if (rotation == 0)
        return;
    glm::mat4 rot;
    switch (rotation) {
        case 1:
            rot = glm::mat4(1, 0, 0, 0, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 1);
            break;
        case 2:
            rot = glm::mat4(0, 0, -1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1);
            break;
        case 4:
            rot = glm::mat4(-1, 0, 0, 0, 0, 1, 0, 0,  0, 0, -1, 0, 0, 0, 0, 1);
            break;
        case 5:
            rot = glm::mat4(1, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 1);
            break;
        case 6:
            rot = glm::mat4(0, 0, 1, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 0, 1);
            break;
        case 8:
            rot = glm::mat4(
                    0, 0, -1, 0,
                    0, -1, 0, 0,
                    -1, 0, 0, 0,
                    0, 0, 0, 1);
            break;
        case 10:
            rot = glm::mat4(-1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1);
            break;
        default:
            return;
    }
    mvp *= rot;
}

void Renderer::render() {
    glEnable(GL_BLEND);
    glEnable(GL_DEPTH_TEST);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    glActiveTexture(GL_TEXTURE0);
    glUniform1i(uni_tex, /*GL_TEXTURE*/0);

    glEnableVertexAttribArray(att_pos);
    glEnableVertexAttribArray(att_uvs);

    VoxelNode* current = voxel_stack;
    while (current != nullptr) {
        translate(current->pos);
        rotate(current->rotation);
        applyMVP();
        uint32_t offset = current->shape->ebo_offset;
        GLuint last = 0;

        uint8_t mask = 1;
        for (int i = 0; i < current->shape->side_count; i++) {
//            if ((mask & current->relation) > 0) {
//                mask = mask << 1;
//                continue;
//            }
            if (last != current->tex_ids[i]) {
                glBindTexture(GL_TEXTURE_2D, current->tex_ids[i]);
                last = current->tex_ids[i];
            }
            glDrawElements(GL_TRIANGLES, current->shape->sides[i], GL_UNSIGNED_SHORT, (void*) offset);
            offset += current->shape->sides[i] * sizeof(GLushort);
            mask = mask << 1;
        }

        invRotate(current->rotation);
        invTranslate(current->pos);
        current = current->next;
    }

    glDisableVertexAttribArray(att_pos);
    glDisableVertexAttribArray(att_uvs);

    glDisable(GL_BLEND);
    glDisable(GL_DEPTH_TEST);
}

void Renderer::renderFPS() {

}

void Renderer::addVoxel(glm::fvec3 pos, uint8_t relation, uint8_t rotation, uint8_t category, uint32_t index) {
    auto node = (VoxelNode*) malloc(sizeof(VoxelNode));
    node->pos = pos;
    node->next = nullptr;
    node->relation = relation;
    node->rotation = rotation;
    if (voxel_stack != nullptr)
        node->next = voxel_stack;
    voxel_stack = node;

    uint8_t type = CUBE;

    if (category == STAIRS) {
        StairTexture tex = STAIR_TEXTURES[index];
        category = tex.category;
        index = tex.index;
        type = STAIR;
    }

    if (category == SIMPLE) {
        uint16_t image_index = SIMPLE_TEXTURE_IMAGES[index];
        node->tex_ids = (GLuint*) malloc(6 * sizeof(GLuint));
        if (_texture_ids[image_index] == 0) {
            const char* asset_path = TEXTURE_ASSETS[image_index];
            _texture_ids[image_index] = load_image(asset_path);
            printf("Loaded asset %d (%s) into %u\n", image_index, asset_path, _texture_ids[image_index]);
        }
        for (int ix = 0; ix < 6; ix++)
            node->tex_ids[ix] = _texture_ids[image_index];
    } else if (category == MULTI_TEXTURE) {
        MultiTexture tex = MULTI_TEXTURES[index];
        node->tex_ids = (GLuint*) malloc(6 * sizeof(GLuint));
        for (int ix = 0; ix < 6; ix++) {
            uint16_t image_index = tex.textures[tex.texture_ids[ix]];
            if (_texture_ids[image_index] == 0) {
                const char* asset_path = TEXTURE_ASSETS[image_index];
                _texture_ids[image_index] = load_image(asset_path);
                printf("Loaded asset %d (%s) into %u\n", image_index, asset_path, _texture_ids[image_index]);
            }
            node->tex_ids[ix] = _texture_ids[image_index];
        }
    }

    Shape* current = shape_stack;
    while (current != nullptr) {
        if (current->type == type) {
            node->shape = current;
            return;
        }
        current = current->next;
    }

    Shape* shape;
    switch (type) {
        case STAIR:
            shape = Shape::makeStair();
            break;
        case CUBE:
            shape = Shape::makeCube();
            break;
    }

    shape->next = shape_stack;
    shape_stack = shape;
    node->shape = shape;
}

void Renderer::mainLoop(GLFWwindow* window) {
    // Setup the camera
    updateProjection();

    while (!glfwWindowShouldClose(window)) {
        glUseProgram(program);

        glClearColor(1.0, 1.0, 1.0, 1.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        if (!_buffers)
            init_buffers();

        glfwPollEvents();

        if (shape_stack != nullptr) {
            logic();
            render();
        }

        // TODO: FPS
        updateOrthographic();
        applyMVP();
        renderFPS();

        glfwSwapBuffers(window);
    }
}