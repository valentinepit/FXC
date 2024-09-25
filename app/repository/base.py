from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.exceptions import NotFoundException


class BaseRepository(ABC):
    @abstractmethod
    def add(self, obj: Any) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def get(self, field: str, value: Any) -> Any | None:
        raise NotImplementedError

    async def delete(self, obj: Any):
        raise NotImplementedError

    @abstractmethod
    async def get_or_error(self, instance_id: int, joined_load: tuple[str, ...] | None = None) -> Any | None:
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

    async def delete(self, obj: Any):
        return await self.session.delete(obj)

    async def get_or_error(self, instance_id: int, joined_load: tuple[str, ...] | None = None) -> Any:
        if instance := await self.get('id', instance_id, joined_load=joined_load):
            return instance
        raise NotFoundException(f'{self.model_cls.__name__} with id {instance_id} not found')

    async def get_or_error_by_field(
        self,
        field: str,
        value: Any,
        joined_load: tuple[str, ...] | None = None,
    ) -> Any:
        if instance := await self.get(field, value, joined_load=joined_load):
            return instance
        raise NotFoundException(f'{self.model_cls.__name__} with {field} = {value} not found')
