from enum import Enum

from settings import CHUNK_SIZE, WORLD_WIDTH, WORLD_HEIGHT

# Textures IDs
class Texture(Enum):
    SAND = 1
    GRASS = 2
    DIRT = 3
    STONE = 4
    SNOW = 5
    SAKURA_LEAVES = 6
    WOOD = 7
    TNT = 8
    OAK_PLANK = 9
    DIAMOND_ORE = 10
    NORMAL_LEAVES = 11
    BEEHIVE = 12
    OAK_LEAVES = 13
    GOLD_BLOCK = 14

# Terrain levels
class TerrainLevel(Enum):
    SAND = 7
    GRASS = 8
    DIRT = 40
    STONE = 49
    SNOW = 54

# World settings
DIAMOND_PROBABILITY = 0.002

# Trees settings
TREE_PROBABILITY = 0.02
TNT_PROBABILITY = 0.01
SAKURA_PROBABILITY = 0.05
OAK_PROBABILITY = 0.15
BEEHIVE_PROBABILITY = 0.01
TREE_WIDTH, TREE_HEIGHT = 4, 8
TREE_H_WIDTH, TREE_H_HEIGHT = TREE_WIDTH // 2, TREE_HEIGHT // 2

# Water settings
WATER_LINE = 5.8
WATER_AREA = 5 * CHUNK_SIZE * WORLD_WIDTH

# Cloud settings
CLOUD_SCALE = 25
CLOUD_HEIGHT = WORLD_HEIGHT * CHUNK_SIZE * 2
