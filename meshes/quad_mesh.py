from typing import TYPE_CHECKING
from numpy import hstack, ndarray, array

from meshes.base_mesh import BaseMesh
if TYPE_CHECKING:
    from main import Engine

class QuadMesh(BaseMesh):
    def __init__(self, game: 'Engine') -> None:
        super().__init__()
        
        self.game = game
        self.context = self.game.context
        self.shader = self.game.shader.water
        
        self.vbo_format = '2u1 3u1'
        self.attrs = ('in_texture_coords', 'in_position')
        self.vao = self.get_vao()
        
    def get_vertex_data(self) -> ndarray:
        vertices = array([
            (0, 0, 0), (1, 0, 1), (1, 0, 0),
            (0, 0, 0), (0, 0, 1), (1, 0, 1)
        ], dtype='uint8')
        texture_coords = array([
            (0, 0), (1, 1), (1, 0),
            (0, 0), (0, 1), (1, 1)
        ], dtype='uint8')
        return hstack([texture_coords, vertices])
    