import uuid

class GameRepository():
    @classmethod
    def make(cls, type: str, *args , **kwargs):
        if type == 'mem':
            return GameRepositoryMem(*args, **kwargs)
        else:
            raise NotImplementedError(f'{type} is not supported')

class GameRepositoryMem(GameRepository):
    def __init__(self) -> None:
        self.id2ins = {}

    def save(self, game) -> str:
        game_id = str(uuid.uuid4())
        self.id2ins[game_id] = game
        game.game_id = game_id
        return game_id

    def get(self, game_id: str):
        game = self.id2ins.get(game_id)
        if game is None:
            print(f'game_id of the game isn\'t exist')
        return game