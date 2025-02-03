from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import StreamingResponse

from blackjack.domain import const
from blackjack.domain.event import event2json, event2dict
from blackjack.usecase import game_usecase as gu

from .presenter import *  # NOQA

app = FastAPI()
v1 = FastAPI()
app.mount('/api/v1', v1)


@v1.post('/game/create/by_player/{player_id}',
         response_model=CreateGamePresenter.Response,
         status_code=201)
async def create_game(player_id: str):
    presenter = gu.CreateGame().execute(gu.CreateGame.Input(player_id),
                                        CreateGamePresenter())
    ret = presenter.is_validate
    if ret is not None:
        raise HTTPException(status_code=404, detail=ret)
    return presenter.as_view_model()


@v1.post('/game/{game_id}/join/{player_id}',
         status_code=status.HTTP_204_NO_CONTENT)
async def join_game(game_id: str, player_id: str):
    presenter = gu.JoinGame().execute(gu.JoinGame.Input(game_id, player_id),
                                      JoinGamePresenter())
    ret = presenter.is_validate
    if ret is not None:
        raise HTTPException(status_code=404, detail=ret)
    return presenter.as_view_model()


@v1.post('/game/{game_id}/start/by_player/{player_id}',
         status_code=status.HTTP_204_NO_CONTENT)
async def start_game(game_id: str, player_id: str):
    presenter = await gu.StartGame().execute(gu.StartGame.Input(game_id, player_id),
                                       StartGamePresenter())
    ret = presenter.is_validate
    if ret is not None:
        raise HTTPException(status_code=404, detail=ret)
    return presenter.as_view_model()


@v1.post('/game/{game_id}/{player_id}/play/stand',
         status_code=status.HTTP_204_NO_CONTENT)
async def play_stand(game_id: str, player_id: str):
    presenter = await gu.PlayStand().execute(gu.PlayStand.Input(game_id, player_id),
                                      PlayGamePresenter())
    ret = presenter.is_validate
    if ret is not None:
        raise HTTPException(status_code=404, detail=ret)
    return presenter.as_view_model()


@v1.get('/game/{game_id}/{player_id}/status', status_code=status.HTTP_200_OK)
async def game_status(request: Request, game_id: str, player_id: str):
    async def event_generator():
        q = gu.GameStatus().execute(
            gu.GameStatus.Input(game_id, player_id))
        while True:
            if await request.is_disconnected():
                break
            ret = await q.get()
            yield f"data: {event2json(ret)}\n\n"
            if ret is None or ret.status == const.GAME.END.value:
                yield f"data: \n\n"
                return

    return StreamingResponse(
                event_generator(),
                media_type="text/event-stream"
            )
