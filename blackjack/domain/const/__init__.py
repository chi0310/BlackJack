from enum import Enum


class PLAYER(Enum):
    INIT = 'player init'
    PLAYING = 'player playing'
    BUSTED = 'player busted'
    FINISHED = 'player finished'


class GAME(Enum):
    CREATE = 'game create'
    START = 'game start'
    JOIN = 'game join'
    PLAYING = 'game playing'
    END = 'game end'


class SUITS(Enum):
    SPADES = 'spades'
    HEARTS = 'hearts'
    DIAMONDS = 'diamonds'
    CLUBS = 'clubs'