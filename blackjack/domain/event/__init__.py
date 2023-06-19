from dataclasses import dataclass


@dataclass
class DomainEvent():
    err: str = None


@dataclass
class ActionEvent(DomainEvent):
    action: str = ''
    player_id: str = ''
    game_id: str = ''


@dataclass
class StatusEvent(DomainEvent):
    status: str = ''
