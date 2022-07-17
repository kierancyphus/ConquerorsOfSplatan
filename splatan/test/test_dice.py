from splatan.main.Dice import Dice


def test_dice_roll_returns_valid_number():
    dice = Dice(sides=6)
    assert dice.roll() in range(13)
