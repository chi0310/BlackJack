import unittest

from fastapi import status
from fastapi.testclient import TestClient

from blackjack.controller.app import app
from blackjack.domain.const import GAME


class TestSimpleE2E(unittest.TestCase):

    def setUp(self) -> None:
        self.test_client = TestClient(app)

    def test_simple_path(self):
        players = ['p1', 'p2', 'p3', 'p4']

        reponse = self.test_client.post(
            f'/api/v1/game/create/by_player/{players[0]}').json()

        game_id = reponse['game_id']

        for p in players[1::]:
            reponse = self.test_client.post(f'/api/v1/game/{game_id}/join/{p}')
            self.assertEqual(reponse.status_code, status.HTTP_204_NO_CONTENT)

        reponse = self.test_client.post(
            f'/api/v1/game/{game_id}/start/by_player/{players[0]}')
        self.assertEqual(reponse.status_code, status.HTTP_204_NO_CONTENT)

        reponse = self.test_client.get(
            f'/api/v1/game/{game_id}/p1/status').json()
        self.assertEqual({'status': GAME.START.name}, reponse)

        for p in players:
            reponse = self.test_client.post(
                f'/api/v1/game/{game_id}/{p}/play/pass')
            self.assertEqual(reponse.status_code, status.HTTP_204_NO_CONTENT)

        reponse = self.test_client.get(
            f'/api/v1/game/{game_id}/p1/status').json()
        self.assertEqual({'status': GAME.END.name}, reponse)
