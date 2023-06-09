from . import const


class Player():

    def __init__(self, game_id: str) -> None:
        self.game_id = game_id

        self._money = 0
        self._status = const.PLAYER.INIT

    def play(self, action: str):
        if action == 'pass':
            self._status = const.PLAYER.PASS

    @property
    def state(self):
        return self._status
