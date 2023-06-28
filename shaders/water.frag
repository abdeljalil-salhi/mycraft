#version 330 core

layout (location = 0) out vec4 fragColor;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

in vec2 uv;

uniform sampler2D unit_texture;
uniform float water_line;

void main(void)
{
    vec3 texture_color = texture(unit_texture, uv).rgb;
    texture_color = pow(texture_color, gamma);

    // Water fog effect
    float fog_distance = gl_FragCoord.z / gl_FragCoord.w;
    float alpha = mix(0.5, 0.0, 1.0 - exp(-0.000002 * fog_distance * fog_distance));

    texture_color = pow(texture_color, inv_gamma);
    fragColor = vec4(texture_color, alpha);
}