//
// Created by Zoe on 10/20/2022.
//

#ifndef OPENGL_SHADER_UTILS_H
#define OPENGL_SHADER_UTILS_H

#include <GL/glew.h>

extern char* file_read(const char* filename);
extern void print_log(GLuint object);
extern GLuint create_shader(const char* filename, GLenum type);

#endif //OPENGL_SHADER_UTILS_H
