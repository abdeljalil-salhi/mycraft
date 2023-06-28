#version 330 core

layout (location = 0) in vec2 in_texture_coords;
layout (location = 1) in vec3 in_position;

uniform mat4 matrix_projection;
uniform mat4 matrix_view;
uniform mat4 matrix_view_projection;
uniform int water_area;
uniform float water_line;

out vec2 uv;

void main(void)
{
    vec3 position = in_position;
    position.xz *= water_area;
    position.xz -= 0.33 * water_area;
    position.y += water_line;
    uv = in_texture_coords * water_area;
    gl_Position = matrix_projection * matrix_view * vec4(position, 1.0);
}