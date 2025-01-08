from typing import List

from .deck import Card

def calculate_score(cards: List[Card]) -> int:
    value = 0
    num_of_a = 0
    for c in cards:
        cnum = c.num
        if cnum in [11, 12, 13]:
            value += 10
        elif cnum == 1:
            num_of_a += 1
        else:
            value += cnum
    for _ in range(num_of_a):
        if value + 11 > 21:
            value += 1
        else:
            value += 11
    return value