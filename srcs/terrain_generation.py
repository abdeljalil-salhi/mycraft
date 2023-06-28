from numba import njit
from math import hypot
from numpy import ndarray
from random import random

from settings import CENTER_XZ, CENTER_Y, CHUNK_SIZE, CHUNK_AREA
from srcs.texturing import *
from srcs.noise import noise2, noise3

@njit
def get_height(x: int, z: int) -> int:
    # Island mask
    island = 1 / (pow(0.0025 * hypot(x - CENTER_XZ, z - CENTER_XZ), 20) + 0.0001)
    island = min(island, 1.0)
    
    # Terrain parameters
    amplitude1 = CENTER_Y
    amplitude2, amplitude4, amplitude8 = amplitude1 * 0.5, amplitude1 * 0.25, amplitude1 * 0.125
    frequency1 = 0.005
    frequency2, frequency4, frequency8 = frequency1 * 2, frequency1 * 4, frequency1 * 8
    
    # Erosion effect
    if noise2(0.1 * x, 0.1 * z) < 0:
        amplitude1 /= 1.07
    
    # Terrain generation
    height  = noise2(x * frequency1, z * frequency1) * amplitude1 + amplitude1
    height += noise2(x * frequency2, z * frequency2) * amplitude2 - amplitude2
    height += noise2(x * frequency4, z * frequency4) * amplitude4 + amplitude4
    height += noise2(x * frequency8, z * frequency8) * amplitude8 - amplitude8
    
    return int(max(height, 1) * island)

@njit
def get_index(x: int, y: int, z: int) -> int:
    return x + CHUNK_SIZE * z + CHUNK_AREA * y

@njit
def set_voxel_id(voxels: ndarray, x: int, y: int, z: int, wx: int, wy: int, wz: int, world_height: int) -> None:
    voxel_id = 0
    
    if wy < world_height - 1:
        # Generating caves
        if (noise3(wx * 0.09, wy * 0.09, wz * 0.09) > 0
            and noise2(wx * 0.1, wz * 0.1) * 3 + 3 < wy < world_height - 10):
            voxel_id = 0
        else:
            if random() < DIAMOND_PROBABILITY:
                voxel_id = DIAMOND_ORE
            else:
                voxel_id = STONE
    else:
        rng = int(7 * random())
        ry = wy - rng
        if SNOW_LEVEL <= ry < world_height:
            voxel_id = SNOW
        elif STONE_LEVEL <= ry < SNOW_LEVEL:
            voxel_id = STONE
        elif DIRT_LEVEL <= ry < STONE_LEVEL:
            voxel_id = DIRT
        elif GRASS_LEVEL <= ry < DIRT_LEVEL:
            voxel_id = GRASS
        else:
            voxel_id = SAND
    
    voxels[get_index(x, y, z)] = voxel_id
    
    # Generating trees
    if wy < DIRT_LEVEL:
        generate_tree(voxels, x, y, z, voxel_id)

@njit
def generate_tree(voxels: ndarray, x: int, y: int, z: int, voxel_id: int):    
    if voxel_id != GRASS or random() > TREE_PROBABILITY:
        return None
    if y + TREE_HEIGHT >= CHUNK_SIZE:
        return None
    if x - TREE_H_WIDTH < 0 or x + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    if z - TREE_H_WIDTH < 0 or z + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    
    # Generate dirt under the tree
    voxels[get_index(x, y, z)] = DIRT
    
    # Generate leaves
    m = 0
    rnd2 = random()
    for n, iy in enumerate(range(TREE_H_HEIGHT, TREE_HEIGHT - 1)):
        k = iy % 2
        rng = int(random() * 2)
        for ix in range(-TREE_H_WIDTH + m, TREE_H_WIDTH - m * rng):
            for iz in range(-TREE_H_WIDTH + m * rng, TREE_H_WIDTH - m):
                if (ix + iz) % 4:
                    if rnd2 < SAKURA_PROBABILITY:
                        voxels[get_index(x + ix + k, y + iy, z + iz + k)] = SAKURA_LEAVES
                    else:
                        voxels[get_index(x + ix + k, y + iy, z + iz + k)] = TRANSPARENT_LEAVES
        m += 1 if n > 0 else 3 if n > 1 else 0
    
    # Generate tree trunk
    for iy in range(1, TREE_HEIGHT - 2):
        voxels[get_index(x, y + iy, z)] = WOOD
    
    # Generate tree top
    if rnd2 < SAKURA_PROBABILITY:
        voxels[get_index(x, y + TREE_HEIGHT - 2, z)] = SAKURA_LEAVES
    else:
        voxels[get_index(x, y + TREE_HEIGHT - 2, z)] = TRANSPARENT_LEAVES
