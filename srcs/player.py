from typing import TYPE_CHECKING
from pygame import key, mouse, K_z, K_s, K_d, K_q, K_w, K_a, K_e, MOUSEBUTTONDOWN
from glm import vec3

from settings import PLAYER_POSITION, PLAYER_SPEED, QWERTY, MOUSE_SENSITIVITY
from srcs.camera import Camera
if TYPE_CHECKING:
    from main import Engine   

class Player(Camera):
    def __init__(self, game: 'Engine', position:vec3=PLAYER_POSITION, yaw:float=-90.0, pitch:float=0.0) -> None:
        self.game = game
        super().__init__(position, yaw, pitch)
    
    def init_player(self, world) -> None:
        self.world = world
        self.event_handler = self.game.event_handler
    
    def update(self) -> None:
        if self.event_handler.inventory_open or self.event_handler.pause or not self.event_handler.ingame:
            return
        self.keyboard_events()
        self.mouse_events()
        super().update()
    
    def mouse_events(self) -> None:
        mouse_dx, mouse_dy = mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)
    
    def handle_mouse_events(self, event) -> None:
        if event.type == MOUSEBUTTONDOWN:
            voxel_handler = self.game.scene.world.voxel_handler
            if event.button == 1:
                voxel_handler.set_voxel()
            elif event.button == 3:
                voxel_handler.switch_interaction_mode()
    
    def keyboard_events(self) -> None:
        key_state = key.get_pressed()
        velocity = self.game.delta_time * PLAYER_SPEED
        if key_state[K_w if QWERTY else K_z]:
            self.move_forward(velocity)
        if key_state[K_s]:
            self.move_backward(velocity)
        if key_state[K_d]:
            self.move_right(velocity)
        if key_state[K_a if QWERTY else K_q]:
            self.move_left(velocity)
        if key_state[K_e]:
            self.move_up(velocity)
        if key_state[K_q if QWERTY else K_a]:
            self.move_down(velocity)
