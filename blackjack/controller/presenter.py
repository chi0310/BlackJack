from pydantic import BaseModel

from blackjack.usecase import Presenter

__all__ = [
    'CreateGamePresenter', 'JoinGamePresenter', 'GameStatusPresenter',
    'StartGamePresenter', 'PlayGamePresenter'
]


class CreateGamePresenter(Presenter):

    class Response(BaseModel):
        game_id: str

    def as_view_model(self):
        return self.Response(game_id=self.events[0].game_id)


class JoinGamePresenter(Presenter):

    class Response(BaseModel):
        success: bool

    def as_view_model(self):
        return self.Response(success=self.events[0].success)


class StartGamePresenter(Presenter):

    class Response(BaseModel):
        success: bool

    def as_view_model(self):
        return self.Response(success=self.events[0].success)


class PlayGamePresenter(Presenter):

    class Response(BaseModel):
        success: bool

    def as_view_model(self):
        return self.Response(success=self.events[0].success)


class GameStatusPresenter(Presenter):

    class Response(BaseModel):
        status: str

    def as_view_model(self):
        return self.Response(status=self.events[0].status)
