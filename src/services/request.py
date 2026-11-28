from sqlalchemy.ext.asyncio import AsyncSession

from enums.request_sort import RequestSortField
from enums.sort import Sort
from src.enums.request_status import RequestStatus
from src.exceptions.base import PermissionDeniedError
from src.exceptions.request import InvalidStatusTransitionError, InvalidWeightRangeError
from src.repositories.request import RequestRepository
from src.schemas.request import ChangeRequestStatus, RequestUpdate, RequestFilter, RequestResponseHidden, \
    RequestResponse


class RequestServices:
    @staticmethod
    async def _check_request_ownership(
        request_id: int, user_id: int, session: AsyncSession
    ):
        request = await RequestRepository(session).get_or_raise(id=request_id)

        if request.creator_id != user_id:
            raise PermissionDeniedError("You cannot edit another request")

        return request

    @staticmethod
    async def cancel_request(
        request_id: int, user_id: int, session: AsyncSession
    ) -> None:
        request = await RequestServices()._check_request_ownership(
            request_id, user_id, session
        )

        if request.status != RequestStatus.CREATED:
            raise InvalidStatusTransitionError(
                f"Cannot cancel request with status {request.status}"
            )

        await RequestRepository(session).update(
            id=request_id, data=ChangeRequestStatus(status=RequestStatus.CANCELLED)
        )

    @staticmethod
    async def update_request(
        request_id: int, data: RequestUpdate, user_id: int, session: AsyncSession
    ):
        request = await RequestServices()._check_request_ownership(
            request_id=request_id, user_id=user_id, session=session
        )
        new_min = data.weight_min if data.weight_min is not None else request.weight_min
        new_max = data.weight_max if data.weight_max is not None else request.weight_max

        if new_min > new_max:
            raise InvalidWeightRangeError("Minimum weight cannot exceed maximum weight")

        return await RequestRepository(session).update(id=request_id, data=data)

    @staticmethod
    async def delete_request(request_id: int, user_id: int, session: AsyncSession):
        await RequestServices()._check_request_ownership(
            request_id=request_id, user_id=user_id, session=session
        )
        await RequestRepository(session).delete(id=request_id)

    @staticmethod
    async def get_requests_filter_by(session: AsyncSession,
        filters: RequestFilter,
        sort_by: RequestSortField | None,
        sort: Sort | None,
        offset: int,
        limit: int,
    ):
        get_requests = await RequestRepository(session).get_filter_by(
            filters=filters,
            sort_by=sort_by,
            sort=sort,
            offset=offset,
            limit=limit,
        )

        result = [RequestResponseHidden.model_validate(request)
                  if request.is_profile_hidden else RequestResponse.model_validate(request)
                  for request in get_requests]

        return result