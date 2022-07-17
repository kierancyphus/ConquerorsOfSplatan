from splatan.enums.TerrainSampler import TerrainTypes

from typing import Dict
from collections import defaultdict


class Cards:
    def __init__(self) -> None:
        self.cards: Dict[TerrainTypes, int] = defaultdict(int)

    def add_card(self, terrain_type: TerrainTypes) -> None:
        self.cards[terrain_type] += 1

    def add_cards(self, terrain_type: TerrainTypes, amount: int) -> None:
        self.cards[terrain_type] += amount

    def __str__(self) -> str:
        return str(dict(self.cards))

    def __len__(self) -> int:
        return sum(self.cards.values())
