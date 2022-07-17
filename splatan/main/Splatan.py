from splatan.main.Board import Board
from splatan.main.Players import Players
import splatan.main.Player as Player
from splatan.main.enums.GameState import GameState
from splatan.main.Dice import Dice
from splatan.main.enums.Settlements import Settlements

from typing import Tuple


class Splatan:
    def __init__(self, host_name: str):
        self.num_players = 0
        self.dice = Dice()
        self.roll_number: int = 0
        self.board = Board(self.dice)
        self.players = Players(self.board)
        self.state: GameState = GameState.SETTINGS

        # enroll the host
        self.host = Player.Player(host_name)
        self.players.add_player(self.host)

    def settings(self) -> None:
        # doesn't do anything for now, but will eventually let you choose how many pieces you want and stuff
        self.state = GameState.PLAYER_ENROLLMENT
        pass

    def enroll_player(self, name: str) -> Players:
        """
        Add a player to the game

        Raises ValueError if the name is already taken.
        Raises ValueError if the gamestate is not enrollment
        :param name: name of the player trying to enroll
        :return:
        """
        if self.state != GameState.PLAYER_ENROLLMENT:
            raise ValueError('Error: Enrollment is not currently open.')

        new_player = Player.Player(name)
        self.players.add_player(new_player)
        return self.players

    def start_game(self, player: Player.Player) -> Player:
        """
        A player attempts to close enrollment and start the game. If someone other than the host
        attempts to start the game, it raises a ValueError.
        :param player: a player making the request. Must be the host
        :return: the first player to go
        """
        if player != self.host:
            raise ValueError('Error: only the host can start the game')

        # TODO: Ideally I store the enum in an object and expose a `next_game_state` method
        self.state = GameState.INITIAL_SETUP
        return self.players.choose_starting_player()

    def build_initial_settlement_and_road(self, player: Player.Player, location: str, settlement: Settlements,
                                          road_end: str) -> Tuple[Board, Player.Player]:
        """
        builds initial settlement, increments the player turn and returns the board state and the next player to go
        :param road_end:
        :param player:
        :param location:
        :param settlement:
        :return: Board state and the next player to go
        """
        self.check_turn(player)

        built_settlement = self.board.build_settlement(location, settlement)
        player.save_settlement(built_settlement)

        self.board.build_road(location, road_end)

        return self.board, self.players.next_turn_player()

    def check_initial_setup_complete(self) -> bool:
        """
        checks if the initial setup stage is complete and modified game state if so
        :return: True if all players have build two settlements and False otherwise
        """
        initial_setup_complete = self.players.all_players_completed_initial_setup()

        if initial_setup_complete:
            self.state = GameState.DISTRIBUTE_RESOURCES
            self.players.distribute_initial_resources()
            # distribute initial resources

        return initial_setup_complete

    def roll(self) -> int:
        self.roll_number = self.dice.roll()
        return self.roll_number

    def distribute_resources(self) -> Players:
        rolled_tiles = self.board.get_rolled_tiles(self.roll_number)
        self.players.distribute_resources(rolled_tiles)
        return self.players

    def build_settlement(self, player: Player.Player, location: str, settlement: Settlements) -> None:
        """

        :param player:
        :param location:
        :param settlement:
        :return:
        """
        self.check_turn(player)

        # player.charge(...)

        self.board.build_settlement(location, settlement)

    def build_road(self, player: Player.Player, start: str, end: str) -> None:
        self.check_turn(player)
        if player.should_be_charged():
            # if not player.can_afford(...):
            #     raise ValueError(f"Player {player} can't afford {settlement}")
            # player.charge(...)
            pass

        self.board.build_road(start, end)

    def end_turn(self, player: Player.Player) -> Player.Player:
        self.check_turn(player)
        return self.players.next_turn_player()

    def change_game_state(self, state: GameState) -> None:
        self.state = state

    def check_turn(self, player: Player.Player) -> None:
        if player != self.players.get_current_player():
            raise ValueError(f"Error: it is not {player.name}'s turn")

    def __str__(self) -> str:
        game = f"{self.players}\n"
        game += f"{self.board}\n"
        game += f"<State: {self.state}>"
        return game
