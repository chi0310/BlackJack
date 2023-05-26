from fastapi import FastAPI

from blackjack.domain import schema
from blackjack.usecase import game_usecase

app = FastAPI()


@app.post('/game/create/by_player/{player_id}')
async def create_game(player_id: str) -> str:
    game_id = game_usecase.create_game(player_id)
    return game_id


@app.post('/game/{game_id}/join/{player_id}')
async def join_game(game_id: str, player_id: str) -> bool:
    success = game_usecase.join_game(game_id, player_id)
    return success


@app.post('/game/{game_id}/start/by_player/{player_id}')
async def start_game(game_id: str, player_id: str) -> bool:
    success = game_usecase.start(game_id, player_id)
    return success


@app.post('/game/{game_id}/{player_id}/play/pass')
async def play_pass(game_id, player_id):
    success = game_usecase.playpass(game_id, player_id)
    return success


@app.post('/game/{game_id}/status', response_model=schema.GameStatus)
async def game_status(game_id):
    response = game_usecase.status(game_id)
    return response
