#version 330 core

layout (location = 0) out vec4 fragColor;

const vec3 cloud_color = vec3(1);

uniform vec3 background_color;

void main(void)
{
    float fog_distance = gl_FragCoord.z / gl_FragCoord.w;
    vec3 color = mix(cloud_color, background_color, 1.0 - exp(-0.000001 * fog_distance * fog_distance));
    fragColor = vec4(color, .8);
}