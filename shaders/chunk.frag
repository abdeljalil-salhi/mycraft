#version 330 core

layout (location = 0) out vec4 fragColor;

const vec3 gamma = vec3(2.2);
const vec3 invGamma = 1 / gamma;

uniform sampler2DArray unit_texture_array;

in vec3 voxel_color;
in vec2 uv;
in float shading;

flat in int face_id;
flat in int voxel_id;

void main(void)
{
    vec2 face_uv = uv;
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

    vec3 texture_color = texture(unit_texture_array, vec3(face_uv, voxel_id)).rgb;
    texture_color = pow(texture_color, gamma);
    // texture_color *= voxel_color;
    texture_color *= shading;
    texture_color = pow(texture_color, invGamma);
    
    fragColor = vec4(texture_color, 1.0);
}