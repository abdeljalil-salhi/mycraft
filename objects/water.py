from typing import TYPE_CHECKING

from meshes.quad_mesh import QuadMesh
if TYPE_CHECKING:
    from main import Engine

class Water:
    def __init__(self, game: 'Engine') -> None:
        self.game = game
        self.mesh = QuadMesh(game)
    
    def render(self) -> None:
        self.mesh.render()
