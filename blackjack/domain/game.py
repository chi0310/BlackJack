from __future__ import annotations
from typing import Mapping, Optional, Tuple, List
import asyncio

from . import const, event
from .player import Player
from .dealer import Dealer
from .errors import GameError


class Game():

    def __init__(self) -> None:
        self.game_id = None
        self._players: Mapping[str, Player] = {}
        self._dealer = Dealer()
        self._deck = None

        self._event_log_q: Mapping[str, asyncio.Queue] = {}
        self._status = const.GAME.CREATE

    @classmethod
    def create(cls) -> Game:
        return cls()

    def join(self, player_id: str):
        if len(self._players) >= 4:
            err = GameError.GAME_FULL
            res = event.ActionEvent(action=const.GAME.JOIN.value,
                                    player_id=player_id,
                                    game_id=self.game_id,
                                    err=err)
            return [res]
        player = Player(player_id, self._dealer, 0)
        self._players[player_id] = player
        self._event_log_q[player_id] = asyncio.Queue()
        if len(self._players) == 1:
            self.head_id = player_id
            res = event.ActionEvent(action=const.GAME.CREATE.value,
                                    player_id=player_id,
                                    game_id=self.game_id)
        else:
            res = event.ActionEvent(action=const.GAME.JOIN.value,
                                    player_id=player_id,
                                    game_id=self.game_id)
        return [res]

    async def start(self, player_id):
        if self.head_id != player_id:
            err = GameError.NOT_HEAD_OF_GAME
            res = event.ActionEvent(action=const.GAME.START.value,
                                    player_id=player_id,
                                    game_id=self.game_id,
                                    err=err)
            return [res]
        if len(self._players) == 4:
            self._status = const.GAME.START
            err = None
        else:
            err = GameError.NOT_ENOUGH_PLAYERS
        res = event.ActionEvent(action=const.GAME.START.value,
                                player_id=player_id,
                                game_id=self.game_id,
                                err=err)
        print('start1')
        if err is None:
            self._init_log_q()
            self._init_deal()
            await self._update_status()
            print('start2')
        return [res]

    def _init_deal(self):
        for _ in range(2):
            for player in self._players.values():
                player.hit()
            
        self._dealer.hit()
        self._dealer.hit()

    def _init_log_q(self):
        for k in self._players.keys():
            self._event_log_q[k] = asyncio.Queue()

    def _validate_player_action(self, player_id: str) -> Tuple[Optional[Player], Optional[int]]:
        if self._status != const.GAME.START:
            return None, GameError.GAME_NOT_STARTED
        player = self._players.get(player_id)
        if player is None:
            return None, GameError.INVALID_PLAYER_ID
        return player, None

    async def play_hit(self, player_id):
        player, err = self._validate_player_action(player_id)
        if err is not None:
            res = event.ActionEvent(action=const.GAME.PLAYING.value,
                                    player_id=player_id,
                                    game_id=self.game_id,
                                    err=err)
            return [res]
        err = player.hit()
        await self._update_status()
        res = event.ActionEvent(action=const.GAME.PLAYING.value,
                                player_id=player_id,
                                game_id=self.game_id,
                                err=err)
        return [res]

    async def play_stand(self, player_id):
        player, err = self._validate_player_action(player_id)
        if err is not None:
            res = event.ActionEvent(action=const.GAME.PLAYING.value,
                                player_id=player_id,
                                game_id=self.game_id,
                                err=err)
            return [res]
        err = player.stand()
        await self._update_status()
        res = event.ActionEvent(action=const.GAME.PLAYING.value,
                                player_id=player_id,
                                game_id=self.game_id,
                                err=err)
        return [res]

    async def play_double(self, player_id):
        player, err = self._validate_player_action(player_id)
        if err is not None:
            res = event.ActionEvent(action=const.GAME.PLAYING.value,
                                player_id=player_id,
                                game_id=self.game_id,
                                err=err)
            return [res]
        err = player.double()
        await self._update_status()
        res = event.ActionEvent(action=const.GAME.PLAYING.value,
                                player_id=player_id,
                                game_id=self.game_id,
                                err=err)
        return [res]

    async def _update_status(self):
        """
        Updates the status of the game and logs the game events for each player.
        This method checks if all players have finished their turns. If all players
        have finished, it updates the game status to `const.GAME.END`. It then creates
        a `GameEvent` for each player, including masked events for other players, and
        puts the event in the player's event log queue.
        Returns:
            bool: True if all players have finished their turns, False otherwise.
        Note:
            self._status will only be const.GAME.END or const.GAME.START.
        """
        ret = True
        for _, v in self._players.items():
            if v.state != const.PLAYER.FINISHED:
                ret = False
        if ret:
            self._status = const.GAME.END

        dealer_event = self._dealer.to_dealer_event(is_calc_score=ret)
        ids = self._players.keys()
        for k, v in self._players.items():
            player_events: List[event.PlayerEvent] = []
            winners = []
            for id in ids:
                if id == k:
                    player_events.append(v.to_player_event(True))
                else:
                    p = self._players[id]
                    if ret:
                        pe = p.to_player_event(True)
                        player_events.append(pe)
                        if pe.final_score > dealer_event.final_score and \
                                pe.final_score <= 21:
                            winners.append(id)
                    else:
                        player_events.append(
                        event.mask_player_event(
                            p.to_player_event(False)
                        )
                    )

            game_event = event.GameEvent(
                status=self._status.value,
                dealer=dealer_event,
                players=player_events,
                winners=winners,
            )
            await self._event_log_q[k].put(game_event)
        return ret

    def status(self) -> event.DomainEvent:
        return [event.StatusEvent(status=self._status.value)]

    def settle(self):
        pass

    def get_event_log(self, player_id: str) -> asyncio.Queue:
        return self._event_log_q.get(player_id)
