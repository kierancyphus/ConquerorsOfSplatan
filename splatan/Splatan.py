from splatan.Board import Board
from splatan.Players import Players
import splatan.Player as Player
from splatan.enums.GameState import GameState
from splatan.Dice import Dice
from splatan.Settlements import Settlements


class Splatan:
    def __init__(self, host_name: str):
        self.num_players = 0
        self.players = Players()
        self.dice = Dice()
        self.board = Board(self.dice)
        self.state: GameState = GameState.SETTINGS

        # enroll the host
        self.host = Player.Player(host_name, self.board)
        self.players.add_player(self.host)

    def settings(self) -> None:
        # doesn't do anything for now, but will eventually let you choose how many pieces you want and stuff
        self.state = GameState.PLAYER_ENROLLMENT
        pass

    def enroll_player(self, name: str) -> None:
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

    def build_settlement(self, player: Player.Player, location: str, settlement: Settlements) -> None:
        """

        :param player:
        :param location:
        :param settlement:
        :return:
        """
        self.check_turn(player)

        if player.should_be_charged():
            # if not player.can_afford(...):
            #     raise ValueError(f"Player {player} can't afford {settlement}")
            # player.charge(...)
            pass

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
        return self.players.get_current_player_and_increment()

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


if __name__ == "__main__":
    splatan = Splatan("Jose")
    print(splatan)
    splatan.enroll_player("Jim")
    print()
    print(splatan)
    splatan.enroll_player("Joe")
    print()
    print(splatan)





