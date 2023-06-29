import unittest

from fastapi import status
from fastapi.testclient import TestClient

from blackjack.domain.deck import Deck
from blackjack.domain.const import SUITS


class TestDomainDeck(unittest.TestCase):

    def setUp(self) -> None:
        self.deck = Deck()

    def test_domain_deck(self):
        self.deck.shuffle()

        self.assertEqual(52, len(self.deck._cards))
        self.assertEqual(52*4, len(self.deck._sequence))

        nums = 0
        suitss = 0
        count = 0
        for _ in range(len(self.deck._sequence)):
            count += 1
            card = self.deck.pick()
            nums += card.num
            suitss += card.suits.value

        self.assertEqual(52*4, count)
        self.assertEqual((0+3) * 4 / 2 * 13 * 4, suitss)
        self.assertEqual((1+13) * 13 / 2 * 4 * 4, nums)
