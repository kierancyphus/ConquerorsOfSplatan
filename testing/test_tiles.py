from splatan.Dice import Dice
from splatan.Tiles import Tiles
from splatan.Tile import Tile, TerrainTypes

num_tiles = 19
dice = Dice()


def test_tiles_not_empty_on_initialize():
    tiles = Tiles(num_tiles, dice)
    assert len(tiles.roll_to_tile) > 0
    assert len(tiles.tiles) > 0


def test_tiles_returns_correct_tiles_on_roll():
    roll = 5
    fake_roll_to_tile = {
        1: [],
        2: [],
        5: [Tile(1, TerrainTypes.ORE, 5), Tile(2, TerrainTypes.WOOD, 5)]
    }

    tiles = Tiles(num_tiles, dice)
    tiles.roll_to_tile = fake_roll_to_tile

    assert tiles.tiles_for_roll(roll) == fake_roll_to_tile[roll]