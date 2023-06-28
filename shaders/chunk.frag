#version 330 core

layout (location = 0) out vec4 fragColor;

const vec3 gamma = vec3(2.2);
const vec3 inv_gamma = 1 / gamma;

uniform sampler2DArray unit_texture_array;
uniform vec3 background_color;
uniform float water_line;

in vec2 uv;
in float shading;
in vec3 fragment_world_position;

flat in int face_id;
flat in int voxel_id;

void main(void)
{
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;
    
    vec3 texture_color = texture(unit_texture_array, vec3(face_uv, voxel_id)).rgb;
    texture_color = pow(texture_color, gamma);
    
    // Shading
    texture_color *= shading;

    // Underwater effect
    if (fragment_world_position.y < water_line)
        texture_color *= vec3(0.0, 0.3, 1.0);
    
    // Fog effect
    float fog_distance = gl_FragCoord.z / gl_FragCoord.w;
    texture_color = mix(texture_color, background_color, (1.0 - exp2(-0.00001 * fog_distance * fog_distance)));
    
    texture_color = pow(texture_color, inv_gamma);
    fragColor = vec4(texture_color, 1.0);
}