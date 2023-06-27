from typing import TYPE_CHECKING
from pygame import image, transform
from moderngl import NEAREST

if TYPE_CHECKING:
    from main import Engine

class Textures:
    def __init__(self, game: 'Engine') -> None:
        self.game = game
        self.context = game.context
        self.texture_0 = self.load('frame')
        self.texture_0.use(location=0)
    
    def load(self, file_name: str) -> None:
        texture = image.load(f'assets/{file_name}.png')
        texture = transform.flip(texture, flip_x=True, flip_y=False)
        texture = self.context.texture(
            size=texture.get_size(),
            components=4,
            data=image.tostring(texture, "RGBA", False),
        )
        texture.anisotropy = 32.0
        texture.build_mipmaps()
        texture.filter = (NEAREST, NEAREST)
        return texture
    