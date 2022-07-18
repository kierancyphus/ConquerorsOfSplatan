from splatan.main.Player import Player
import splatan.main.Tile as Tile
import splatan.main.Board as Board
from splatan.main.errors import PlayerExistsError, PlayerDoesNotExistError

from typing import List, Dict
from random import randint


class Players:
    def __init__(self, board: Board.Board) -> None:
        self.current_player_index = 0
        self.num_players: int = 0
        self.players: List[Player] = []
        self.name_to_player: Dict[str, Player] = {}

        self.board = board

    def add_player(self, player_name: str) -> None:
        player = Player(player_name)

        if player in self.players:
            raise PlayerExistsError(f"{player.name} is already a player")

        self.players.append(player)
        self.name_to_player[player_name] = player
        self.num_players += 1

    def get_player_by_name(self, name: str) -> Player:
        if name not in self.name_to_player:
            raise PlayerDoesNotExistError(f"Player {name} doesn't exist")
        return self.name_to_player[name]

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def get_current_player_and_increment(self) -> Player:
        player = self.get_current_player()
        self.current_player_index = self.get_next_player_index()
        return player

    def next_turn_player(self) -> Player:
        self.current_player_index = self.get_next_player_index()
        return self.get_current_player()

    def get_next_player_index(self) -> int:
        return (self.current_player_index + 1) % self.num_players

    def choose_starting_player(self) -> Player:
        starting_player_index = randint(0, self.num_players - 1)
        self.current_player_index = starting_player_index
        return self.players[starting_player_index]

    def all_players_completed_initial_setup(self) -> bool:
        for player in self.players:
            if not player.completed_initial_setup():
                return False

        return True

    def distribute_initial_resources(self) -> None:
        for player in self.players:
            last_settlement = player.get_last_settlement()
            tile_ids = last_settlement.get_tile_ids()
            resources = self.board.get_resources_for_tile_ids(tile_ids)
            player.receives_cards(resources)

    def distribute_resources(self, tiles: List[Tile.Tile]) -> None:
        for tile in tiles:
            for player in self.players:
                if player.is_on_tile(tile):
                    player.receives_card(tile.terrain)

    def get_all_players_names(self) -> List[str]:
        return [player.name for player in self.players]

    def __str__(self) -> str:
        return f"<Players: {[str(p) for p in self.players]}>"

    def __len__(self) -> int:
        return len(self.players)

