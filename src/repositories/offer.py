from sqlalchemy import select

from src.exceptions.base import NotFoundError
from src.models import OfferORM, RequestsORM
from src.repositories.base import BaseRepository
from src.schemas.offer import OfferResponse


class OfferRepository(BaseRepository[OfferORM]):
    model = OfferORM
    schema = OfferResponse

    async def get_request_from_offer(self, offer_id: int) -> RequestsORM:
        stmt = select(RequestsORM).join(OfferORM).where(OfferORM.id == offer_id)
        result = await self.session.execute(stmt)
        instance = result.scalar_one_or_none()

        if not instance:
            raise NotFoundError("Object Not Found")

        return instance
