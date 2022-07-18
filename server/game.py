from fastapi import APIRouter, Depends, HTTPException
from server.types.enroll_player import EnrollPlayerRequest, EnrollPlayerResponse
from server.GameManager import GameManager, game_manager_provider

router = APIRouter()


@router.get("/")
async def test(game_id: str):
    return {"game_id": game_id}


@router.post("/enroll_player", response_model=EnrollPlayerResponse)
async def enroll_player(game_id: str, request: EnrollPlayerRequest, game_manager: GameManager = Depends(game_manager_provider)):
    game = game_manager.get_game(game_id)

    try:
        players = game.enroll_player(request.name)
        other_players = [player_name for player_name in players.get_all_players_names() if player_name != request.name]
        response = EnrollPlayerResponse(name=request.name, other_players=other_players)
    except ValueError:
        raise HTTPException(status_code=400)



    return response
