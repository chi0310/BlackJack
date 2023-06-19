from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from blackjack.domain import event
from blackjack.usecase import game_usecase

from .middleware.jwt import JWT

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@app.post('/game/create/by_player/{player_id}')
async def create_game(player_id: str, payload: dict = Depends(JWT())) -> dict:
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


@app.post('/game/{game_id}/status', response_model=event.GameStatus)
async def game_status(game_id):
    response = game_usecase.status(game_id)
    return response


class Token(BaseModel):
    access_token: str
    token_type: str


@app.post('/token', response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != 'hh' or \
            form_data.password != 'hh1':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = JWT.create_access_token(
        data={'sub': f'{form_data.username}:blackjack'})
    return {'access_token': access_token, 'token_type': 'bearer'}
