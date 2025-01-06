import unittest

from blackjack.domain.game import Game
from blackjack.domain.errors import GameError
from blackjack.domain.event import ActionEvent
from blackjack.domain import const


class TestDomainGame(unittest.TestCase):

    def setUp(self):
        self.game = Game.create()

    def test_create_game(self):
        game = Game.create()
        self.assertIsNotNone(game)
        self.assertIsInstance(game, Game)

    def test_join(self):
        res = self.game.join("player1")
        self.assertEqual(len(self.game._players), 1)
        self.assertIsInstance(res[0], ActionEvent)
        self.assertEqual(res[0].action, const.GAME.CREATE)

        res = self.game.join("player2")
        self.assertEqual(len(self.game._players), 2)
        self.assertIsInstance(res[0], ActionEvent)
        self.assertEqual(res[0].action, const.GAME.JOIN)

    def test_join_full(self):
        self.game.join("player1")
        self.game.join("player2")
        self.game.join("player3")
        self.game.join("player4")
        res = self.game.join("player5")
        self.assertEqual(len(self.game._players), 4)
        self.assertIsInstance(res[0], ActionEvent)
        self.assertEqual(res[0].err, GameError.GAME_FULL)

    def test_start(self):
        self.game.join("head_player")
        self.game.join("player2")
        self.game.join("player3")
        self.game.join("player4")
        res = self.game.start("head_player")
        self.assertEqual(self.game._status, const.GAME.START)
        self.assertIsInstance(res[0], ActionEvent)
        self.assertEqual(res[0].action, const.GAME.START)
        self.assertIsNone(res[0].err)

    def test_start_game_not_head(self):
        self.game.join("player1")
        self.game.join("player2")
        self.game.join("player3")
        self.game.join("player4")
        res = self.game.start("player2")
        self.assertNotEqual(self.game._status, const.GAME.START)
        self.assertIsInstance(res[0], ActionEvent)
        self.assertEqual(res[0].err, GameError.NOT_HEAD_OF_GAME)

    def test_start_game_not_enough_players(self):
        self.game.join("player1")
        self.game.join("player2")
        res = self.game.start("player1")
        self.assertNotEqual(self.game._status, const.GAME.START)
        self.assertIsInstance(res[0], ActionEvent)
        self.assertEqual(res[0].err, GameError.NOT_ENOUGH_PLAYERS)

    def test_play_hit(self):
        self.game.join("player1")
        self.game.join("player2")
        self.game.join("player3")
        self.game.join("player4")
        res = self.game.start("player1")
        self.assertEqual(res[0].err, None)

        res = self.game.play_hit("player1")
        self.assertIsInstance(res[0], ActionEvent)
        self.assertEqual(res[0].action, const.GAME.PLAYING)

    def test_play_stand(self):
        self.game.join("player1")
        self.game.join("player2")
        self.game.join("player3")
        self.game.join("player4")
        res = self.game.start("player1")
        self.assertEqual(res[0].err, None)

        res = self.game.play_stand("player1")
        self.assertIsInstance(res[0], ActionEvent)
        self.assertEqual(res[0].action, const.GAME.PLAYING)

    def test_play_double(self):
        self.game.join("player1")
        self.game.join("player2")
        self.game.join("player3")
        self.game.join("player4")
        res = self.game.start("player1")
        self.assertEqual(res[0].err, None)

        res = self.game.play_double("player1")
        self.assertIsInstance(res[0], ActionEvent)
        self.assertEqual(res[0].action, const.GAME.PLAYING)

    def test_update_status(self):
        self.game.join("player1")
        self.game.join("player2")
        self.game.join("player3")
        self.game.join("player4")
        res = self.game.start("player1")
        self.assertEqual(res[0].err, None)

        self.game.play_stand("player1")
        self.game.play_stand("player2")
        self.game.play_stand("player3")
        self.game.play_stand("player4")
        self.assertTrue(self.game.update_status())
        self.assertEqual(self.game._status, const.GAME.END)

    def test_validate_player_action_game_not_started(self):
        self.game.join("player1")
        player, err = self.game._validate_player_action("player1")
        self.assertIsNone(player)
        self.assertEqual(err, GameError.GAME_NOT_STARTED)

    def test_validate_player_action_invalid_player(self):
        self.game.join("player1")
        self.game.join("player2")
        self.game.join("player3")
        self.game.join("player4")
        res = self.game.start("player1")
        self.assertEqual(res[0].err, None)

        player, err = self.game._validate_player_action("invalid_player")
        self.assertIsNone(player)
        self.assertEqual(err, GameError.INVALID_PLAYER_ID)