from dataclasses import dataclass


class DomainEvent():
    pass


@dataclass
class ActionEvent(DomainEvent):
    action: str
    success: bool
    player_id: str
    game_id: str


@dataclass
class StatusEvent(DomainEvent):
    status: str
