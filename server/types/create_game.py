from pydantic import BaseModel
from uuid import UUID

class CreateGameRequest(BaseModel):
    host_name: str


class CreateGameResponse(BaseModel):
    host_name: str
    game_id: UUID
