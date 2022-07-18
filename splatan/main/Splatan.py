from splatan.main.Board import Board
from splatan.main.Players import Players
import splatan.main.Player as Player
from splatan.main.enums.GameState import GameState
from splatan.main.Dice import Dice
from splatan.main.enums.Settlements import Settlements
from splatan.main.errors import EnrollmentNotOpenError, NotHostError

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
        self.players.add_player(host_name)
        self.host = self.players.get_player_by_name(host_name)

    def settings(self) -> None:
        # doesn't do anything for now, but will eventually let you choose how many pieces you want and stuff
        self.state = GameState.PLAYER_ENROLLMENT

    def enroll_player(self, name: str) -> Players:
        """
        Add a player to the game

        Raises ValueError if the name is already taken.
        Raises ValueError if the gamestate is not enrollment
        :param name: name of the player trying to enroll
        :return:
        """
        if self.state != GameState.PLAYER_ENROLLMENT:
            raise EnrollmentNotOpenError('Error: Enrollment is not currently open.')

        self.players.add_player(name)
        return self.players

    def start_game(self, player_name: str) -> str:
        """
        A player attempts to close enrollment and start the game. If someone other than the host
        attempts to start the game, it raises a ValueError.
        :param player_name: name of player making the request. Must be the host
        :return: the first player to go
        """
        player = self.players.get_player_by_name(player_name)

        if player != self.host:
            raise NotHostError('Error: only the host can start the game')

        # TODO: Ideally I store the enum in an object and expose a `next_game_state` method
        self.state = GameState.INITIAL_SETUP

        starting_player = self.players.choose_starting_player()
        return starting_player.name

    def build_initial_settlement_and_road(self, player_name: str, location: str, settlement: Settlements,
                                          road_end: str) -> Tuple[Board, str]:
        """
        builds initial settlement, increments the player turn and returns the board state and the next player to go
        :param road_end:
        :param player:
        :param location:
        :param settlement:
        :return: Board state and the next player to go
        """
        player = self.players.get_player_by_name(player_name)

        self.check_turn(player)

        built_settlement = self.board.build_settlement(location, settlement)
        player.save_settlement(built_settlement)

        self.board.build_road(location, road_end)
        next_turn_player = self.players.next_turn_player()

        return self.board, next_turn_player.name

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

    def end_turn(self, player_name: str) -> str:
        player = self.players.get_player_by_name(player_name)
        self.check_turn(player)
        next_player = self.players.next_turn_player()
        return next_player.name

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
