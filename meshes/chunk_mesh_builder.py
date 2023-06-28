from numba import njit
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

    return (a + b + c), (g + h + a), (e + f + g), (c + d + e)

@njit
def pack_data(x: int, y: int, z: int, voxel_id: int, face_id: int, ao_id: int, flip_id: int) -> tuple:
    # x: 6bit  y: 6bit  z: 6bit  voxel_id: 8bit  face_id: 3bit  ao_id: 2bit  flip_id: 1bit
    a, b, c, d, e, f, g = x, y, z, voxel_id, face_id, ao_id, flip_id
    
    b_bit, c_bit, d_bit, e_bit, f_bit, g_bit = 6, 6, 8, 3, 2, 1
    fg_bit = f_bit + g_bit
    efg_bit = e_bit + fg_bit
    defg_bit = d_bit + efg_bit
    cdefg_bit = c_bit + defg_bit
    bcdefg_bit = b_bit + cdefg_bit
    
    packed_data = (
        a << bcdefg_bit |
        b << cdefg_bit |
        c << defg_bit |
        d << efg_bit |
        e << fg_bit |
        f << g_bit | g
    )
    return packed_data

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
        vertex_data[index] = vertex
        index += 1
    return index

@njit
def build_chunk_mesh(chunk_voxels: ndarray, format_size: int, chunk_position: tuple, world_voxels: ndarray) -> ndarray:
    # Well, here; the maximum number of visible faces is 3
    # and each face is built from 2 triangles with 3 vertices each
    # so 3 * 2 * 3 = 18 vertices per voxel
    vertex_data = empty(CHUNK_VOLUME * 18 * format_size, dtype='uint32')
    index = 0
    
    for x in range(CHUNK_SIZE):
        for y in range (CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                if not voxel_id:
                    continue
                
                # Get the world position of the voxel
                cx, cy, cz = chunk_position
                wx = x + cx * CHUNK_SIZE
                wy = y + cy * CHUNK_SIZE
                wz = z + cz * CHUNK_SIZE

                # Top face
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
                    ao = get_ao((x, y + 1, z), (wx, wy + 1, wz), world_voxels, plane='Y')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    # Format: x, y, z, voxel_id, face_id, ao_id, flip_id
                    v0 = pack_data(x    , y + 1, z    , voxel_id, 0, ao[0], flip_id)
                    v1 = pack_data(x + 1, y + 1, z    , voxel_id, 0, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 0, ao[2], flip_id)
                    v3 = pack_data(x    , y + 1, z + 1, voxel_id, 0, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v0, v3, v1, v3, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # Bottom face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    ao = get_ao((x, y - 1, z), (wx, wy - 1, wz), world_voxels, plane='Y')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x    , y    , z    , voxel_id, 1, ao[0], flip_id)
                    v1 = pack_data(x + 1, y    , z    , voxel_id, 1, ao[1], flip_id)
                    v2 = pack_data(x + 1, y    , z + 1, voxel_id, 1, ao[2], flip_id)
                    v3 = pack_data(x    , y    , z + 1, voxel_id, 1, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v3, v0, v1, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # Right face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    ao = get_ao((x + 1, y, z), (wx + 1, wy, wz), world_voxels, plane='X')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x + 1, y    , z    , voxel_id, 2, ao[0], flip_id)
                    v1 = pack_data(x + 1, y + 1, z    , voxel_id, 2, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 2, ao[2], flip_id)
                    v3 = pack_data(x + 1, y    , z + 1, voxel_id, 2, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Left face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    ao = get_ao((x - 1, y, z), (wx - 1, wy, wz), world_voxels, plane='X')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x    , y    , z    , voxel_id, 3, ao[0], flip_id)
                    v1 = pack_data(x    , y + 1, z    , voxel_id, 3, ao[1], flip_id)
                    v2 = pack_data(x    , y + 1, z + 1, voxel_id, 3, ao[2], flip_id)
                    v3 = pack_data(x    , y    , z + 1, voxel_id, 3, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # Back face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    ao = get_ao((x, y, z - 1), (wx, wy, wz - 1), world_voxels, plane='Z')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x,     y,     z    , voxel_id, 4, ao[0], flip_id)
                    v1 = pack_data(x,     y + 1, z    , voxel_id, 4, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z    , voxel_id, 4, ao[2], flip_id)
                    v3 = pack_data(x + 1, y,     z    , voxel_id, 4, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Front face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    ao = get_ao((x, y, z + 1), (wx, wy, wz + 1), world_voxels, plane='Z')
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x    , y    , z + 1, voxel_id, 5, ao[0], flip_id)
                    v1 = pack_data(x    , y + 1, z + 1, voxel_id, 5, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 5, ao[2], flip_id)
                    v3 = pack_data(x + 1, y    , z + 1, voxel_id, 5, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)
    
    return vertex_data[:index + 1]
