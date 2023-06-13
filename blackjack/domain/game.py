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

        self._state = const.GAME.CREATE

    @classmethod
    def create(cls):
        return cls()

    def join(self, player_id: str):
        if len(self._players) >= 4:
            return False
        player = Player(player_id)
        self._players[player_id] = player
        if len(self._players) == 1:
            res = event.ActionEvent(action=const.GAME.CREATE,
                                    success=True,
                                    player_id=player_id,
                                    game_id=self.game_id)
        else:
            res = event.ActionEvent(action=const.GAME.JOIN,
                                    success=True,
                                    player_id=player_id,
                                    game_id=self.game_id)
        return [res]

    def start(self, player_id):
        if self.head_id != player_id:
            return False
        if len(self._players) == 4:
            self._state = const.GAME.START
            success = True
        else:
            success = False
        res = event.ActionEvent(action=const.GAME.START,
                                success=success,
                                player_id=player_id,
                                game_id=self.game_id)
        return [res]

    def play_pass(self, player_id):
        if self._state != const.GAME.START:
            return False
        player = self._players.get(player_id)
        if player is None:
            print(f'no valid player_id {player_id}')
            return False
        player.play('pass')
        self.update_state()
        res = event.ActionEvent(action=const.GAME.PLAYING,
                                success=True,
                                player_id=player_id,
                                game_id=self.game_id)
        return [res]

    def update_state(self):
        ret = True
        for p in self._players.values():
            if p._state != const.PLAYER.PASS:
                ret = False
        if ret:
            self._state = const.GAME.END
        return ret

    def status(self, player_id: str) -> event.DomainEvent:
        # TODO
        # make different event according to player_id
        return [event.StatusEvent(status=self._state.name)]
