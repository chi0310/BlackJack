from typing import List, Optional

from blackjack.domain.event import DomainEvent


class Presenter():

    def __init__(self):
        pass

    def present(self, events: List[DomainEvent]) -> None:
        self.events = events

    def as_view_model(self):
        raise NotImplementedError

    @property
    def is_validate(self) -> Optional[str]:
        ret = ''
        for e in self.events:
            if e.err is not None:
                temp = f'{e.err}\n'
                ret += temp
        if len(ret) == 0:
            return None
        else:
            return ret
