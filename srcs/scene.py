from typing import TYPE_CHECKING

from srcs.world import World
if TYPE_CHECKING:
    from main import Engine

class Scene:
    def __init__(self, game: 'Engine') -> None:
        self.game = game
        self.world = World(self.game)
    
    def update(self) -> None:
        self.world.update()
    
    def render(self) -> None:
        self.world.render()
    