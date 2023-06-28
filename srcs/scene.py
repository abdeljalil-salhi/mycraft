from typing import TYPE_CHECKING

from srcs.world import World
from objects.voxel_marker import VoxelMarker
if TYPE_CHECKING:
    from main import Engine

class Scene:
    def __init__(self, game: 'Engine') -> None:
        self.game = game
        self.world = World(self.game)
        self.voxel_marker = VoxelMarker(self.world.voxel_handler)
    
    def update(self) -> None:
        self.world.update()
        self.voxel_marker.update()
    
    def render(self) -> None:
        self.world.render()
        self.voxel_marker.render()
    