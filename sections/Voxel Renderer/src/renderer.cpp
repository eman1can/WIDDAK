//
// Created by Zoe on 11/11/2022.
//

#include <cstdlib>
#include <iostream>

using namespace std;

#include "renderer.h"
#include "input.h"
#include "shape.h"
#include "shader_utils.h"

int Renderer::_init() {
    program = glCreateProgram();
    GLuint vs, fs;
    GLint link_ok = GL_FALSE;

    if ((vs = create_shader("sections/Voxel Renderer/shaders/cube.v.glsl", GL_VERTEX_SHADER)) == 0) {
        fprintf(stderr, "Failed to compile vertex shader.\n");
        return -1;
    }
    if ((fs = create_shader("sections/Voxel Renderer/shaders/cube.f.glsl", GL_FRAGMENT_SHADER)) == 0) {
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

void Renderer::init_buffers() {
    if (shape_stack == nullptr) {
        return;
    }
    _buffers = true;


    GLintptr v_size = 0;
    GLintptr e_size = 0;

    Shape* current = shape_stack;
    while (current != nullptr) {
        v_size += current->vsize();
        e_size += current->esize();
        current = current->next;
    }

    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferData(GL_ARRAY_BUFFER, v_size, nullptr, GL_STATIC_DRAW);

    printf("Allocate VAO of size %td\n", v_size);

    current = shape_stack;
    GLintptr offset = 0;
    while (current != nullptr) {
        printf("Copy data of size %td to VAO at offset %td\n", current->vsize(), offset);
        glBufferSubData(GL_ARRAY_BUFFER, offset, current->vsize(), (void*) current->vertices);
        offset += current->vsize();
        current = current->next;
    }

    glVertexAttribPointer(att_pos, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), (GLvoid*) nullptr);
    glVertexAttribPointer(att_uvs, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), (GLvoid*) (3 * sizeof(GLfloat)));

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, e_size, nullptr, GL_STATIC_DRAW);

    printf("Allocate VAO of size %td\n", e_size);

    offset = 0;
    GLushort ix_offset = 0;
    current = shape_stack;
    while (current != nullptr) {
        if (ix_offset != 0) {
            for (int ix = 0; ix < current->index_count; ix++)
                current->indices[ix] += ix_offset;
        }
        printf("Copy data of size %td to VBO at offset %td\n", current->esize(), offset);
        glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, offset, current->esize(), (void*) current->indices);
        current->ebo_offset = offset;
        offset += current->esize();
        ix_offset += current->vertex_count / 5;
        current = current->next;
    }
}

int Renderer::open() {
    glfwSetFramebufferSizeCallback(_window, Input::onResize);
    glfwSetCursorPosCallback(_window, Input::onMouse);
    glfwSetMouseButtonCallback(_window, Input::onMouseButton);
    glfwSetKeyCallback(_window, Input::onKeyboard);
    glfwSetInputMode(_window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);

    mainLoop(_window);

    destroy();
    glfwTerminate();

    return EXIT_SUCCESS;
}

void Renderer::setSize(int width, int height) {
    glViewport(0, 0, (_width = width), (_height = height));
    render();
}

void Renderer::destroy() {
    glDeleteProgram(program);
    glDeleteBuffers(1, &vbo);
    glDeleteBuffers(1, &ebo);
    // TODO: Cleanup stuff
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

__declspec(dllexport) void renderer_add_voxel(Renderer* renderer, float x, float y, float z, uint8_t relation, uint8_t rotation, uint8_t category, uint32_t index) {
    renderer->addVoxel(glm::fvec3(x, y, z), relation, rotation, category, index);
}

__declspec(dllexport) void renderer_open(Renderer* renderer) {
    renderer->open();
}
}