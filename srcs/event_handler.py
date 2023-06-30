from typing import TYPE_CHECKING
from pygame import KEYDOWN, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9

if TYPE_CHECKING:
    from main import Engine

class EventHandler:
    def __init__(self, game: 'Engine') -> None:
        self.game = game
        self.player = game.player
        self.inventory = game.inventory
        
        self.ingame = True
        self.inventory_open = False
        self.pause = False
    
    def handle_key_events(self, key) -> None:
        if key == K_1 and not self.inventory_open:
            self.inventory.set_current_slot(0)
        elif key == K_2 and not self.inventory_open:
            self.inventory.set_current_slot(1)
        elif key == K_3 and not self.inventory_open:
            self.inventory.set_current_slot(2)
        elif key == K_4 and not self.inventory_open:
            self.inventory.set_current_slot(3)
        elif key == K_5 and not self.inventory_open:
            self.inventory.set_current_slot(4)
        elif key == K_6 and not self.inventory_open:
            self.inventory.set_current_slot(5)
        elif key == K_7 and not self.inventory_open:
            self.inventory.set_current_slot(6)
        elif key == K_8 and not self.inventory_open:
            self.inventory.set_current_slot(7)
        elif key == K_9 and not self.inventory_open:
            self.inventory.set_current_slot(8)
    
    def handle_events(self, event) -> None:
        if self.ingame and not self.pause:
            self.player.handle_mouse_events(event)
            key = event.key if event.type == KEYDOWN else None
            if key:
                self.handle_key_events(key)
