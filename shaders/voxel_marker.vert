#version 330 core

layout (location = 0) in vec2 in_texture_coords;
layout (location = 1) in vec3 in_position;

uniform mat4 matrix_projection;
uniform mat4 matrix_view;
uniform mat4 matrix_model;
uniform uint mode_id;

const vec3 marker_colors[2] = vec3[2](vec3(1, 0, 0), vec3(0, 0, 1));

out vec3 marker_color;
out vec2 uv;

void main(void)
{
    uv = in_texture_coords;
    marker_color = marker_colors[mode_id];
    
    gl_Position = matrix_projection * matrix_view * matrix_model * vec4((in_position - 0.5) * 1.01 + 0.5, 1.0);
}