from typing import TYPE_CHECKING
from numpy import array, hstack, ndarray

from meshes.base_mesh import BaseMesh
if TYPE_CHECKING:
    from main import Engine

class CubeMesh(BaseMesh):
    def __init__(self, game: 'Engine') -> None:
        super().__init__()
        
        self.game = game
        self.context = self.game.context
        self.shader = self.game.shader.voxel_marker
        
        self.vbo_format = '2f2 3f2'
        self.attrs = ('in_texture_coords', 'in_position',)
        self.vao = self.get_vao()
    
    @staticmethod
    def get_data(vertices: list, indices: list) -> ndarray:
        return array([vertices[i] for triangle in indices for i in triangle], dtype='float16')
    
    def get_vertex_data(self) -> ndarray:
        vertices = [
            (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1),
            (0, 1, 0), (0, 0, 0), (1, 0, 0), (1, 1, 0)
        ]
        indices = [
            (0, 2, 3), (0, 1, 2),
            (1, 7, 2), (1, 6, 7),
            (6, 5, 4), (4, 7, 6),
            (3, 4, 5), (3, 5, 0),
            (3, 7, 4), (3, 2, 7),
            (0, 6, 1), (0, 5, 6)
        ]
        vertex_data = self.get_data(vertices, indices)
        
        texture_coords_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        texture_coords_indices = [
            (0, 2, 3), (0, 1, 2),
            (0, 2, 3), (0, 1, 2),
            (0, 1, 2), (2, 3, 0),
            (2, 3, 0), (2, 0, 1),
            (0, 2, 3), (0, 1, 2),
            (3, 1, 2), (3, 0, 1),
        ]
        texture_coords_data = self.get_data(texture_coords_vertices, texture_coords_indices)
        
        return hstack([texture_coords_data, vertex_data])
