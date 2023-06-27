from typing import TYPE_CHECKING

from meshes.base_mesh import BaseMesh
from meshes.chunk_mesh_builder import build_chunk_mesh
if TYPE_CHECKING:
    from objects.chunk import Chunk

class ChunkMesh(BaseMesh):
    def __init__(self, chunk: 'Chunk') -> None:
        super().__init__()
        self.game = chunk.game
        self.chunk = chunk
        self.context = self.game.context
        self.shader = self.game.shader.chunk
        
        self.vbo_format = '3u1 1u1 1u1'
        self.format_size = sum(int(f[:1]) for f in self.vbo_format.split())
        self.attrs = ('in_position', 'voxel_id', 'face_id')
        self.vao = self.get_vao()
    
    def get_vertex_data(self):
        return build_chunk_mesh(
            chunk_voxels=self.chunk.voxels,
            format_size=self.format_size)
