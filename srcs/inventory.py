from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Engine

class Inventory:
    def __init__(self, game: 'Engine') -> None:
        self.game = game
        self.player = game.player
        
        self.inventory = []
        self.inventory_size = 9
        self.selected_slot = 0
        self.selected_voxel = 0

        self.init_inventory()
    
    def init_inventory(self) -> None:
        self.inventory = [i for i in range(1, self.inventory_size + 1)]
