from splatan.Vertex import Vertex
from splatan.Tile import Tile
from splatan.Cards import Cards
from splatan.enums.TerrainSampler import TerrainTypes

from typing import List, Dict


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.settlements: List[Vertex] = []
        # TODO change to own class
        self.roads: List[str] = []
        self.cards = Cards()

    def is_on_tile(self, tile: Tile) -> bool:
        # TODO: doesn't account for multiple on one tile (or even different values on tile)
        for settlement in self.settlements:
            if settlement.is_on_tile(tile.id):
                return True
        return False

    def is_at(self, vertex: Vertex) -> bool:
        return vertex in self.settlements

    def save_settlement(self, settlement: Vertex) -> None:
        self.settlements.append(settlement)

    def should_be_charged(self) -> bool:
        return len(self.settlements) >= 2

    def completed_initial_setup(self) -> bool:
        return self.should_be_charged()

    def receives_card(self, card: TerrainTypes) -> None:
        self.cards.add_card(card)

    def receives_cards(self, cards: Dict[TerrainTypes, int]) -> None:
        for terrain, amount in cards.items():
            self.cards.add_cards(terrain, amount)

    def get_last_settlement(self) -> Vertex:
        return self.settlements[-1]

    def __eq__(self, other) -> bool:
        if isinstance(other, Player):
            return other.name == self.name
        return False

    def __hash__(self) -> int:
        return hash(self.name)

    def __str__(self) -> str:
        return f"<Player: {self.name}, Cards: {self.cards}>"
