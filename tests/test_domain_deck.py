import unittest
import pytest

from fastapi.testclient import TestClient

from blackjack.domain.deck import Deck, Card
import blackjack.domain.exception as excp

def _format_card(card: Card) -> tuple[int, int]:
    return (card.suit, card.num)

class TestDomainDeck(unittest.TestCase):

    def setUp(self) -> None:
        self.deck = Deck()

    def test_pick_out_of_range(self):
        for i in range(52):
            self.deck.pick()

        self.assertEqual(False, self.deck.is_valid())

        with pytest.raises(excp.DeckOutOfRangeError):
            self.deck.pick()

    def test_pick_no_duplicate(self):
        memo = set()
        for i in range(52):
            card = self.deck.pick()
            info = _format_card(card)
            self.assertEqual(
                True, info not in memo
            )
            memo.add(info)

