from typing import Optional, List, Set
from splatan.Settlements import Settlements


class Vertex:
    def __init__(self,
                 location: str,
                 ability: Optional[str] = None,
                 settlement: Optional[Settlements] = Settlements.NONE) -> None:
        """

        :param location: name of the junction on the board. Naming convention is tile numbers in ascending order. E.g. 1.2.3
        :param player: the player who owns the vertex
        :param ability: Whether or not the vertex is a port or something
        :param settlement: type of settlement
        """
        self.name = location
        self.ability = ability
        self.settlement = settlement
        self.neighbours: List['Vertex'] = []
        self.tile_ids: Set[str] = self.get_tiles(location)

    def __str__(self) -> str:
        return f"<Vertex {self.name}>"

    def build_road(self, to: 'Vertex') -> None:
        self.neighbours.append(to)

    def is_beside(self, other: 'Vertex') -> bool:
        """
        Determines if tiles are adjacent on the board.
        TODO: this is broken for edge tiles, but should be fixed by checking the length of the tile_ids
        :param other: tile to compare to
        :return: True if beside False otherwise
        """
        same_tiles = self.tile_ids.intersection(other.tile_ids)
        return len(same_tiles) == 2

    def get_tiles(self, location: str) -> Set[str]:
        return {tile for tile in location.split(".") if tile != "?"}
