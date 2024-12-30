from blackjack.domain.deck import Deck, Card

class Dealer():
    def __init__(self) -> None:
        self.deck = Deck()

    def deal(self) -> Card:
        return self.deck.pick()

    def double_bets_from_player(self):
        return True

    def settle_bets(self):
        pass

    def hit():
        pass 

    def draw():
        pass