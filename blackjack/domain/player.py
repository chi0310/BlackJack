from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from .event import PlayerEvent
from . import const
from .utils import calculate_score
from .errors import PlayerError
from .dealer import Dealer


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
        return calculate_score(self._cards)

    def hit(self):
        self._state.hit(self)

    def stand(self):
        self._state.stand(self)

    def double(self):
        self._state.double(self)

    def to_player_event(self, is_calc_score: bool = False) -> PlayerEvent:
        return PlayerEvent(
            id=self.game_id,
            status=self.state.value,
            cards=[(c.suit, c.num) for c in self._cards],
            final_score=self.calculate_score() if is_calc_score else 0
        )

    @property
    def state(self):
        return stateins2const(self._state)
