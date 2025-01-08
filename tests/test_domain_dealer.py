import unittest
from blackjack.domain.dealer import Dealer
from blackjack.domain.deck import Card

class TestDealer(unittest.TestCase):

    def setUp(self):
        self.dealer = Dealer()

    def test_deal(self):
        card = self.dealer.deal()
        self.assertIsInstance(card, Card)

    def test_hit(self):
        self.dealer.hit()
        self.assertEqual(len(self.dealer.cards), 1)

    def test_draw_until_seventeen(self):
        # Mock the deck to control the cards dealt
        self.dealer.deck.pick = lambda: Card('Hearts', 2)
        self.dealer.draw_until_seventeen()
        self.assertGreaterEqual(self.dealer.calculate_score(), 18)

    def test_calculate_score(self):
        self.dealer.cards = [Card('Hearts', 10), Card('Diamonds', 7)]
        score = self.dealer.calculate_score()
        self.assertEqual(score, 17)

if __name__ == '__main__':
    unittest.main()
