from splatan.Tile import Tile
from splatan.Dice import Dice
import splatan.Vertices as Vertices
from splatan.Tiles import Tiles
from splatan.Settlements import Settlements

from typing import List


class Board:
    def __init__(self, dice: Dice) -> None:
        self.num_tiles = 19
        self.dice = dice
        self.vertices = Vertices.Vertices()
        self.tiles = Tiles(self.num_tiles, self.dice)

    def get_rolled_tiles(self, roll: int) -> List[Tile]:
        return self.tiles.tiles_for_roll(roll)

    def build_settlement(self, name: str, settlement: Settlements) -> None:
        self.vertices.build_settlement(name, settlement)
        pass

    def build_road(self, start: str, end: str) -> None:
        self.vertices.build_road(start, end)

    def __str__(self) -> str:
        return str(self.tiles)
    # def sample_terrain(self) -> str:
    #     return self.terrains[randint(0, len(self.terrains) - 1)]

    # def create_tiles(self) -> None:
    #     for tile_num in range(self.num_tiles):
    #         tile = Tile(tile_num, self.sample_terrain(), self.dice.roll())
    #         self.tiles.append(tile)

    # def initialize_board(self) -> None:
    #     self.create_tiles()



