from . import const


class Card():

    def __init__(self, suits: const.SUITS, num: int):
        self.suits = suits
        self.num = num