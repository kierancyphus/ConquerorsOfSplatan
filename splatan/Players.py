import splatan.Player as Player
from typing import List
from random import randint


class Players:
    def __init__(self) -> None:
        self.current_player_index = 0
        self.num_players: int = 0
        self.players: List[Player] = []

    def add_player(self, player: Player) -> None:
        if player in self.players:
            raise ValueError(f"Error: player: {player.name} is already a player")

        self.players.append(player)
        self.num_players += 1

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def get_current_player_and_increment(self) -> Player:
        player = self.players[self.current_player_index]
        self.current_player_index = (self.current_player_index + 1) % self.num_players
        return player

    def choose_starting_player(self) -> Player:
        starting_player_index = randint(0, self.num_players - 1)
        self.current_player_index = starting_player_index
        return self.players[starting_player_index]

    def __str__(self) -> str:
        return f"<Players: {[str(p) for p in self.players]}>"

