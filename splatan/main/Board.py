from splatan.main.Tile import Tile
from splatan.main.Dice import Dice
import splatan.main.Vertices as Vertices
from splatan.main.Tiles import Tiles
from splatan.main.enums.Settlements import Settlements
from splatan.main.Vertex import Vertex
from splatan.main.enums.TerrainSampler import TerrainTypes

from typing import List, Dict
from collections import defaultdict


class Board:
    def __init__(self, dice: Dice) -> None:
        self.num_tiles = 19
        self.dice = dice
        self.vertices = Vertices.Vertices()
        self.tiles = Tiles(self.num_tiles, self.dice)

    def get_rolled_tiles(self, roll: int) -> List[Tile]:
        return self.tiles.tiles_for_roll(roll)

    def build_settlement(self, name: str, settlement: Settlements) -> Vertex:
        return self.vertices.build_settlement(name, settlement)

    def build_road(self, start: str, end: str) -> None:
        self.vertices.build_road(start, end)

    def get_resources_for_tile_ids(self, tile_ids: List[str]) -> Dict[TerrainTypes, int]:
        resources = defaultdict(int)
        for tile_id in tile_ids:
            tile = self.tiles.get_tile_by_id(int(tile_id))
            resources[tile.terrain] += 1

        return resources

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



