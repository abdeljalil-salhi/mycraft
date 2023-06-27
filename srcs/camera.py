from glm import vec3, radians, perspective, mat4, cos, sin, normalize, cross, lookAt, clamp

from settings import VERTICAL_FOV, ASPECT_RATIO, NEAR, FAR, PITCH_LIMIT

class Camera:
    def __init__(self, position: float, yaw: float, pitch: float) -> None:
        self.position = vec3(position)
        self.yaw = radians(yaw)
        self.pitch = radians(pitch)
        
        self.up = vec3(0.0, 1.0, 0.0)
        self.right = vec3(1.0, 0.0, 0.0)
        self.forward = vec3(0.0, 0.0, -1.0)
        
        self.matrix_projection = perspective(VERTICAL_FOV, ASPECT_RATIO, NEAR, FAR)
        self.matrix_view = mat4()
    
    def update(self) -> None:
        self.update_vectors()
        self.update_view_matrix()
    
    def update_view_matrix(self) -> None:
        self.matrix_view = lookAt(self.position, self.position + self.forward, self.up)
    
    def update_vectors(self) -> None:
        self.forward.x = cos(self.yaw) * cos(self.pitch)
        self.forward.y = sin(self.pitch)
        self.forward.z = sin(self.yaw) * cos(self.pitch)
        
        self.forward = normalize(self.forward)
        self.right = normalize(cross(self.forward, vec3(0.0, 1.0, 0.0)))
        self.up = normalize(cross(self.right, self.forward))
    
    def rotate_pitch(self, delta_y: float) -> None:
        self.pitch -= delta_y
        self.pitch = clamp(self.pitch, -PITCH_LIMIT, PITCH_LIMIT)
    
    def rotate_yaw(self, delta_x: float) -> None:
        self.yaw += delta_x
    
    def move_forward(self, velocity: float) -> None:
        self.position += self.forward * velocity
    
    def move_backward(self, velocity: float) -> None:
        self.position -= self.forward * velocity
    
    def move_right(self, velocity: float) -> None:
        self.position += self.right * velocity
    
    def move_left(self, velocity: float) -> None:
        self.position -= self.right * velocity
    
    def move_up(self, velocity: float) -> None:
        self.position += self.up * velocity
    
    def move_down(self, velocity: float) -> None:
        self.position -= self.up * velocity
    