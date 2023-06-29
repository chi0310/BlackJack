import random
from . import const
from .card import Card


class Deck():
    def __init__(self) -> None:
        self._cards = []
        for suit in const.SUITS:
            for num in range(1, 14, 1):
                self._cards.append([suit, num])

        self._sequence = None

    def pick(self):
        card_arg = self._cards[self._sequence.pop() % 52] 
        suit = card_arg[0]
        num = card_arg[1]
        return Card(suit, num)

    def shuffle(self):
        # TODO this method is slow [ref](https://stackoverflow.com/a/9755548)
        self._sequence = random.sample(range(52*4), 52*4) 