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
#include "textures.h"
#undef main

#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

class Shape {
public:
    static Shape* makeCube(float);
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
};

struct VoxelNode {
    glm::fvec3 pos;
    Shape* shape;
    GLuint* tex_ids;
    uint8_t category;
    uint32_t index;
    VoxelNode* next;
};

Shape::Shape() {
    next = nullptr;
    vertices = nullptr;
    indices = nullptr;
    sides = nullptr;
    vertex_count = 0;
    index_count = 0;
    side_count = 0;
}

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

Shape* Shape::makeCube(float edge=1.0) {
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

class Renderer {
public:
    Renderer(int width, int height);

    int init();
    int open();

    void addVoxel(glm::fvec3 pos, uint8_t category, uint32_t index);

    void setSize(int width, int height);

    void onResize(GLFWwindow* window, int width, int height);
    void onMouse(GLFWwindow* window, int button, int action, int mods);
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

    void translate(glm::fvec3);
    void invTranslate(glm::fvec3);
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

    Shape* shape_stack;
    VoxelNode* voxel_stack;
    glm::mat4 mvp;

    void* input;
    GLFWwindow* _window;

    GLuint* _texture_ids;
};

class Input {
public:
    static Input& getInstance(void* renderer) {
        static Input instance; // lazy singleton, instantiated on first use
        if (renderer != nullptr)
            instance.renderer = renderer;
        return instance;
    }

    static void onResize(GLFWwindow* win, int w, int h) { getInstance(nullptr).onResizeImpl(win, w, h); }
    void onResizeImpl(GLFWwindow* win, int w, int h) { ((Renderer*) renderer)->onResize(win, w, h); }

    static void onMouse(GLFWwindow* win, int b, int a, int m) { getInstance(nullptr).onMouseImpl(win, b, a, m); }
    void onMouseImpl(GLFWwindow* win, int b, int a, int m) { ((Renderer*) renderer)->onMouse(win, b, a, m); }

    static void onKeyboard(GLFWwindow* win, int k, int s, int a, int m) { getInstance(nullptr).onKeyboardImpl(win, k, s, a, m); }
    void onKeyboardImpl(GLFWwindow* win, int k, int s, int a, int m) { ((Renderer*) renderer)->onKeyboard(win, k, s, a, m); }

    Input(Input const&) = delete;
    void operator=(Input const&) = delete;
private:
    Input() = default;
    void* renderer;
};

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

int Renderer::_init() {
    program = glCreateProgram();
    GLuint vs, fs;
    GLint link_ok = GL_FALSE;

    if ((vs = create_shader("sections/Voxel Renderer/cube.v.glsl", GL_VERTEX_SHADER)) == 0) {
        fprintf(stderr, "Failed to compile vertex shader.\n");
        return -1;
    }
    if ((fs = create_shader("sections/Voxel Renderer/cube.f.glsl", GL_FRAGMENT_SHADER)) == 0) {
        fprintf(stderr, "Failed to compile fragment shader\n");
        return -1;
    }

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

    glGenBuffers(1, &vbo);
    glGenBuffers(1, &ebo);

    const char* uniform_names[] = {"mvp", "tex"};
    GLint* uniforms[] = {&uni_mvp, &uni_tex};

    for (int uni_index = 0; uni_index < sizeof(uniform_names)/sizeof(uniform_names[0]); uni_index++) {
        (*uniforms[uni_index]) = glGetUniformLocation(program, uniform_names[uni_index]);
        if ((*uniforms[uni_index]) == -1) {
            cerr << "Could not bind uniform " << uniform_names[uni_index] << endl;
            return -1;
        }
    }



    return 0;
}

void Renderer::destroy() {
    glDeleteProgram(program);
    glDeleteBuffers(1, &vbo);
    glDeleteBuffers(1, &ebo);
    // TODO: Cleanup stuff
}

void Renderer::init_buffers() {
    if (shape_stack == nullptr) {
        return;
    }

    GLintptr offset = 0;
    Shape* current;

    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferData(GL_ARRAY_BUFFER, shape_stack->vsize(), 0, GL_STATIC_DRAW);
    glVertexAttribPointer(att_pos, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), (GLvoid*) nullptr);
    glVertexAttribPointer(att_uvs, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), (GLvoid*) (3 * sizeof(GLfloat)));

    current = shape_stack;
    while (current != nullptr) {
        glBufferSubData(GL_ARRAY_BUFFER, offset, shape_stack->vsize(), current->vertices);
        offset += current->vsize();
        current = current->next;
    }

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, shape_stack->esize(), 0, GL_STATIC_DRAW);

    offset = 0;
    current = shape_stack;
    while (current != nullptr) {
        glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, offset, shape_stack->esize(), current->indices);
        offset += current->esize();
        current = current->next;
    }
}

void Renderer::onResize(GLFWwindow* window, int width, int height) {
    setSize(width, height);
}

void Renderer::onMouse(GLFWwindow* window, int button, int action, int mods) {
    printf("%d, %d, %d\n", button, action, mods);
}

void Renderer::onKeyboard(GLFWwindow* window, int keycode, int scancode, int action, int mods) {
    float sensitivity = 0.2;
    if (action == 1 || action == 2) {
        switch (keycode) {
            case 87: // W
                key_translate.z = sensitivity;
                break;
            case 83: // S
                key_translate.z = -sensitivity;
                break;
            case 68: // D
                key_translate.x = -sensitivity;
                break;
            case 65: // A
                key_translate.x = sensitivity;
                break;
            case 32: // Space
                key_translate.y = -sensitivity;
                break;
            case 340: // Shift
                key_translate.y = sensitivity;
                break;
            default:
                printf("Unhandled Keycode: %d, %d, %d, %d\n", keycode, scancode, action, mods);
                break;
        }
    } else {
        switch (keycode) {
            case 87: // W
            if (key_translate.z == sensitivity)
                key_translate.z = 0;
                break;
            case 83: // S
                if (key_translate.z == -sensitivity)
                    key_translate.z = 0;
                break;
            case 68: // D
                if (key_translate.x == -sensitivity)
                    key_translate.x = 0;
                break;
            case 65: // A
                if (key_translate.x == sensitivity)
                    key_translate.x = 0;
                break;
            case 32: // Space
                if (key_translate.y == -sensitivity)
                    key_translate.y = 0;
                break;
            case 340: // Shift
                if (key_translate.y == sensitivity)
                    key_translate.y = 0;
                break;
            default:
                break;
        }
    }

}

void Renderer::setSize(int width, int height) {
    glViewport(0, 0, (_width = width), (_height = height));
    render();
}

void Renderer::logic() {
//    float angle = (float) glfwGetTime() * (float) glm::radians(15.0);  // base 15° per second
//    glm::mat4 anim = glm::rotate(glm::mat4(1.0f), angle * 3.0f, glm::vec3(0, 1, 0));   // Z axis

    mvp *= glm::translate(glm::mat4(1.0f), key_translate);

    glUniformMatrix4fv(uni_mvp, 1, GL_FALSE, glm::value_ptr(mvp));
}

void Renderer::translate(glm::fvec3 pos) {
//    printf("%f, %f, %f\n", pos.x, pos.y, pos.z);
    glm::mat4 model = glm::translate(glm::mat4(1.0f), pos);
    mvp *= model;
    glUniformMatrix4fv(uni_mvp, 1, GL_FALSE, glm::value_ptr(mvp));
}

void Renderer::invTranslate(glm::fvec3 pos) {
    glm::mat4 model = glm::translate(glm::mat4(1.0f), glm::vec3(-pos.x, -pos.y, -pos.z));
    mvp *= model;
    glUniformMatrix4fv(uni_mvp, 1, GL_FALSE, glm::value_ptr(mvp));
}

void Renderer::render() {
    glEnable(GL_BLEND);
    glEnable(GL_DEPTH_TEST);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    glActiveTexture(GL_TEXTURE0);
    glUniform1i(uni_tex, /*GL_TEXTURE*/0);
//    glBindTexture(GL_TEXTURE_2D, *shape_stack->textures());

    glEnableVertexAttribArray(att_pos);
    glEnableVertexAttribArray(att_uvs);

    VoxelNode* current = voxel_stack;
    while (current != nullptr) {
        translate(current->pos);
        uint32_t offset = 0;
        GLuint last = 0;
        for (int i = 0; i < current->shape->side_count; i++) {
            if (last != current->tex_ids[i]) {
                glBindTexture(GL_TEXTURE_2D, current->tex_ids[i]);
                last = current->tex_ids[i];
            }
            glDrawElements(GL_TRIANGLES, current->shape->sides[i], GL_UNSIGNED_SHORT, (void*) (offset * sizeof(GLushort)));
            offset += current->shape->sides[i];
        }

        invTranslate(current->pos);
        current = current->next;
    }

    glDisableVertexAttribArray(att_pos);
    glDisableVertexAttribArray(att_uvs);

    glDisable(GL_BLEND);
    glDisable(GL_DEPTH_TEST);
}

void Renderer::addVoxel(glm::fvec3 pos, uint8_t category, uint32_t index) {
    if (shape_stack == nullptr)
        shape_stack = Shape::makeCube();

    auto node = (VoxelNode*) malloc(sizeof(VoxelNode));
    node->pos = pos;
    node->shape = shape_stack;
    node->next = nullptr;
    if (voxel_stack != nullptr)
        node->next = voxel_stack;
    voxel_stack = node;

    // Load Images
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

    _buffers = false;
}


void Renderer::mainLoop(GLFWwindow* window) {
    // Setup the camera
    glm::mat4 model = glm::translate(glm::mat4(1.0f), glm::vec3(0.0, 0.0, -4.0));
    glm::mat4 view = glm::lookAt(glm::vec3(0.0, 2.0, 0.0), glm::vec3(0.0, 0.0, -4.0), glm::vec3(0.0, 1.0, 0.0));
    glm::mat4 projection = glm::perspective(45.0f, 1.0f * (float) _width / (float) _height, 0.1f, 100.0f);
    mvp = projection * view * model;

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

        glfwSwapBuffers(window);
    }
}

int Renderer::init() {
    if (!glfwInit())
        return -1;

    _window = glfwCreateWindow(_width, _height, "Voxel Renderer", nullptr, nullptr);
    if (!_window) {
        glfwTerminate();
        cerr << "Error: can't create window" << endl;
        return -1;
    }

    glfwMakeContextCurrent(_window);

    if (glewInit() != GLEW_OK) {
        fprintf(stderr, "Failed to init glew!");
        return -1;
    }

    std::cout << glGetString(GL_VERSION) << std::endl;

    if (_init() < 0)
        return EXIT_FAILURE;
    return EXIT_SUCCESS;
}

int Renderer::open() {
    glfwSetFramebufferSizeCallback(_window, Input::onResize);
    glfwSetMouseButtonCallback(_window, Input::onMouse);
    glfwSetKeyCallback(_window, Input::onKeyboard);

    mainLoop(_window);

    destroy();
    glfwTerminate();

    return EXIT_SUCCESS;
}

int main() {
    auto renderer = new Renderer(720, 640);
    if (renderer->init() != 0) {
        fprintf(stderr, "Failed to init renderer\n");
        return 1;
    }

    renderer->open();
}

extern "C" {
    __declspec(dllexport) Renderer* renderer_create(int width, int height) {
        auto renderer = new Renderer(720, 640);
        return renderer;
    }
    __declspec(dllexport) int renderer_init(Renderer* renderer) {
        if (renderer->init() != 0) {
            fprintf(stderr, "Failed to init renderer\n");
            return 1;
        }
        return 0;
    }
    __declspec(dllexport) void renderer_add_voxel(Renderer* renderer, float x, float y, float z, uint8_t category, uint32_t index) {
        renderer->addVoxel(glm::fvec3(x, y, z), category, index);
    }
    __declspec(dllexport) void renderer_open(Renderer* renderer) {
        renderer->open();
    }
}