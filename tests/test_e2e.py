import unittest
import json

from fastapi import status
from fastapi.testclient import TestClient

from blackjack.controller.app import app
from blackjack.domain.const import GAME
import pytest
# from async_asgi_testclient import TestClient as AsyncTestClient
import httpx


class TestE2E(unittest.TestCase):

    def setUp(self) -> None:
        self.test_client = TestClient(app)

    def test_full_game_flow(self):
        """
        Test the full game flow of a BlackJack game.
        This test simulates the entire lifecycle of a BlackJack game, including:
        1. Creating a game by the first player.
        2. Joining the game by the remaining players.
        3. Starting the game by the first player.
        4. Playing the 'stand' action for all players.
        5. Checking the game status via Server-Sent Events (SSE).
        The test ensures that:
        - The game is created successfully.
        - All players join the game successfully.
        - The game starts successfully.
        - Each player can perform the 'stand' action successfully.
        - The game status is correctly updated and received via SSE.
        """
        
        players = ['p1', 'p2', 'p3', 'p4']

        # Create game
        response = self.test_client.post(
            f'/api/v1/game/create/by_player/{players[0]}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        game_id = response.json()['game_id']

        # Join game
        for p in players[1:]:
            response = self.test_client.post(f'/api/v1/game/{game_id}/join/{p}')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Start game
        response = self.test_client.post(
            f'/api/v1/game/{game_id}/start/by_player/{players[0]}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        for p in players:
            response = self.test_client.post(
                f'/api/v1/game/{game_id}/{p}/play/stand')
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check game status via SSE
        with self.test_client.stream(
                'GET',
                f'/api/v1/game/{game_id}/{players[0]}/status',
                ) as response:
            print(response)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            for event in response.iter_lines():
                if 'data: ' not in event:
                    continue
                event = event.replace('data: ', '')
                ejson = json.loads(event)
                # data = ejson['data']
                self.assertIn(ejson['status'],
                                [GAME.START.value, GAME.END.value])
                if ejson['status'] == GAME.END.value:
                    break
