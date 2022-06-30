from random import randint
from typing import Optional


class Dice:
    def __init__(self, sides: Optional[int] = 6) -> None:
        self.sides = sides

    def roll(self) -> int:
        roll_one = randint(1, self.sides)
        roll_two = randint(1, self.sides)
        return roll_one + roll_two
