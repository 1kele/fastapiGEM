from operator import and_

from sqlalchemy import select
from collections.abc import Sequence

from src.enums.request_sort import RequestSortField
from src.enums.request_status import RequestStatus
from src.enums.sort import Sort
from src.models import RequestsORM
from src.repositories.base import BaseRepository
from src.schemas.request import RequestFilter, RequestResponse


class RequestRepository(BaseRepository[RequestsORM]):
    model = RequestsORM
    schema = RequestResponse

    async def get_filter_by(
        self,
        filters: RequestFilter,
        sort_by: RequestSortField | None,
        sort: Sort | None,
        offset: int,
        limit: int,
    ) -> Sequence[RequestsORM]:
        stmt = select(self.model)

        if filters.stone_id:
            stmt = stmt.where(self.model.stone_id.in_(filters.stone_id))
        if filters.city_id:
            stmt = stmt.where(self.model.city_id.in_(filters.city_id))
        if filters.shape:
            stmt = stmt.where(self.model.shape.in_(filters.shape))
        if filters.color:
            stmt = stmt.where(self.model.color.in_(filters.color))
        if filters.origin:
            stmt = stmt.where(self.model.origin.in_(filters.origin))
        if filters.weight_min is not None:
            stmt = stmt.where(self.model.weight_max >= filters.weight_min)
        if filters.weight_max is not None:
            stmt = stmt.where(self.model.weight_min <= filters.weight_max)
        if filters.price_min is not None:
            stmt = stmt.where(self.model.price_max >= filters.price_min)
        if filters.price_max is not None:
            stmt = stmt.where(self.model.price_min <= filters.price_max)

        if sort_by == RequestSortField.WEIGHT:
            if sort == Sort.DESC:
                stmt = stmt.order_by(self.model.weight_max.desc())
            else:
                stmt = stmt.order_by(self.model.weight_min)

        if sort_by == RequestSortField.PRICE:
            if sort == Sort.DESC:
                stmt = stmt.order_by(self.model.price_max.desc())
            else:
                stmt = stmt.order_by(self.model.price_min)

        stmt = stmt.where(
            and_(
                self.model.status != RequestStatus.CANCELLED,
                self.model.status != RequestStatus.EXPIRED,
            )
        )
        stmt = stmt.order_by(self.model.id)

        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)

        result = await self.session.execute(stmt)

        instance = result.scalars().all()

        return instance
