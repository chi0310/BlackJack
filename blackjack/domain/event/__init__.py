import json
from dataclasses import dataclass, asdict
from pydantic import BaseModel
from enum import Enum

# def event2json(event) -> str:
#     def default(o):
#         if isinstance(o, Enum):
#             return o.value
#         if hasattr(o, '__dataclass_fields__'):
#             return asdict(o)
#         raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')
#     return json.dumps(asdict(event), default=default)

def event2json(event: BaseModel) -> str:
    return json.dumps(event.dict())

def event2dict(event: BaseModel) -> dict:
    return event.dict()

class DomainEvent(BaseModel):
    err: int = None


class ActionEvent(BaseModel):
    err: int = None
    action: str = ''
    player_id: str = ''
    game_id: str = ''


class StatusEvent(BaseModel):
    err: int = None
    status: str = ''


class PlayerEvent(BaseModel):
    id: str
    status: str
    cards: list[tuple[str, int]]
    final_score: int = 0


def mask_player_event(event: PlayerEvent) -> PlayerEvent:
    return PlayerEvent(
        id=event.id,
        status=event.status,
        cards=[c if i < 2 else ('?', 0) for i, c in enumerate(event.cards)],
        final_score=0
    )


class DealerEvent(BaseModel):
    cards: list[tuple[str, int]]
    final_score: int = 0


class GameEvent(BaseModel):
    status: str
    dealer: DealerEvent
    players: list[PlayerEvent]
