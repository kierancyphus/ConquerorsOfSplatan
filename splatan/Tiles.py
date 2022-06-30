from splatan.Tile import Tile
from splatan.enums.Terrains import Terrains
from splatan.Dice import Dice
from typing import List, Dict
from collections import defaultdict


class Tiles:
    def __init__(self, num_tiles: int, dice: Dice) -> None:
        self.num_tiles: int = num_tiles
        self.dice: Dice = dice
        self.tiles: List[Tile] = []
        self.roll_to_tile: Dict[int, List[Tile]] = defaultdict(list)

        self.initialize_tiles()

    def initialize_tiles(self):
        for tile_num in range(self.num_tiles):
            terrain, roll_number = Terrains.sample_terrain(), self.dice.roll()
            tile = Tile(tile_num, terrain, roll_number)
            self.tiles.append(tile)
            self.roll_to_tile[roll_number].append(tile)

    def tiles_for_roll(self, roll: int) -> List[Tile]:
        return self.roll_to_tile[roll]

    def format_tile_state(self) -> str:
        formatted = {k: [str(t) for t in v] for k, v in self.roll_to_tile.items()}
        return str(formatted)

    def __str__(self) -> str:
        return f"<Board>\n\t{self.format_tile_state()}\n</Board>"

