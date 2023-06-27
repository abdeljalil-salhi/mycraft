from typing import TYPE_CHECKING

from objects.chunk import Chunk
if TYPE_CHECKING:
    from main import Engine

class Scene:
    def __init__(self, game: 'Engine') -> None:
        self.game = game
        self.chunk = Chunk(self.game)
    
    def update(self) -> None:
        pass
    
    def render(self) -> None:
        self.chunk.render()
    