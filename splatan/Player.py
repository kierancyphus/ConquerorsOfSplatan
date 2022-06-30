from typing import Dict, Set, List
from splatan.enums.Terrains import TerrainTypes
import splatan.Vertex as Vertex
import splatan.Board as Board


class Player:
    def __init__(self, name: str, board: Board.Board) -> None:
        self.name = name
        self.board = board
        self.settlements: Set[Vertex.Vertex] = set()
        # TODO change to own class
        self.roads: List[str] = []
        # TODO: change to own class
        self.cards: Dict[TerrainTypes, int] = {}

    def is_at(self, vertex: Vertex.Vertex) -> bool:
        return vertex in self.settlements



    def save_settlement(self, settlement: Vertex) -> None:
        self.settlements.add(settlement)

    def should_be_charged(self) -> bool:
        return len(self.settlements) < 2 and len(self.roads) < 2

    def __eq__(self, other) -> bool:
        if isinstance(other, Player):
            return other.name == self.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return f"<Player: {self.name}>"
