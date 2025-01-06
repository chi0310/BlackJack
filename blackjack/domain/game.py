from typing import Mapping, Optional, Tuple

from . import const, event
from .player import Player
from .dealer import Dealer
from .errors import GameError


class Game():

    def __init__(self) -> None:
        self.game_id = None
        self._players: Mapping[str, 'Player'] = {}
        self._dealer = Dealer()
        self._deck = None

        self._status = const.GAME.CREATE

    @classmethod
    def create(cls) -> 'Game':
        return cls()

    def join(self, player_id: str):
        if len(self._players) >= 4:
            err = GameError.GAME_FULL
            res = event.ActionEvent(action=const.GAME.JOIN,
                                    player_id=player_id,
                                    game_id=self.game_id,
                                    err=err)
            return [res]
        player = Player(player_id, self._dealer, 0)
        self._players[player_id] = player
        if len(self._players) == 1:
            self.head_id = player_id
            res = event.ActionEvent(action=const.GAME.CREATE,
                                    player_id=player_id,
                                    game_id=self.game_id)
        else:
            res = event.ActionEvent(action=const.GAME.JOIN,
                                    player_id=player_id,
                                    game_id=self.game_id)
        return [res]

    def start(self, player_id):
        if self.head_id != player_id:
            err = GameError.NOT_HEAD_OF_GAME
            res = event.ActionEvent(action=const.GAME.START,
                                    player_id=player_id,
                                    game_id=self.game_id,
                                    err=err)
            return [res]
        if len(self._players) == 4:
            self._status = const.GAME.START
            err = None
        else:
            err = GameError.NOT_ENOUGH_PLAYERS
        res = event.ActionEvent(action=const.GAME.START,
                                player_id=player_id,
                                game_id=self.game_id,
                                err=err)
        return [res]

    def _validate_player_action(self, player_id: str) -> Tuple[Optional[Player], Optional[int]]:
        if self._status != const.GAME.START:
            return None, GameError.GAME_NOT_STARTED
        player = self._players.get(player_id)
        if player is None:
            return None, GameError.INVALID_PLAYER_ID
        return player, None

    def play_hit(self, player_id):
        player, err = self._validate_player_action(player_id)
        if err is not None:
            res = event.ActionEvent(action=const.GAME.PLAYING,
                                    player_id=player_id,
                                    game_id=self.game_id,
                                    err=err)
            return [res]
        err = player.hit()
        self.update_status()
        res = event.ActionEvent(action=const.GAME.PLAYING,
                                player_id=player_id,
                                game_id=self.game_id,
                                err=err)
        return [res]

    def play_stand(self, player_id):
        player, err = self._validate_player_action(player_id)
        if err is not None:
            res = event.ActionEvent(action=const.GAME.PLAYING,
                                player_id=player_id,
                                game_id=self.game_id,
                                err=err)
            return [res]
        err = player.stand()
        self.update_status()
        res = event.ActionEvent(action=const.GAME.PLAYING,
                                player_id=player_id,
                                game_id=self.game_id,
                                err=err)
        return [res]

    def play_double(self, player_id):
        player, err = self._validate_player_action(player_id)
        if err is not None:
            res = event.ActionEvent(action=const.GAME.PLAYING,
                                player_id=player_id,
                                game_id=self.game_id,
                                err=err)
            return [res]
        err = player.double()
        self.update_status()
        res = event.ActionEvent(action=const.GAME.PLAYING,
                                player_id=player_id,
                                game_id=self.game_id,
                                err=err)
        return [res]

    def update_status(self):
        ret = True
        for p in self._players.values():
            if p.state != const.PLAYER.FINISHED:
                ret = False
        if ret:
            self._status = const.GAME.END
        return ret

    def status(self, player_id: str) -> event.DomainEvent:
        # TODO
        # make different event according to player_id
        return [event.StatusEvent(status=self._status.name)]
