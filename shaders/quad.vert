#version 330 core

layout (location = 0) in vec3 in_position;
layout (location = 1) in vec3 in_color;

uniform mat4 matrix_projection;
uniform mat4 matrix_view;
uniform mat4 matrix_model;

out vec3 color;

void main(void)
{
    color = in_color;
    gl_Position = matrix_projection * matrix_view * matrix_model * vec4(in_position, 1.0);
}