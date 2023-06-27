#version 330 core

layout (location = 0) out vec4 fragColor;

in vec3 color;

void main(void)
{
    fragColor = vec4(color, 1.0);
}