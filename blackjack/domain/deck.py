import random
from typing import List
from dataclasses import dataclass
import threading

import  blackjack.domain.exception as excp
from . import const

@dataclass
class Card:
    suit: str
    num: int


class Deck():
    def __init__(self) -> None:
        self._cards = []
        for suit in const.SUITS:
            for num in range(1, 14, 1):
                card = Card(suit=suit.value, num=num)
                self._cards.append(card)

        self._nums = len(self._cards)
        self._pick_lock = threading.Lock()
    
    def pick(self) -> Card:
        with self._pick_lock:
            if not self.is_valid():
                raise excp.DeckOutOfRangeError
            self._nums -= 1
            index = random.randint(0, self._nums)
            ret = self._cards[index]
            self._cards[index] = self._cards[self._nums]
            return ret
    
    def is_valid(self) -> bool:
        return self._nums > 0
