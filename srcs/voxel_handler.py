from typing import TYPE_CHECKING
from glm import ivec3, sign, fract

from settings import MAX_RAY_DISTANCE, CHUNK_SIZE, WORLD_WIDTH, WORLD_HEIGHT, WORLD_DEPTH, CHUNK_AREA, WORLD_AREA
from meshes.chunk_mesh_builder import get_chunk_index
from objects.chunk import Chunk
from srcs.texturing import Texture
if TYPE_CHECKING:
    from srcs.world import World

class VoxelHandler:
    def __init__(self, world: 'World') -> None:
        self.game = world.game
        self.chunks = world.chunks
        
        # Ray casting
        self.chunk: 'Chunk' = None
        self.voxel_id = None
        self.voxel_index = None
        self.voxel_local_position = None
        self.voxel_world_position = None
        self.voxel_normal = None
        
        # 0: Remove voxel, 1: Add voxel
        self.interaction_mode = 0
        self.new_voxel_id = Texture.OAK_PLANK.value
    
    def rebuild_adjacent_chunk(self, adjacent_voxel_position) -> None:
        index = get_chunk_index(adjacent_voxel_position)
        if index != -1:
            self.chunks[index].mesh.rebuild()
    
    def rebuild_adjacent_chunks(self) -> None:
        lx, ly, lz = self.voxel_local_position
        wx, wy, wz = self.voxel_world_position
        
        if lx == 0:
            self.rebuild_adjacent_chunk((wx - 1, wy, wz))
        elif lx == CHUNK_SIZE - 1:
            self.rebuild_adjacent_chunk((wx + 1, wy, wz))
        if ly == 0:
            self.rebuild_adjacent_chunk((wx, wy - 1, wz))
        elif ly == CHUNK_SIZE - 1:
            self.rebuild_adjacent_chunk((wx, wy + 1, wz))
        if lz == 0:
            self.rebuild_adjacent_chunk((wx, wy, wz - 1))
        elif lz == CHUNK_SIZE - 1:
            self.rebuild_adjacent_chunk((wx, wy, wz + 1))
    
    def add_voxel(self) -> None:
        if self.voxel_id:
            result = self.get_voxel_id(self.voxel_world_position + self.voxel_normal)
            if not result[0]:
                self.game.mixer.put_sound.play()
                _, voxel_index, _, chunk = result
                chunk.voxels[voxel_index] = self.new_voxel_id
                chunk.mesh.rebuild()
                if chunk.is_empty:
                    chunk.is_empty = False
    
    def remove_voxel(self) -> None:
        if self.voxel_id:
            self.game.mixer.harvest_sound.play()
            self.chunk.voxels[self.voxel_index] = 0
            self.chunk.mesh.rebuild()
            self.rebuild_adjacent_chunks()
    
    def set_voxel(self) -> None:
        self.add_voxel() if self.interaction_mode else self.remove_voxel()
    
    def switch_interaction_mode(self) -> None:
        self.interaction_mode = not self.interaction_mode
    
    def update(self) -> None:
        self.ray_cast()
    
    def ray_cast(self) -> bool:
        # Starting point
        x1, y1, z1 = self.game.player.position
        # Ending point
        x2, y2, z2 = self.game.player.position + self.game.player.forward * MAX_RAY_DISTANCE
        current_voxel_position = ivec3(x1, y1, z1)
        self.voxel_id = 0
        self.voxel_normal = ivec3(0)
        step_direction = -1
        dx = sign(x2 - x1)
        delta_x = min(dx / (x2 - x1), 10000000.0) if dx != 0 else 10000000.0
        max_x = delta_x * (1.0 - fract(x1)) if dx > 0 else delta_x * fract(x1)
        dy = sign(y2 - y1)
        delta_y = min(dy / (y2 - y1), 10000000.0) if dy != 0 else 10000000.0
        max_y = delta_y * (1.0 - fract(y1)) if dy > 0 else delta_y * fract(y1)
        dz = sign(z2 - z1)
        delta_z = min(dz / (z2 - z1), 10000000.0) if dz != 0 else 10000000.0
        max_z = delta_z * (1.0 - fract(z1)) if dz > 0 else delta_z * fract(z1)
        while not (max_x > 1.0 and max_y > 1.0 and max_z > 1.0):
            result = self.get_voxel_id(voxel_world_position=current_voxel_position)
            if result[0]:
                self.voxel_id, self.voxel_index, self.voxel_local_position, self.chunk = result
                self.voxel_world_position = current_voxel_position

                if step_direction == 0:
                    self.voxel_normal.x = -dx
                elif step_direction == 1:
                    self.voxel_normal.y = -dy
                else:
                    self.voxel_normal.z = -dz
                return True
            if max_x < max_y:
                if max_x < max_z:
                    current_voxel_position.x += dx
                    max_x += delta_x
                    step_direction = 0
                else:
                    current_voxel_position.z += dz
                    max_z += delta_z
                    step_direction = 2
            else:
                if max_y < max_z:
                    current_voxel_position.y += dy
                    max_y += delta_y
                    step_direction = 1
                else:
                    current_voxel_position.z += dz
                    max_z += delta_z
                    step_direction = 2
        return 

    def get_voxel_id(self, voxel_world_position: ivec3) -> tuple:
        cx, cy, cz = chunk_position = voxel_world_position / CHUNK_SIZE
        if 0 <= cx < WORLD_WIDTH and 0 <= cy < WORLD_HEIGHT and 0 <= cz < WORLD_DEPTH:
            chunk_index = cx + WORLD_WIDTH * cz + WORLD_AREA * cy
            chunk = self.chunks[chunk_index]
            lx, ly, lz = voxel_local_position = voxel_world_position - chunk_position * CHUNK_SIZE
            voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
            voxel_id = chunk.voxels[voxel_index]
            return voxel_id, voxel_index, voxel_local_position, chunk
        return 0, 0, 0, 0
