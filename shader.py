from typing import TYPE_CHECKING
from moderngl import Program

if TYPE_CHECKING:
    from main import Engine

class Shader:
    def __init__(self, game: 'Engine') -> None:
        self.game = game
        self.context = game.context
        self.quad = self.get_program('quad')
        
        self.set_uniforms_on_init()
    
    def set_uniforms_on_init(self) -> None:
        pass
    
    def update(self) -> None:
        pass

    def get_program(self, shader_name: str) -> Program:
        with open(f'shaders/{shader_name}.vert', 'r') as f:
            vertex_shader = f.read()
        with open(f'shaders/{shader_name}.frag', 'r') as f:
            fragment_shader = f.read()
        return self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
