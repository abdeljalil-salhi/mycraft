#version 330 core

layout (location = 0) out vec4 fragColor;

const vec3 gamma = vec3(2.2);
const vec3 invGamma = 1 / gamma;

uniform sampler2D unit_texture_0;

in vec3 voxel_color;
in vec2 uv;

void main(void)
{
    vec3 texture_color = texture(unit_texture_0, uv).rgb;
    texture_color = pow(texture_color, gamma);
    texture_color.rgb *= voxel_color;
    texture_color = pow(texture_color, invGamma);
    fragColor = vec4(texture_color, 1.0);
}