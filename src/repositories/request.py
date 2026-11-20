from operator import and_

from sqlalchemy import select, func, update

from enums.request_sort import RequestSortField
from enums.request_status import RequestStatus
from enums.sort import Sort
from exceptions.base import NotFoundError, PermissionDeniedError
from models import RequestsORM
from repositories.base import BaseRepository
from schemas.request import RequestResponse, RequestFilter


class RequestRepository(BaseRepository):
    model = RequestsORM
    schema = RequestResponse

    async def get_filter_by(
        self,
        filters: RequestFilter,
        sort_by: RequestSortField,
        sort: Sort,
        offset: int,
        limit: int,
    ):
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
            stmt = stmt.where(self.model.weight_min >= filters.weight_max)
        if filters.price_per_carat_min is not None:
            stmt = stmt.where(
                self.model.price_per_carat_min >= filters.price_per_carat_min
            )
        if filters.price_per_carat_max is not None:
            stmt = stmt.where(
                self.model.price_per_carat_max >= filters.price_per_carat_max
            )
        if filters.price_total_min is not None:
            stmt = stmt.where(self.model.price_total_min >= filters.price_total_min)
        if filters.price_total_max is not None:
            stmt = stmt.where(self.model.price_total_max >= filters.price_total_max)

        if sort_by == RequestSortField.WEIGHT:
            if sort == Sort.DESC:
                stmt = stmt.order_by(self.model.weight_max.desc())
            else:
                stmt = stmt.order_by(self.model.weight_min)

        # проблема с сортировкой по цене в том что у нас есть либо цена за караты либо тотал и в каждом request разные поля используются
        if sort_by == RequestSortField.PRICE:
            if sort == Sort.DESC:
                price = func.coalesce(
                    self.model.price_total_max, self.model.price_per_carat_max
                )
                stmt = stmt.order_by(price.desc())
            else:
                price = func.coalesce(
                    self.model.price_total_min, self.model.price_per_carat_min
                )
                stmt = stmt.order_by(price)

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

    async def cancelled_request(self, request_id: int, user_id: int) -> None:
        stmt1 = select(self.model).where(id=request_id)
        result1 = await self.session.execute(stmt1)
        instance1 = result1.scalar_one_or_none()

        if not instance1:
            raise NotFoundError("Request not found")

        request = self.schema.model_validate(instance1)

        if not request.creator_id == user_id:
            raise PermissionDeniedError(
                "Доступ запрещен! Нельзя редактировать чужую заявку"
            )

        stmt2 = (
            update(self.model)
            .where(id=request_id)
            .values(status=RequestStatus.CANCELLED)
        )
        result2 = await self.session.execute(stmt2)
