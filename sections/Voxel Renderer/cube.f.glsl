#version 330 core

out vec4 frag_color;

in vec2 f_tex_coords;

uniform sampler2D tex;

void main(void) {
  vec2 flip_tex_coords = vec2(f_tex_coords.x, 1.0 - f_tex_coords.y);
  vec4 color = texture2D(tex, flip_tex_coords);
  if (color.a < 0.1)
    discard;
  frag_color = color;
}
