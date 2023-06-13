from typing import List

from blackjack.domain.event import DomainEvent


class Presenter():

    def __init__(self):
        pass

    def present(self, events: List[DomainEvent]) -> None:
        self.events = events

    def as_view_model(self):
        raise NotImplementedError
