from enum import Enum, auto


class GameState(Enum):
    SETTINGS = auto()
    PLAYER_ENROLLMENT = auto()
    INITIAL_SETUP = auto()
    DISTRIBUTE_RESOURCES = auto()
    PLAYER_TURN = auto()
    END_GAME = auto()
