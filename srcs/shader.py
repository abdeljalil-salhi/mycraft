from typing import TYPE_CHECKING
from moderngl import Program
from glm import mat4

if TYPE_CHECKING:
    from main import Engine

class Shader:
    def __init__(self, game: 'Engine') -> None:
        self.game = game
        self.context = game.context
        self.player = game.player
        self.chunk = self.get_program('chunk')
        
        self.set_uniforms_on_init()
    
    def set_uniforms_on_init(self) -> None:
        self.chunk['matrix_projection'].write(self.player.matrix_projection)
        self.chunk['matrix_model'].write(mat4())
    
    def update(self) -> None:
        self.chunk['matrix_view'].write(self.player.matrix_view)

    def get_program(self, shader_name: str) -> Program:
        with open(f'shaders/{shader_name}.vert', 'r') as f:
            vertex_shader = f.read()
        with open(f'shaders/{shader_name}.frag', 'r') as f:
            fragment_shader = f.read()
        return self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
