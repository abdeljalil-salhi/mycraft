from typing import TYPE_CHECKING
from glm import vec3, translate, mat4x4, mat4

from meshes.cube_mesh import CubeMesh
if TYPE_CHECKING:
    from srcs.voxel_handler import VoxelHandler

class VoxelMarker:
    def __init__(self, voxel_handler: 'VoxelHandler') -> None:
        self.handler = voxel_handler
        self.game = self.handler.game
        self.position = vec3(0.0)
        self.matrix_model = self.get_model_matrix()
        self.mesh = CubeMesh(self.game)
    
    def update(self) -> None:
        if self.handler.voxel_id:
            if self.handler.interaction_mode:
                self.position = self.handler.voxel_world_position + self.handler.voxel_normal
            else:
                self.position = self.handler.voxel_world_position
    
    def set_uniform(self) -> None:
        self.mesh.shader['mode_id'] = self.handler.interaction_mode
        self.mesh.shader['matrix_model'].write(self.get_model_matrix())
    
    def get_model_matrix(self) -> mat4x4:
        return translate(mat4(), vec3(self.position))
    
    def render(self) -> None:
        if self.handler.voxel_id:
            self.set_uniform()
            self.mesh.render()
