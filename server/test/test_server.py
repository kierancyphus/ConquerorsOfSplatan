from fastapi.testclient import TestClient
from pytest import fixture

from server.main import app
from server.GameManager import GameManager, game_manager_provider
from server.types.create_game import CreateGameRequest
from server.types.enroll_player import EnrollPlayerRequest


client = TestClient(app)
mock_game_manager = GameManager()


def inject_mock_game_manager():
    app.dependency_overrides[game_manager_provider] = lambda: mock_game_manager


inject_mock_game_manager()


@fixture(autouse=True)
def before_each():
    mock_game_manager.nuke()
    yield


def test_create_game():
    response = create_game()

    assert response.status_code == 200
    assert mock_game_manager.number_of_active_games() > 0


def test_create_multiple_games():
    create_game()
    response = create_game()

    assert response.status_code == 200
    assert mock_game_manager.number_of_active_games() > 1


# def test_enroll_player():
#     create_game_response = create_game()
#     game_id = create_game_response.json()["game_id"]
#     print(f"create game response: {create_game_response.json()}")
#     print(mock_game_manager.game_id_to_game)
#     request = EnrollPlayerRequest(name="Joe")
#     response = client.post(f"/game/{game_id}/enroll_player", json=dict(request))
#     print(response.json())
#     assert True
    # assert game_manager_provider.number_of_active_games() == 0


def create_game():
    create_game_request = CreateGameRequest(host_name="Jim")
    return client.post("/create-game", json=dict(create_game_request))
