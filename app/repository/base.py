from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import joinedload


class BaseRepository(ABC):
    @abstractmethod
    def add(self, obj: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get(self, field: str, value: Any) -> Any | None:
        raise NotImplementedError

    async def delete(self, obj: Any):
        raise NotImplementedError


class BaseSQLAlchemyRepository(BaseRepository):
    def __init__(self, session, model_cls) -> None:
        self.session = session
        self.model_cls = model_cls

    def add(self, obj: Any) -> Any:
        self.session.add(obj)
        return obj

    def get(self, field: str, value: Any, joined_load: tuple[str, ...] | None = None) -> Any | None:
        base_q = select(self.model_cls).where(getattr(self.model_cls, field) == value)
        if joined_load:
            base_q = base_q.options(*(joinedload(getattr(self.model_cls, field)) for field in joined_load))
        return (self.session.execute(base_q)).scalars().first()
