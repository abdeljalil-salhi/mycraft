from typing import TYPE_CHECKING
from glm import dot
from math import cos, tan

from settings import CHUNK_SPHERE_RADIUS, NEAR, FAR, HORIZONTAL_FOV, VERTICAL_FOV
from objects.chunk import Chunk
if TYPE_CHECKING:
    from srcs.camera import Camera

class Frustum:
    def __init__(self, camera: 'Camera') -> None:
        self.camera = camera
        
        self.factor_x = 1.0 / cos(half_x := HORIZONTAL_FOV * 0.5)
        self.tan_x = tan(half_x)
        self.factor_y = 1.0 / cos(half_y := VERTICAL_FOV * 0.5)
        self.tan_y = tan(half_y)
    
    def is_on_frustum(self, chunk: 'Chunk') -> bool:
        sphere_vector = chunk.center - self.camera.position
        
        # Outside the NEAR and FAR planes
        sz = dot(sphere_vector, self.camera.forward)
        if not (NEAR - CHUNK_SPHERE_RADIUS <= sz <= FAR + CHUNK_SPHERE_RADIUS):
            return False
        
        # Outside the TOP and BOTTOM planes
        sy = dot(sphere_vector, self.camera.up)
        distance = self.factor_y * CHUNK_SPHERE_RADIUS + sz * self.tan_y
        if not (-distance <= sy <= distance):
            return False
        
        # Outside the LEFT and RIGHT planes
        sx = dot(sphere_vector, self.camera.right)
        distance = self.factor_x * CHUNK_SPHERE_RADIUS + sz * self.tan_x
        if not (-distance <= sx <= distance):
            return False
        
        return True
