#version 330 core

layout(location=0) in vec3 position;
layout(location=1) in vec2 tex_coords;

out vec2 f_tex_coords;

uniform mat4 mvp;

void main(void) {
  gl_Position = vec4(0.0, 0.0, 0.0, 1.0);
  gl_Position = mvp * vec4(position, 1.0);
  f_tex_coords = tex_coords;
}