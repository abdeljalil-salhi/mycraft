from typing import TYPE_CHECKING
from numpy import empty

from settings import WORLD_VOLUME, CHUNK_VOLUME, WORLD_WIDTH, WORLD_HEIGHT, WORLD_DEPTH, WORLD_AREA
from objects.chunk import Chunk
from srcs.voxel_handler import VoxelHandler
if TYPE_CHECKING:
    from main import Engine

class World:
    def __init__(self, game: 'Engine') -> None:
        self.game = game
        self.chunks = [None for _ in range(WORLD_VOLUME)]
        self.voxels = empty([WORLD_VOLUME, CHUNK_VOLUME], dtype='uint8')
        
        self.build_chunks()
        self.build_chunk_mesh()
        self.voxel_handler = VoxelHandler(self)
    
    def build_chunks(self) -> None:
        for x in range(WORLD_WIDTH):
            for y in range(WORLD_HEIGHT):
                for z in range(WORLD_DEPTH):
                    chunk = Chunk(self, position=(x, y, z))
                    
                    chunk_index = x + WORLD_WIDTH * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk
                    self.voxels[chunk_index] = chunk.build_voxels()
                    
                    # Save the pointer to voxels in the chunk
                    chunk.voxels = self.voxels[chunk_index]
    
    def build_chunk_mesh(self) -> None:
        for chunk in self.chunks:
            chunk.build_mesh()
    
    def update(self) -> None:
        self.voxel_handler.update()
    
    def render(self) -> None:
        for chunk in self.chunks:
            chunk.render()
