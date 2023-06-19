from typing import Mapping

from . import const, event
from .player import Player


class Game():

    def __init__(self, head_id: str) -> None:
        self.head_id = head_id

        self.game_id = None
        self._players: Mapping[str, 'Player'] = {}
        self._dealer = None
        self._deck = None

        self._status = const.GAME.CREATE

    @classmethod
    def create(cls):
        return cls()

    def join(self, player_id: str):
        if len(self._players) >= 4:
            err = 'game is up to four players'
            res = event.ActionEvent(action=const.GAME.JOIN,
                                    player_id=player_id,
                                    game_id=self.game_id,
                                    err=err)
            return [res]
        player = Player(player_id)
        self._players[player_id] = player
        if len(self._players) == 1:
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
            err = 'not the head of the game'
        if len(self._players) == 4:
            self._status = const.GAME.START
            err = None
        else:
            err = 'not enough player'
        res = event.ActionEvent(action=const.GAME.START,
                                player_id=player_id,
                                game_id=self.game_id,
                                err=err)
        return [res]

    def play_pass(self, player_id):
        err = None
        if self._status != const.GAME.START:
            err = 'game is not ready'
        player = self._players.get(player_id)
        if player is None:
            err = f'no valid player_id {player_id}'
        player.play('pass')
        self.update_status()
        res = event.ActionEvent(action=const.GAME.PLAYING,
                                player_id=player_id,
                                game_id=self.game_id,
                                err=err)
        return [res]

    def update_status(self):
        ret = True
        for p in self._players.values():
            if p._status != const.PLAYER.PASS:
                ret = False
        if ret:
            self._status = const.GAME.END
        return ret

    def status(self, player_id: str) -> event.DomainEvent:
        # TODO
        # make different event according to player_id
        return [event.StatusEvent(status=self._status.name)]
