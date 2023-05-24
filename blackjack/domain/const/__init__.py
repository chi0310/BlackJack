from enum import Enum

class PLAYER(Enum):
    INIT = 0
    PLAY = 1
    PASS = 2
    BUST = 3

class GAME(Enum):
    INIT = 0
    START = 1
    END = 2
