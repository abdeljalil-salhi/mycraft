#version 330 core

layout (location = 0) out vec4 fragColor;

in vec3 voxel_color;

void main(void)
{
    fragColor = vec4(voxel_color, 1.0);
}