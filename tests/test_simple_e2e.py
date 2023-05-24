import pytest
import unittest
from unittest import mock
from fastapi.testclient import TestClient

from blackjack.controller.app import app

class TestSimpleE2E(unittest.TestCase):
    def setUp(self) -> None:
        self.test_client = TestClient(app)

    def test_simple_path(self):
        players = ['p1', 'p2', 'p3', 'p4']

        game_id = self.test_client.post(
                    f'/game/create/by_player/{players[0]}').json()

        for p in players[1::]:
            success = self.test_client.post(
                        f'/game/{game_id}/join/{p}').json()
            self.assertEqual(success, True)

        success = self.test_client.post(
                    f'/game/{game_id}/start/by_player/{players[0]}').json()
        self.assertEqual(success, True)
        
        for p in players:
            reponse = self.test_client.post(f'/game/{game_id}/{p}/play/pass').json()

        reponse = self.test_client.post(f'/game/{game_id}/status').json()
        self.assertEqual({'game_id': mock.ANY, 'state': 2}, reponse)
