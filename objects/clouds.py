from typing import TYPE_CHECKING

from meshes.cloud_mesh import CloudMesh
if TYPE_CHECKING:
    from main import Engine

class Clouds:
    def __init__(self, game: 'Engine') -> None:
        self.game = game
        self.mesh = CloudMesh(game)
    
    def update(self) -> None:
        self.mesh.shader['unit_time'] = self.game.time
    
    def render(self) -> None:
        self.mesh.render()
