from numba import njit, uint8
from numpy import ndarray, empty
from glm import vec3

from settings import CHUNK_VOLUME, CHUNK_SIZE, CHUNK_AREA, WORLD_WIDTH, WORLD_HEIGHT, WORLD_DEPTH, WORLD_AREA

@njit
def get_ao(local_position: vec3, world_position: vec3, world_voxels: ndarray, plane: str) -> tuple:
    x, y, z = local_position
    wx, wy, wz = world_position

    if plane == 'Y':
        a = is_void((x    , y    , z - 1), (wx    , wy    , wz - 1), world_voxels)
        b = is_void((x - 1, y    , z - 1), (wx - 1, wy    , wz - 1), world_voxels)
        c = is_void((x - 1, y    , z    ), (wx - 1, wy    , wz    ), world_voxels)
        d = is_void((x - 1, y    , z + 1), (wx - 1, wy    , wz + 1), world_voxels)
        e = is_void((x    , y    , z + 1), (wx    , wy    , wz + 1), world_voxels)
        f = is_void((x + 1, y    , z + 1), (wx + 1, wy    , wz + 1), world_voxels)
        g = is_void((x + 1, y    , z    ), (wx + 1, wy    , wz    ), world_voxels)
        h = is_void((x + 1, y    , z - 1), (wx + 1, wy    , wz - 1), world_voxels)
    elif plane == 'X':
        a = is_void((x    , y    , z - 1), (wx    , wy    , wz - 1), world_voxels)
        b = is_void((x    , y - 1, z - 1), (wx    , wy - 1, wz - 1), world_voxels)
        c = is_void((x    , y - 1, z    ), (wx    , wy - 1, wz    ), world_voxels)
        d = is_void((x    , y - 1, z + 1), (wx    , wy - 1, wz + 1), world_voxels)
        e = is_void((x    , y    , z + 1), (wx    , wy    , wz + 1), world_voxels)
        f = is_void((x    , y + 1, z + 1), (wx    , wy + 1, wz + 1), world_voxels)
        g = is_void((x    , y + 1, z    ), (wx    , wy + 1, wz    ), world_voxels)
        h = is_void((x    , y + 1, z - 1), (wx    , wy + 1, wz - 1), world_voxels)
    elif plane == 'Z':
        a = is_void((x - 1, y    , z    ), (wx - 1, wy    , wz    ), world_voxels)
        b = is_void((x - 1, y - 1, z    ), (wx - 1, wy - 1, wz    ), world_voxels)
        c = is_void((x    , y - 1, z    ), (wx    , wy - 1, wz    ), world_voxels)
        d = is_void((x + 1, y - 1, z    ), (wx + 1, wy - 1, wz    ), world_voxels)
        e = is_void((x + 1, y    , z    ), (wx + 1, wy    , wz    ), world_voxels)
        f = is_void((x + 1, y + 1, z    ), (wx + 1, wy + 1, wz    ), world_voxels)
        g = is_void((x    , y + 1, z    ), (wx    , wy + 1, wz    ), world_voxels)
        h = is_void((x - 1, y + 1, z    ), (wx - 1, wy + 1, wz    ), world_voxels)

    ao = (a + b + c), (g + h + a), (e + f + g), (c + d + e)
    return ao

@njit
def to_uint8(x: int, y: int, z: int, voxel_id: int, face_id: int, ao_id: int) -> tuple:
    return uint8(x), uint8(y), uint8(z), uint8(voxel_id), uint8(face_id), uint8(ao_id)

@njit
def get_chunk_index(world_voxel_position: vec3) -> int:
    wx, wy, wz = world_voxel_position
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE
    if not (0 <= cx < WORLD_WIDTH and 0 <= cy < WORLD_HEIGHT and 0 <= cz < WORLD_DEPTH):
        return -1
    return cx + WORLD_WIDTH * cz + WORLD_AREA * cy

@njit
def is_void(local_voxel_position: vec3, world_voxel_position: vec3, world_voxels: ndarray) -> bool:
    chunk_index = get_chunk_index(world_voxel_position)
    if chunk_index == -1:
        return False
    
    chunk_voxels = world_voxels[chunk_index]
    x, y, z = local_voxel_position
    
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
                    ao = get_ao((x, y + 1, z), (wx, wy + 1, wz), world_voxels, 'Y')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]
                    
                    # format: x, y, z, voxel_id, face_id
                    v0 = to_uint8(x    , y + 1, z    , voxel_id, 0, ao[0])
                    v1 = to_uint8(x + 1, y + 1, z    , voxel_id, 0, ao[1])
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 0, ao[2])
                    v3 = to_uint8(x    , y + 1, z + 1, voxel_id, 0, ao[3])
                    
                    if flip_id:
                        index = add_data(vertex_data, index, v1, v0, v3, v1, v3, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)
                
                # Bottom face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    ao = get_ao((x, y - 1, z), (wx, wy - 1, wz), world_voxels, 'Y')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]
                    
                    v0 = to_uint8(x    , y    , z    , voxel_id, 1, ao[0])
                    v1 = to_uint8(x + 1, y    , z    , voxel_id, 1, ao[1])
                    v2 = to_uint8(x + 1, y    , z + 1, voxel_id, 1, ao[2])
                    v3 = to_uint8(x    , y    , z + 1, voxel_id, 1, ao[3])
                    
                    if flip_id:
                        index = add_data(vertex_data, index, v1, v3, v0, v1, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)
                
                # Right face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    ao = get_ao((x + 1, y, z), (wx + 1, wy, wz), world_voxels, 'X')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]
                    
                    v0 = to_uint8(x + 1, y    , z    , voxel_id, 2, ao[0])
                    v1 = to_uint8(x + 1, y + 1, z    , voxel_id, 2, ao[1])
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 2, ao[2])
                    v3 = to_uint8(x + 1, y    , z + 1, voxel_id, 2, ao[3])
                    
                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                
                # Left face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    ao = get_ao((x - 1, y, z), (wx - 1, wy, wz), world_voxels, 'X')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]
                    
                    v1 = to_uint8(x    , y + 1, z    , voxel_id, 3, ao[0])
                    v0 = to_uint8(x    , y    , z    , voxel_id, 3, ao[1])
                    v2 = to_uint8(x    , y + 1, z + 1, voxel_id, 3, ao[2])
                    v3 = to_uint8(x    , y    , z + 1, voxel_id, 3, ao[3])
                    
                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)
                
                # Back face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    ao = get_ao((x, y, z - 1), (wx, wy, wz - 1), world_voxels, 'Z')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]
                    
                    v0 = to_uint8(x    , y    , z    , voxel_id, 4, ao[0])
                    v1 = to_uint8(x    , y + 1, z    , voxel_id, 4, ao[1])
                    v2 = to_uint8(x + 1, y + 1, z    , voxel_id, 4, ao[2])
                    v3 = to_uint8(x + 1, y    , z    , voxel_id, 4, ao[3])
                    
                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)
                
                # Front face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    ao = get_ao((x, y, z + 1), (wx, wy, wz + 1), world_voxels, 'Z')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]
                    
                    v0 = to_uint8(x    , y    , z + 1, voxel_id, 5, ao[0])
                    v1 = to_uint8(x    , y + 1, z + 1, voxel_id, 5, ao[1])
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 5, ao[2])
                    v3 = to_uint8(x + 1, y    , z + 1, voxel_id, 5, ao[3])
                    
                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)
    
    return vertex_data[:index + 1]
    