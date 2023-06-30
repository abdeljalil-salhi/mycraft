from pygame import init, display, time, event, mouse, quit, GL_CONTEXT_MAJOR_VERSION, GL_CONTEXT_MINOR_VERSION, GL_CONTEXT_PROFILE_MASK, GL_CONTEXT_PROFILE_CORE, GL_DEPTH_SIZE, OPENGL, DOUBLEBUF, QUIT, KEYDOWN, K_ESCAPE
from moderngl import create_context, DEPTH_TEST, CULL_FACE, BLEND
from sys import exit

from settings import WINDOW_RESOLUTION, BACKGROUND_COLOR
from srcs.shader import Shader
from srcs.scene import Scene
from srcs.player import Player
from srcs.textures import Textures
from srcs.inventory import Inventory
from srcs.event_handler import EventHandler
from srcs.mixer import Mixer

class Engine:
    def __init__(self) -> None:
        init()
        display.gl_set_attribute(GL_CONTEXT_MAJOR_VERSION, 3)
        display.gl_set_attribute(GL_CONTEXT_MINOR_VERSION, 3)
        display.gl_set_attribute(GL_CONTEXT_PROFILE_MASK, GL_CONTEXT_PROFILE_CORE)
        display.gl_set_attribute(GL_DEPTH_SIZE, 24)
        display.set_mode(WINDOW_RESOLUTION, flags=OPENGL | DOUBLEBUF)
        event.set_grab(True)
        mouse.set_visible(False)
        mouse.set_pos(WINDOW_RESOLUTION.x * 0.5, WINDOW_RESOLUTION.y * 0.5)

        self.context = create_context()
        self.context.enable(flags=DEPTH_TEST | CULL_FACE | BLEND)
        self.context.gc_mode = 'auto'

        self.clock = time.Clock()
        self.delta_time = 0.0
        self.time = 0.0
        self.is_running = True
        
        self.on_init()
    
    def show_loading_screen(self) -> None:
        self.context.clear(color=BACKGROUND_COLOR)
        display.flip()
    
    def on_init(self) -> None:
        self.show_loading_screen()
        
        self.textures = Textures(self)
        self.player = Player(self)
        self.inventory = Inventory(self)
        self.shader = Shader(self)
        self.scene = Scene(self)
        self.event_handler = EventHandler(self)
        self.mixer = Mixer()
        
        self.player.init_player(self.scene.world)
    
    def update(self) -> None:
        self.player.update()
        self.shader.update()
        self.scene.update()
        
        self.delta_time = self.clock.tick()
        self.time = time.get_ticks() * 0.001
        display.set_caption(f'MyCraft - {self.clock.get_fps():.0f}fps')
    
    def render(self) -> None:
        self.context.clear(color=BACKGROUND_COLOR)
        self.scene.render()
        display.flip()
    
    def handle_events(self) -> None:
        for e in event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                self.is_running = False
            self.event_handler.handle_events(e)
    
    def run(self) -> None:
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            self.mixer.play_soundtrack()
        quit()
        exit()
    
if __name__ == '__main__':
    game = Engine()
    game.run()
