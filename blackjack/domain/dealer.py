from .utils import calculate_score
from .deck import Deck, Card
from . import event

class Dealer():
    def __init__(self) -> None:
        self.deck = Deck()
        self.cards = []

    def deal(self) -> Card:
        return self.deck.pick()

    def double_bets_from_player(self):
        return True

    def settle_bets(self):
        pass

    def hit(self):
        self.cards.append(self.deal())

    def draw_until_seventeen(self):
        while self.calculate_score() < 17:
            self.hit()

    def calculate_score(self) -> int:
        return calculate_score(self.cards)
    
    def to_dealer_event(self, is_calc_score: bool = False) -> event.DealerEvent:
        return event.DealerEvent(
            cards=[(c.suit, c.num) for c in self.cards],
            final_score=self.calculate_score() if is_calc_score else 0
        )
