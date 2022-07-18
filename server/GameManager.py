from splatan import Splatan

from uuid import uuid4
from typing import Dict


class GameManager:
    def __init__(self):
        self.game_id_to_game: Dict[str, Splatan] = {}

    def add_game(self, host_name: str) -> str:
        # don't bother checking for collisions
        game_id = str(uuid4())

        new_game = Splatan(host_name)
        self.game_id_to_game[game_id] = new_game
        return game_id

    def get_game(self, game_id: str) -> Splatan:
        return self.game_id_to_game[game_id]

    def number_of_active_games(self) -> int:
        return len(self.game_id_to_game)

    def nuke(self) -> None:
        self.game_id_to_game = {}


async def game_manager_provider():
    return GameManager()
