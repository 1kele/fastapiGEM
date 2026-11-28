from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from src.exceptions.base import NotFoundError


class BaseRepository[ModelT: Base]:
    model: type[ModelT]
    schema: type[BaseModel]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, data: BaseModel) -> ModelT:
        new_entry = self.model(**data.model_dump())

        self.session.add(new_entry)

        await self.session.flush()

        return new_entry

    async def add_bulk(self, data: Sequence[BaseModel]) -> None:
        orm_objects = [self.model(**payload.model_dump()) for payload in data]

        self.session.add_all(orm_objects)

        await self.session.flush()

    async def get(self, **filters: Any) -> ModelT | None:
        stmt = select(self.model).filter_by(**filters)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_or_raise(self, **filters: Any) -> ModelT:
        instance = await self.get(**filters)

        if not instance:
            raise NotFoundError("Object not found")

        return instance

    async def get_all(
        self, offset: int, limit: int, **filters: Any
    ) -> Sequence[ModelT]:
        stmt = select(self.model).filter_by(**filters)

        if offset:
            stmt = stmt.offset(offset)

        if limit:
            stmt = stmt.limit(limit)

        result = await self.session.execute(stmt)

        instance = result.scalars().all()

        if not instance:
            raise NotFoundError("Objects not found")

        return instance

    async def update(self, id: int, data: BaseModel) -> ModelT:
        stmt = (
            update(self.model)
            .filter_by(id=id)
            .values(**data.model_dump(exclude_unset=True))
            .returning(self.model)
        )

        result = await self.session.execute(stmt)

        instance = result.scalar_one_or_none()

        if not instance:
            raise NotFoundError("Object not found")

        return instance

    async def delete(self, id: int) -> None:
        stmt = delete(self.model).filter_by(id=id).returning(self.model)

        result = await self.session.execute(stmt)

        if not result.scalar_one_or_none():
            raise NotFoundError("Object not found")
