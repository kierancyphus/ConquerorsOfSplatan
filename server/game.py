from fastapi import APIRouter, Depends, HTTPException
from server.types.enroll_player import EnrollPlayerRequest, EnrollPlayerResponse
from server.types.settings import SettingsResponse, SettingsRequest
from server.GameManager import GameManager, game_manager_provider
from splatan import PlayerExistsError, EnrollmentNotOpenError

router = APIRouter()


# @router.post("/settings", response_model=SettingsResponse)
# async def settings(game_id: str, request: EnrollPlayerRequest, game_manager: GameManager = Depends(game_manager_provider)):
#     # TODO: currently doesn't do anything because I dont have any settings
#     game = game_manager.get_game(game_id)
#     print(f"made it to game: {game_id}")
#     game.settings()
#     return SettingsResponse()


@router.post("/enroll_player", response_model=EnrollPlayerResponse)
async def enroll_player(game_id: str, request: EnrollPlayerRequest, game_manager: GameManager = Depends(game_manager_provider)):
    game = game_manager.get_game(game_id)

    try:
        players = game.enroll_player(request.name)
    except PlayerExistsError:
        raise HTTPException(status_code=400, detail=f"Player with name {request.name} already exists")
    except EnrollmentNotOpenError:
        raise HTTPException(status_code=400, detail="Enrollment is currently closed")

    other_players = [player_name for player_name in players.get_all_players_names() if player_name != request.name]
    return EnrollPlayerResponse(name=request.name, other_players=other_players)