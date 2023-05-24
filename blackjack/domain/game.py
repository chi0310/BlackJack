from typing import Mapping

from . import const
from . import schema
from .player import Player

class Game():
    def __init__(self, head_id: str) -> None:
        self.head_id = head_id

        self.game_id = None
        self._players: Mapping[str, 'Player'] = {}
        self._dealer = None
        self._deck = None

        self._state = const.GAME.INIT

    @classmethod
    def create(cls):
        return cls()

    def join(self, game_id: str):
        if len(self._players) == 4:
            return False
        player = Player(game_id)
        self._players[game_id] = player
        return True

    def start(self, player_id):
        if self.head_id != player_id:
            return False
        if len(self._players) == 4:
            self._state = const.GAME.START
            return True
        else:
            return False

    def play_pass(self, game_id):
        if self._state != const.GAME.START:
            return False
        player = self._players.get(game_id)
        if player is None:
            print(f'no valid player_id {game_id}')
            return False
        player.play('pass')
        self.check_state()
        return True

    def check_state(self):
        ret = True
        for p in self._players.values():
            if p._state != const.PLAYER.PASS:
                ret = False
        if ret: self._state = const.GAME.END
        return ret

    def status(self) -> schema.GameStatus:
        return schema.GameStatus(
            game_id=self.game_id,
            state=self._state.value
        )