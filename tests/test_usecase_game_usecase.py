import unittest
from blackjack.usecase.game_usecase import (
    CreateGame, JoinGame, StartGame, PlayHit, PlayStand, PlayDouble, GameStatus
)
from blackjack.usecase import Presenter

class TestGameUsecase(unittest.TestCase):

    def setUp(self):
        self.presenter = Presenter()

    def test_create_game(self):
        usecase = CreateGame()
        req = CreateGame.Input(player_id="player1")
        presenter = usecase.execute(req, self.presenter)
        self.assertIsNotNone(presenter)

    def test_join_game(self):
        usecase = JoinGame()
        req = JoinGame.Input(game_id="game1", player_id="player2")
        presenter = usecase.execute(req, self.presenter)
        self.assertIsNotNone(presenter)

    def test_start_game(self):
        usecase = StartGame()
        req = StartGame.Input(game_id="game1", player_id="player1")
        presenter = usecase.execute(req, self.presenter)
        self.assertIsNotNone(presenter)

    def test_play_hit(self):
        usecase = PlayHit()
        req = PlayHit.Input(game_id="game1", player_id="player1")
        presenter = usecase.execute(req, self.presenter)
        self.assertIsNotNone(presenter)

    def test_play_stand(self):
        usecase = PlayStand()
        req = PlayStand.Input(game_id="game1", player_id="player1")
        presenter = usecase.execute(req, self.presenter)
        self.assertIsNotNone(presenter)

    def test_play_double(self):
        usecase = PlayDouble()
        req = PlayDouble.Input(game_id="game1", player_id="player1")
        presenter = usecase.execute(req, self.presenter)
        self.assertIsNotNone(presenter)

    def test_game_status(self):
        usecase = GameStatus()
        req = GameStatus.Input(game_id="game1", player_id="player1")
        presenter = usecase.execute(req, self.presenter)
        self.assertIsNotNone(presenter)
