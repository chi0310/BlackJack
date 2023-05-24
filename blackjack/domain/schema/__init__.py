from pydantic import BaseModel

class GameStatus(BaseModel):
    game_id: str
    state: int