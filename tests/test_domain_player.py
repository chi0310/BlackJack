import unittest
import pytest

from blackjack.domain.player import (
    Player, PlayingState, BustedState, FinishedState,
    stateins2const
)
from blackjack.domain.deck import Card

class DummyDealer():
    def set_deal(self, num: int):
        self._deal_card = Card(suit=0, num=num)
    
    def deal(self):
        return self._deal_card
    
    def double_bets_from_player(self):
        return None


class TestDomainDeck(unittest.TestCase):

    def setUp(self):
        self.game_id = 'dummy_game_id'
    
    def test_draw_card(self):
        dealer = DummyDealer()
        player = Player(
            self.game_id,
            dealer,
            100
        )
        dealer.set_deal(1)
        for i in range(5):
            player.draw_card()
            self.assertEqual(
                len(player._cards),
                i+1
            )

    def test_calculate_score(self):
        dealer = DummyDealer()
        player = Player(
            self.game_id,
            dealer,
            100
        )
        nums = [11, 12 ,13]
        for num in nums:
            dealer.set_deal(num)
            player.draw_card()
        self.assertEqual(
            player.calculate_score(),
            30
        )

        nums = [11, 12 ,1]
        player.reset_cards()
        for num in nums:
            dealer.set_deal(num)
            player.draw_card()
        self.assertEqual(
            player.calculate_score(),
            21
        )

    def test_hit_playingstate(self):
        dealer = DummyDealer()
        player = Player(
            self.game_id,
            dealer,
            100
        )
        nums = [11, 8, 3]
        for num in nums:
            dealer.set_deal(num)
            player.hit()
            self.assertEqual(
                player.state,
                stateins2const(PlayingState())
            )

    def test_hit_bustedstate(self):
        dealer = DummyDealer()
        player = Player(
            self.game_id,
            dealer,
            100
        )
        nums = [11, 8, 4]
        for i, num in enumerate(nums):
            dealer.set_deal(num)
            player.hit()
            if i in [0, 1]:
                self.assertEqual(
                    player.state,
                    stateins2const(PlayingState())
                )
            else:
                self.assertEqual(
                    player.state,
                    stateins2const(BustedState())
                )

    def test_hit_finishedstate(self):
        dealer = DummyDealer()
        player = Player(
            self.game_id,
            dealer,
            100
        )
        nums = [11, 8]
        for i, num in enumerate(nums):
            dealer.set_deal(num)
            player.hit()
            if i in [0, 1]:
                self.assertEqual(
                    player.state,
                    stateins2const(PlayingState())
                )
        player.stand()
        self.assertEqual(
            player.state,
            stateins2const(FinishedState())
        )

    def test_double_playingstate(self):
        dealer = DummyDealer()
        player = Player(
            self.game_id,
            dealer,
            100
        )
        dealer.set_deal(1)
        player.hit()

        dealer.set_deal(2)
        player.double()

        self.assertEqual(
            player.state,
            stateins2const(FinishedState())
        )

    def test_double_bustedstate(self):
        dealer = DummyDealer()
        player = Player(
            self.game_id,
            dealer,
            100
        )

        dealer.set_deal(11)
        player.hit()
        player.hit()

        dealer.set_deal(11)
        player.double()

        self.assertEqual(
            player.state,
            stateins2const(BustedState())
        )