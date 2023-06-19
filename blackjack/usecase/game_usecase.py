from blackjack.domain.event import DomainEvent
from blackjack.domain.game import Game
from blackjack.repository.game_repository import GameRepository

from . import Presenter

game_repo = GameRepository.make('mem')
repo_err = 'game id is unavaliable'


class CreateGame():

    class Input():

        def __init__(self, player_id: str) -> None:
            self.player_id = player_id

    def execute(self, req: Input, presenter: Presenter) -> Presenter:
        game = Game(req.player_id)
        game_id = game_repo.save(game)
        game.game_id = game_id
        events = game.join(req.player_id)
        presenter.present(events)
        return presenter


class JoinGame():

    class Input():

        def __init__(self, game_id: str, player_id: str):
            self.game_id = game_id
            self.player_id = player_id

    def execute(self, req: Input, presnter: Presenter) -> Presenter:
        game = game_repo.get(req.game_id)
        if game is None:
            events = [DomainEvent(err=repo_err)]
        else:
            events = game.join(req.player_id)
        presnter.present(events)
        return presnter


class StartGame():

    class Input():

        def __init__(self, game_id: str, player_id: str):
            self.game_id = game_id
            self.player_id = player_id

    def execute(self, req: Input, presenter: Presenter) -> Presenter:
        game = game_repo.get(req.game_id)
        if game is None:
            events = [DomainEvent(err=repo_err)]
        else:
            events = game.start(req.player_id)
        presenter.present(events)
        return presenter


class PlayPass():

    class Input():

        def __init__(self, game_id: str, player_id: str):
            self.game_id = game_id
            self.player_id = player_id

    def execute(self, req: Input, presenter: Presenter) -> Presenter:
        game = game_repo.get(req.game_id)
        if game is None:
            events = [DomainEvent(err=repo_err)]
        else:
            events = game.play_pass(req.player_id)
        presenter.present(events)
        return presenter


class GameStatus():

    class Input():

        def __init__(self, game_id: str, player_id: str):
            self.game_id = game_id
            self.player_id = player_id

    def execute(self, req: Input, presenter: Presenter) -> Presenter:

        game = game_repo.get(req.game_id)
        if game is None:
            events = [DomainEvent(err=repo_err)]
        else:
            events = game.status(req.player_id)
        presenter.present(events)
        return presenter
