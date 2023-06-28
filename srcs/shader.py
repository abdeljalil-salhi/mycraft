from typing import TYPE_CHECKING
from moderngl import Program
from glm import mat4

from settings import BACKGROUND_COLOR, CENTER_XZ
from srcs.texturing import WATER_LINE, WATER_AREA, CLOUD_SCALE
if TYPE_CHECKING:
    from main import Engine

class Shader:
    def __init__(self, game: 'Engine') -> None:
        self.game = game
        self.context = game.context
        self.player = game.player
        self.chunk = self.get_program(shader_name='chunk')
        self.voxel_marker = self.get_program(shader_name='voxel_marker')
        self.water = self.get_program(shader_name='water')
        self.clouds = self.get_program(shader_name='clouds')
        
        self.set_uniforms_on_init()
    
    def set_uniforms_on_init(self) -> None:
        self.chunk['matrix_projection'].write(self.player.matrix_projection)
        self.chunk['matrix_model'].write(mat4())
        self.chunk['unit_texture_array'] = 1
        self.chunk['background_color'].write(BACKGROUND_COLOR);
        self.chunk['water_line'] = WATER_LINE
        
        self.voxel_marker['matrix_projection'].write(self.player.matrix_projection)
        self.voxel_marker['matrix_model'].write(mat4())
        self.voxel_marker['unit_texture'] = 0
        
        self.water['matrix_projection'].write(self.player.matrix_projection)
        self.water['unit_texture'] = 2
        self.water['water_area'] = WATER_AREA
        self.water['water_line'] = WATER_LINE
        
        self.clouds['matrix_projection'].write(self.player.matrix_projection)
        self.clouds['center'] = CENTER_XZ
        self.clouds['background_color'].write(BACKGROUND_COLOR)
        self.clouds['cloud_scale'] = CLOUD_SCALE
    
    def update(self) -> None:
        self.chunk['matrix_view'].write(self.player.matrix_view)
        self.voxel_marker['matrix_view'].write(self.player.matrix_view)
        self.water['matrix_view'].write(self.player.matrix_view)
        self.clouds['matrix_view'].write(self.player.matrix_view)

    def get_program(self, shader_name: str) -> Program:
        with open(f'shaders/{shader_name}.vert', 'r') as f:
            vertex_shader = f.read()
        with open(f'shaders/{shader_name}.frag', 'r') as f:
            fragment_shader = f.read()
        return self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
