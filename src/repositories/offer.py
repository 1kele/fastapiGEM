from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database import Base
from exceptions.base import NotFoundError
from models import OfferORM, RequestsORM
from repositories.base import BaseRepository
from schemas.offer import OfferResponse


class OfferRepository(BaseRepository):
    model = OfferORM
    schema = OfferResponse

    async def get_request_from_offer(self, offer_id: int) -> Base:
        stmt = select(RequestsORM).join(OfferORM).where(OfferORM.id == offer_id)
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()

        if not instance:
            raise NotFoundError("Object Not Found")

        return instance
