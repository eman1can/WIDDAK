//
// Created by Zoe on 10/20/2022.
//

#include <cstdlib>
#include <iostream>

#include <SDL.h>

#include "shader_utils.h"

using namespace std;

/**
 * Store all the file's contents in memory, useful to pass shaders
 * source code to OpenGL.  Using SDL_RWops for Android asset support.
 */
char* file_read(const char* filename) {
    SDL_RWops *rw = SDL_RWFromFile(filename, "rb");
    if (rw == nullptr) return nullptr;

    Sint64 res_size = SDL_RWsize(rw);
    char* res = (char*)malloc(res_size + 1);

    Sint64 nb_read_total = 0, nb_read = 1;
    char* buf = res;
    while (nb_read_total < res_size && nb_read != 0) {
        nb_read = SDL_RWread(rw, buf, 1, (res_size - nb_read_total));
        nb_read_total += nb_read;
        buf += nb_read;
    }
    SDL_RWclose(rw);
    if (nb_read_total != res_size) {
        free(res);
        return nullptr;
    }

    res[nb_read_total] = '\0';
    return res;
}

/**
 * Display compilation errors from the OpenGL shader compiler
 */
void print_log(GLuint object) {
    GLint log_length = 0;
    if (glIsShader(object)) {
        glGetShaderiv(object, GL_INFO_LOG_LENGTH, &log_length);
    } else if (glIsProgram(object)) {
        glGetProgramiv(object, GL_INFO_LOG_LENGTH, &log_length);
    } else {
        cerr << "printlog: Not a shader or a program" << endl;
        return;
    }

    char* log = (char*)malloc(log_length);

    if (glIsShader(object))
        glGetShaderInfoLog(object, log_length, nullptr, log);
    else if (glIsProgram(object))
        glGetProgramInfoLog(object, log_length, nullptr, log);
    else
        memset(log, 0, log_length);

    cerr << log;
    free(log);
}

/**
 * Compile the shader from file 'filename', with error handling
 */
GLuint create_shader(const char* filename, GLenum type) {
    const GLchar* source = file_read(filename);
    if (source == nullptr) {
        cerr << "Error opening " << filename << ": " << SDL_GetError() << endl;
        return 0;
    }
    GLuint res = glCreateShader(type);

    glShaderSource(res, 1, &source, nullptr);
    free((void*)source);

    glCompileShader(res);
    GLint compile_ok = GL_FALSE;
    glGetShaderiv(res, GL_COMPILE_STATUS, &compile_ok);
    if (compile_ok == GL_FALSE) {
        cerr << filename << ":";
        print_log(res);
        glDeleteShader(res);
        return 0;
    }

    return res;
}