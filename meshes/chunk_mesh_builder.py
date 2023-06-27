from numba import njit, uint8
from numpy import ndarray, empty
from glm import vec3

from settings import CHUNK_VOLUME, CHUNK_SIZE, CHUNK_AREA, WORLD_WIDTH, WORLD_HEIGHT, WORLD_DEPTH, WORLD_AREA

@njit
def to_uint8(x, y, z, voxel_id, face_id) -> tuple:
    return uint8(x), uint8(y), uint8(z), uint8(voxel_id), uint8(face_id)

@njit
def get_chunk_index(world_voxel_pos: vec3) -> int:
    wx, wy, wz = world_voxel_pos
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE
    if not (0 <= cx < WORLD_WIDTH and 0 <= cy < WORLD_HEIGHT and 0 <= cz < WORLD_DEPTH):
        return -1
    return cx + WORLD_WIDTH * cz + WORLD_AREA * cy

@njit
def is_void(local_voxel_pos: vec3, world_voxel_pos: vec3, world_voxels: ndarray) -> bool:
    chunk_index = get_chunk_index(world_voxel_pos)
    if chunk_index == -1:
        return False
    
    chunk_voxels = world_voxels[chunk_index]
    x, y, z = local_voxel_pos
    
    return not chunk_voxels[x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA]

@njit
def add_data(vertex_data: ndarray, index: int, *vertices: tuple) -> int:
    for vertex in vertices:
        for value in vertex:
            vertex_data[index] = value
            index += 1
    return index

@njit
def build_chunk_mesh(chunk_voxels: ndarray, format_size: int, chunk_position: tuple, world_voxels: ndarray) -> ndarray:
    # Well, here; the maximum number of visible faces is 3
    # and each face is built from 2 triangles with 3 vertices each
    # so 3 * 2 * 3 = 18 vertices per voxel
    vertex_data = empty(CHUNK_VOLUME * 18 * format_size, dtype='uint8')
    index = 0
    
    for x in range(CHUNK_SIZE):
        for y in range (CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                if not voxel_id:
                    continue
                
                # Get the voxel position in the world
                cx, cy, cz = chunk_position
                wx = cx * CHUNK_SIZE + x
                wy = cy * CHUNK_SIZE + y
                wz = cz * CHUNK_SIZE + z
                
                # Top face
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
                    # format: x, y, z, voxel_id, face_id
                    v0 = to_uint8(x    , y + 1, z    , voxel_id, 0)
                    v1 = to_uint8(x + 1, y + 1, z    , voxel_id, 0)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 0)
                    v3 = to_uint8(x    , y + 1, z + 1, voxel_id, 0)
                    
                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)
                
                # Bottom face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    v0 = to_uint8(x    , y    , z    , voxel_id, 1)
                    v1 = to_uint8(x + 1, y    , z    , voxel_id, 1)
                    v2 = to_uint8(x + 1, y    , z + 1, voxel_id, 1)
                    v3 = to_uint8(x    , y    , z + 1, voxel_id, 1)
                    
                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)
                
                # Right face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    v0 = to_uint8(x + 1, y    , z    , voxel_id, 2)
                    v1 = to_uint8(x + 1, y + 1, z    , voxel_id, 2)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 2)
                    v3 = to_uint8(x + 1, y    , z + 1, voxel_id, 2)
                    
                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                
                # Left face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    v1 = to_uint8(x    , y + 1, z    , voxel_id, 3)
                    v0 = to_uint8(x    , y    , z    , voxel_id, 3)
                    v2 = to_uint8(x    , y + 1, z + 1, voxel_id, 3)
                    v3 = to_uint8(x    , y    , z + 1, voxel_id, 3)
                    
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)
                
                # Back face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    v0 = to_uint8(x    , y    , z    , voxel_id, 4)
                    v1 = to_uint8(x    , y + 1, z    , voxel_id, 4)
                    v2 = to_uint8(x + 1, y + 1, z    , voxel_id, 4)
                    v3 = to_uint8(x + 1, y    , z    , voxel_id, 4)
                    
                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                
                # Front face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    v0 = to_uint8(x    , y    , z + 1, voxel_id, 5)
                    v1 = to_uint8(x    , y + 1, z + 1, voxel_id, 5)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 5)
                    v3 = to_uint8(x + 1, y    , z + 1, voxel_id, 5)
                    
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)
    
    return vertex_data[:index + 1]
    