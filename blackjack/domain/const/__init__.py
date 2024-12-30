from enum import Enum


class PLAYER(Enum):
    INIT = 0
    PLAYING = 1
    FINISHED = 2
    BUSTED = 3


class GAME(Enum):
    CREATE = 0
    START = 1
    JOIN = 2
    PLAYING = 3
    END = 4


class SUITS(Enum):
    SPADES = 0
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3