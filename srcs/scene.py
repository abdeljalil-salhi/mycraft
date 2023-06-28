from typing import TYPE_CHECKING
from moderngl import CULL_FACE

from srcs.world import World
from objects.voxel_marker import VoxelMarker
from objects.water import Water
from objects.clouds import Clouds
if TYPE_CHECKING:
    from main import Engine

class Scene:
    def __init__(self, game: 'Engine') -> None:
        self.game = game
        self.world = World(self.game)
        self.voxel_marker = VoxelMarker(self.world.voxel_handler)
        self.water = Water(self.game)
        self.clouds = Clouds(self.game)
    
    def update(self) -> None:
        self.world.update()
        self.voxel_marker.update()
        self.clouds.update()
    
    def render(self) -> None:
        # Chunks rendering
        self.world.render()
        
        # Rendering clouds and water without cull facing
        self.game.context.disable(CULL_FACE)
        self.clouds.render()
        self.water.render()
        self.game.context.enable(CULL_FACE)
        
        # Voxel marker rendering
        self.voxel_marker.render()
