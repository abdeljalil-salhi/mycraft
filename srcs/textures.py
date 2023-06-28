from typing import TYPE_CHECKING
from pygame import image, transform
from moderngl import NEAREST

if TYPE_CHECKING:
    from main import Engine

class Textures:
    def __init__(self, game: 'Engine') -> None:
        self.game = game
        self.context = game.context
        self.texture = self.load('frame')
        self.texture_array = self.load('textures', is_texture_array=True)
        self.texture.use(location=0)
        self.texture_array.use(location=1)
    
    def load(self, file_name: str, is_texture_array:bool=False) -> None:
        texture = image.load(f'assets/{file_name}.png')
        texture = transform.flip(texture, flip_x=True, flip_y=False)
        
        if is_texture_array:
            # 3 layers for each texture
            num_layers = 3 * texture.get_height() // texture.get_width()
            texture = self.game.context.texture_array(
                size=(texture.get_width(), texture.get_height() // num_layers, num_layers),
                components=4,
                data=image.tostring(texture, "RGBA"),
            )
        else:
            texture = self.context.texture(
                size=texture.get_size(),
                components=4,
                data=image.tostring(texture, "RGBA", False),
            )
        texture.anisotropy = 32.0
        texture.build_mipmaps()
        texture.filter = (NEAREST, NEAREST)
        return texture
    