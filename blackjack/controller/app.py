from fastapi import FastAPI

from blackjack.usecase import game_usecase as gu

from .presenter import *  # NOQA

app = FastAPI()


@app.post('/game/create/by_player/{player_id}',
          response_model=CreateGamePresenter.Response)
async def create_game(player_id: str):
    presenter = gu.CreateGame().execute(gu.CreateGame.Input(player_id),
                                        CreateGamePresenter())
    return presenter.as_view_model()


@app.post('/game/{game_id}/join/{player_id}',
          response_model=JoinGamePresenter.Response)
async def join_game(game_id: str, player_id: str):
    presenter = gu.JoinGame().execute(gu.JoinGame.Input(game_id, player_id),
                                      JoinGamePresenter())
    return presenter.as_view_model()


@app.post('/game/{game_id}/start/by_player/{player_id}',
          response_model=StartGamePresenter.Response)
async def start_game(game_id: str, player_id: str):
    presenter = gu.StartGame().execute(gu.StartGame.Input(game_id, player_id),
                                       StartGamePresenter())
    return presenter.as_view_model()


@app.post('/game/{game_id}/{player_id}/play/pass',
          response_model=PlayGamePresenter.Response)
async def play_pass(game_id, player_id):
    presenter = gu.PlayPass().execute(gu.PlayPass.Input(game_id, player_id),
                                      PlayGamePresenter())
    return presenter.as_view_model()


@app.get('/game/{game_id}/{player_id}/status',
         response_model=GameStatusPresenter.Response)
async def game_status(game_id: str, player_id: str):
    presenter = gu.GameStatus().execute(
        gu.GameStatus.Input(game_id, player_id), GameStatusPresenter())
    return presenter.as_view_model()
