#version 330 core

layout (location = 0) in vec3 in_position;

uniform mat4 matrix_projection;
uniform mat4 matrix_view;
uniform mat4 matrix_view_projection;
uniform int center;
uniform float unit_time;
uniform float cloud_scale;

void main(void)
{
    vec3 position = vec3(in_position);
    position.xz -= center;
    position.xz *= cloud_scale;
    position.xz += center;

    float time = 300 * sin(0.01 * unit_time);
    position.xz += time;
    
    gl_Position = matrix_projection * matrix_view * vec4(position, 1.0);
}