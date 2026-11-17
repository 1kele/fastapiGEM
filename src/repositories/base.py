from typing import Any

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from src.exceptions.base import NotFoundError


class BaseRepository:
    model = None
    schema = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, data: BaseModel) -> BaseModel:
        new_entry = self.model(**data.model_dump())

        self.session.add(new_entry)

        await self.session.flush()

        return self.schema.model_validate(new_entry)

    async def add_bulk(self, data: list[BaseModel]):
        orm_objects = [self.model(**payload.model_dump()) for payload in data]

        self.session.add_all(orm_objects)

        await self.session.flush()

    async def get(self, **filters: Any) -> BaseModel | None:
        stmt = select(self.model).filter_by(**filters)

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_or_raise(self, **filters: Any) -> BaseModel:
        stmt = select(self.model).filter_by(**filters)

        result = await self.session.execute(stmt)

        instance = result.scalar_one_or_none()

        if not instance:
            raise NotFoundError("Object not found")

        return instance

    async def get_all(self, offset: int, limit: int) -> BaseModel | None:
        stmt = select(self.model)

        if offset:
            stmt = stmt.offset(offset)

        if limit:
            stmt = stmt.limit(limit)

        result = await self.session.execute(stmt)

        instance = result.scalars().all()

        return self.schema.model_validate(instance)

    async def update(self, id: int, data: BaseModel) -> BaseModel:
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
        stmt = delete(self.model).filter_by(id=id)

        await self.session.execute(stmt)
