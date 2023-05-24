from typing import Union

from blackjack.repository.game_repository import GameRepository
from blackjack.domain.game import Game
from blackjack.domain import schema

game_repo = GameRepository.make('mem')

def create_game(player_id: str):
    game = Game(player_id)
    game_id = game_repo.save(game)
    sucess = game.join(player_id)
    if sucess:
        return game_id
    else:
        return

def join_game(game_id: str, player_id: str):
    game = game_repo.get(game_id)
    if game is None:
        return False
    return  game.join(player_id)

def start(game_id, player_id):
    game = game_repo.get(game_id)
    if game is None:
        return False
    return game.start(player_id)


def playpass(game_id: str, player_id: str):
    game = game_repo.get(game_id)
    if game is None:
        return False
    return game.play_pass(player_id)

def status(game_id: str) -> Union[schema.GameStatus, None]:
    game = game_repo.get(game_id)
    if game is None:
        return 
    return game.status()
