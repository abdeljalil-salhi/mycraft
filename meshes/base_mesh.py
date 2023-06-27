from numpy import array
from moderngl import VertexArray

class BaseMesh:
    def __init__(self) -> None:
        self.context = None
        self.shader = None
        self.vbo_format = None
        self.attrs: tuple[str, ...] = None
        self.vao = None
    
    def get_vertex_data(self) -> array: ...
    
    def get_vao(self) -> VertexArray:
        vertex_data = self.get_vertex_data()
        vbo = self.context.buffer(vertex_data)
        return self.context.vertex_array(self.shader,
            [(vbo, self.vbo_format, *self.attrs)], skip_errors=True)
        
    def render(self) -> None:
        self.vao.render()
    