from splatan.main.enums.TerrainSampler import TerrainTypes


class Tile:
    def __init__(self, id: int, terrain: TerrainTypes, roll_number: int) -> None:
        self.id = id
        self.terrain = terrain
        self.roll_number = roll_number

    def __str__(self) -> str:
        return f"<Tile: {self.id}, {self.terrain}, {self.roll_number}>"
