from typing import TYPE_CHECKING
from numpy import ndarray, zeros
from glm import simplex, vec3

from settings import CHUNK_VOLUME, CHUNK_SIZE, CHUNK_AREA
from meshes.chunk_mesh import ChunkMesh
if TYPE_CHECKING:
    from main import Engine

class Chunk:
    def __init__(self, game: 'Engine') -> None:
        self.game = game
        self.voxels: ndarray = self.build_voxels()
        self.mesh: ChunkMesh = None
        self.build_mesh()
    
    def build_mesh(self) -> None:
        self.mesh = ChunkMesh(self)
    
    def render(self) -> None:
        self.mesh.render()
    
    def build_voxels(self) -> ndarray:
        voxels = zeros(CHUNK_VOLUME, dtype='uint8')
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = (
                        x + y + z if int(simplex(vec3(x, y, z) * 0.1) + 1) else 0
                    )
        return voxels
