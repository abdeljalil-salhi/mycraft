from settings import CHUNK_SIZE, WORLD_WIDTH, WORLD_HEIGHT

# Textures IDs
SAND = 1
GRASS = 2
DIRT = 3
STONE = 4
SNOW = 5
LEAVES = 6
WOOD = 7

# Terrain levels
SNOW_LEVEL = 54
STONE_LEVEL = 49
DIRT_LEVEL = 40
GRASS_LEVEL = 8
SAND_LEVEL = 7

# Trees settings
TREE_PROBABILITY = 0.02
TREE_WIDTH, TREE_HEIGHT = 4, 8
TREE_H_WIDTH, TREE_H_HEIGHT = TREE_WIDTH // 2, TREE_HEIGHT // 2

# Water settings
WATER_LINE = 5.6
WATER_AREA = 5 * CHUNK_SIZE * WORLD_WIDTH

# Cloud settings
CLOUD_SCALE = 25
CLOUD_HEIGHT = WORLD_HEIGHT * CHUNK_SIZE * 2