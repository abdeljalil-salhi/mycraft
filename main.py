from settings import WINDOW_RESOLUTION, BACKGROUND_COLOR
from pygame import init, display, time, event, quit, GL_CONTEXT_MAJOR_VERSION, GL_CONTEXT_MINOR_VERSION, GL_CONTEXT_PROFILE_MASK, GL_CONTEXT_PROFILE_CORE, GL_DEPTH_SIZE, OPENGL, DOUBLEBUF, QUIT, KEYDOWN, K_ESCAPE
from moderngl import create_context, DEPTH_TEST, CULL_FACE, BLEND
from sys import exit

class Engine:
    def __init__(self) -> None:
        init()
        display.gl_set_attribute(GL_CONTEXT_MAJOR_VERSION, 3)
        display.gl_set_attribute(GL_CONTEXT_MINOR_VERSION, 3)
        display.gl_set_attribute(GL_CONTEXT_PROFILE_MASK, GL_CONTEXT_PROFILE_CORE)
        display.gl_set_attribute(GL_DEPTH_SIZE, 24)
        display.set_mode(WINDOW_RESOLUTION, flags=OPENGL | DOUBLEBUF)

        self.ctx = create_context()
        self.ctx.enable(flags=DEPTH_TEST | CULL_FACE | BLEND)
        self.ctx.gc_mode = 'auto'

        self.clock = time.Clock()
        self.delta_time = 0.0
        self.time = 0.0
        self.is_running = True

    def update(self) -> None:
        self.delta_time = self.clock.tick()
        self.time = time.get_ticks() * 0.001
        display.set_caption(f'FPS: {self.clock.get_fps():.2f}')
    
    def render(self) -> None:
        self.ctx.clear(color=BACKGROUND_COLOR)
        display.flip()
    
    def handle_events(self) -> None:
        for e in event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                self.is_running = False
    
    def run(self) -> None:
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        quit()
        exit()
    
if __name__ == '__main__':
    engine = Engine()
    engine.run()
