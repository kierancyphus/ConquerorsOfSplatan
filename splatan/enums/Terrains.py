from enum import Enum, auto
from random import randint


class TerrainTypes(Enum):
    DESERT = auto()
    WOOD = auto()
    BRICK = auto()
    SHEEP = auto()
    ORE = auto()


class Terrains:
    @staticmethod
    def sample_terrain() -> TerrainTypes:
        terrains = list(TerrainTypes)
        return terrains[randint(0, len(terrains) - 1)]
