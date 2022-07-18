from fastapi import FastAPI, Depends
from server.types.create_game import CreateGameResponse, CreateGameRequest
from server.GameManager import game_manager_provider, GameManager

import server.game as game


app = FastAPI()
app.include_router(
    game.router,
    prefix="/game/{game_id}"
)


@app.get("/")
async def root():
    return {"message": "I hope this is working"}


@app.post("/create-game", response_model=CreateGameResponse)
async def create_game(request: CreateGameRequest, game_manager: GameManager = Depends(game_manager_provider)):
    game_id = game_manager.add_game(request.host_name)

    return CreateGameResponse(host_name=request.host_name, game_id=game_id)

