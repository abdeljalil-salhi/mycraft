from typing import TYPE_CHECKING
from numpy import ndarray, zeros, any
from glm import simplex, vec2, vec3, translate, mat4, mat4x4, ivec3

from settings import CHUNK_VOLUME, CHUNK_SIZE, CHUNK_AREA
from meshes.chunk_mesh import ChunkMesh
if TYPE_CHECKING:
    from srcs.world import World

class Chunk:
    def __init__(self, world: 'World', position: tuple) -> None:
        self.game = world.game
        self.world = world
        self.position = position
        self.matrix_model = self.get_model_matrix()
        self.voxels: ndarray = None
        self.mesh: ChunkMesh = None
        self.is_empty = True
    
    def get_model_matrix(self) -> mat4x4:
        return translate(mat4(), vec3(self.position) * CHUNK_SIZE)

    def set_uniform(self) -> None:
        self.mesh.shader['matrix_model'].write(self.matrix_model)
    
    def build_mesh(self) -> None:
        self.mesh = ChunkMesh(self)
    
    def render(self) -> None:
        if not self.is_empty:
            self.set_uniform()
            self.mesh.render()
    
    def build_voxels(self) -> ndarray:
        voxels = zeros(CHUNK_VOLUME, dtype='uint8')
        cx, cy, cz = ivec3(self.position) * CHUNK_SIZE
        for x in range(CHUNK_SIZE):
            wx = x + cx
            for z in range(CHUNK_SIZE):
                wz = z + cz
                world_height = int(simplex(vec2(wx, wz) * 0.01) * 32 + 32)
                local_height = min(world_height - cy, CHUNK_SIZE)
                for y in range(local_height):
                    wy = y + cy
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = wy + 1
        
        if any(voxels):
            self.is_empty = False
        
        return voxels
