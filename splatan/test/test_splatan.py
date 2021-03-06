from splatan.main.Splatan import Splatan
from splatan.main.enums.GameState import GameState
from splatan.main.enums.Settlements import Settlements
from splatan.main.enums.TerrainSampler import TerrainTypes
from splatan.main.Tile import Tile
from splatan.main.errors import EnrollmentNotOpenError


from pytest import raises


def test_host_can_enroll_in_settings_state():
    splatan = Splatan("Jim")

    assert len(splatan.players) == 1
    assert splatan.state == GameState.SETTINGS


def test_players_can_not_enroll_before_settings():
    splatan = Splatan("jim")

    with raises(EnrollmentNotOpenError):
        splatan.enroll_player("Jimmy")


def test_game_state_is_player_enrolment_after_settings():
    splatan, _ = host_settings_and_enroll()

    assert splatan.state == GameState.PLAYER_ENROLLMENT


def test_players_can_enroll_after_settings():
    splatan, _ = host_settings_and_enroll()

    assert len(splatan.players) == 2


def test_game_state_changed_after_game_start():
    splatan, _, _ = host_settings_enroll_and_start_game()

    assert splatan.state == GameState.INITIAL_SETUP


def test_returns_error_if_non_host_tries_to_start_game():
    splatan, players = host_settings_and_enroll()

    players.get_current_player_and_increment()
    not_host = players.get_current_player()

    with raises(ValueError):
        splatan.start_game(not_host.name)


def test_starting_player_can_build_settlements_and_roads():
    splatan, players, starting_player_name = host_settings_enroll_and_start_game()

    splatan.build_initial_settlement_and_road(starting_player_name, 'location', Settlements.TOWN, 'some other location')
    assert True


def test_non_starting_player_can_not_build_settlements():
    splatan, players, _ = host_settings_enroll_and_start_game()

    players.get_current_player_and_increment()
    non_starting_player = players.get_current_player_and_increment()

    with raises(ValueError):
        splatan.build_initial_settlement_and_road(non_starting_player.name, 'location', Settlements.TOWN, 'some other location')


def test_check_initial_setup_returns_false_if_not_all_players_gone_twice():
    splatan, players, starting_player_name = host_settings_enroll_and_start_game()

    splatan.build_initial_settlement_and_road(starting_player_name, 'location', Settlements.TOWN, 'some other location')
    assert not splatan.check_initial_setup_complete()


def test_check_initial_setup_returns_true_once_all_players_gone_twice():
    splatan, players, starting_player_name = host_settings_enroll_and_start_game()

    build_initial_settlements(splatan, starting_player_name)

    assert splatan.check_initial_setup_complete()


def test_players_get_initial_resources_after_setup_complete():
    splatan, players, player_name = host_settings_enroll_start_game_setup()
    player = players.get_player_by_name(player_name)

    # TODO: this is a really bad way to do this
    assert len(player.cards) > 0


def test_player_gets_resources_on_roll():
    splatan, players, player_name = host_settings_enroll_start_game_setup()

    # hacky stuff - "replace" tile 14 with one that is guaranteed to roll on a 4
    # which we know the player is on
    test_tile = Tile(14, TerrainTypes.ORE, 4)
    splatan.board.tiles.add_tile(test_tile)

    splatan.roll_number = 4
    splatan.distribute_resources()
    player = players.get_player_by_name(player_name)

    assert len(player.cards) > 3


def test_next_player_turn_on_turn_end():
    splatan, players, player_name = host_settings_enroll_start_game_setup()

    splatan.roll()
    splatan.distribute_resources()

    old_player = players.get_player_by_name(player_name)
    player_name = splatan.end_turn(player_name)
    player = players.get_player_by_name(player_name)

    assert old_player != player


def build_initial_settlements(splatan, player_name: str) -> str:
    _, player_name = splatan.build_initial_settlement_and_road(player_name, '1.2.?', Settlements.TOWN, '1.2.5')
    _, player_name = splatan.build_initial_settlement_and_road(player_name, '4.5.9', Settlements.TOWN, '5.9.10')
    _, player_name = splatan.build_initial_settlement_and_road(player_name, '13.14.17', Settlements.TOWN, '9.13.14')
    _, player_name = splatan.build_initial_settlement_and_road(player_name, '11.15.16', Settlements.TOWN, '11.12.16')
    return player_name


def host_settings_and_enroll():
    splatan = Splatan("jim")
    splatan.settings()
    players = splatan.enroll_player("Jimmy")
    return splatan, players


def host_settings_enroll_and_start_game():
    splatan, players = host_settings_and_enroll()
    host = players.get_current_player()
    starting_player_name = splatan.start_game(host.name)
    return splatan, players, starting_player_name


def host_settings_enroll_start_game_setup():
    splatan, players, starting_player_name = host_settings_enroll_and_start_game()

    player_name = build_initial_settlements(splatan, starting_player_name)
    splatan.check_initial_setup_complete()

    return splatan, players, player_name
