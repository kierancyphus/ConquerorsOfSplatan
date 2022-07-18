from pydantic import BaseModel
from typing import List


class EnrollPlayerRequest(BaseModel):
    name: str


class EnrollPlayerResponse(BaseModel):
    name: str
    other_players: List[str]
