from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from . import const
from .errors import PlayerError
from blackjack.domain.dealer import Dealer


class State(ABC):
    @abstractmethod
    def hit(self, player: Player) -> Optional[str]:
        pass

    @abstractmethod
    def stand(self, player: Player) -> Optional[str]:
        pass

    @abstractmethod
    def double(self, player: Player) -> Optional[str]:
        pass

class PlayingState(State):
    def hit(self, player):
        player.draw_card()
        if player.calculate_score() > 21:
            player._state = BustedState()
        return None

    def stand(self, player):
        player._state = FinishedState()
        return None

    def double(self, player):
        ret = player.double_bets()
        if ret is not None:
            return PlayerError.INSUFFICIENT_FUNDS
        self.hit(player)
        if isinstance(player._state, PlayingState):
            player._state = FinishedState()
        return None
    
class BustedState(State):
    def _busted(self):
        return PlayerError.PLAYER_BUSTED

    def hit(self, player):
        return self._busted

    def stand(self, player):
        return self._busted

    def double(self, player):
        return self._busted

class FinishedState(State):
    def _finished(self):
        return PlayerError.ROUND_FINISHED

    def hit(self, player):
        return self._finished

    def stand(self, player):
        return self._finished

    def double(self, player):
        return self._finished

def stateins2const(state: State) -> const.PLAYER:
    if isinstance(state, PlayingState):
        return const.PLAYER.PLAYING
    elif isinstance(state, FinishedState):
        return const.PLAYER.FINISHED
    elif isinstance(state, BustedState):
        return const.PLAYER.BUSTED
    else:
        raise ValueError

class Player():

    def __init__(self, game_id: str, dealer: Dealer, money: int) -> None:
        self.game_id = game_id
        self.dealer = dealer
        self._money = money

        self._state: State = PlayingState()
        self._cards = []

    def play(self, action: str):
        if action == 'pass':
            self._status = const.PLAYER.PASS

    def draw_card(self):
        card = self.dealer.deal()
        self._cards.append(card)

    def double_bets(self):
        ret = self.dealer.double_bets_from_player()
        if ret is None:
            return None
        else:
            # TODO: insufficient funds
            pass

    def reset_cards(self):
        self._cards = []

    def calculate_score(self) -> int:
        value = 0
        num_of_a = 0
        for c in self._cards:
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

    def hit(self):
        self._state.hit(self)

    def stand(self):
        self._state.stand(self)

    def double(self):
        self._state.double(self)

    @property
    def state(self):
        return stateins2const(self._state)
