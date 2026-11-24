from sqlalchemy.ext.asyncio import AsyncSession

from src.enums.request_status import RequestStatus
from src.exceptions.base import PermissionDeniedError
from src.exceptions.request import InvalidStatusTransitionError
from src.repositories.request import RequestRepository
from src.schemas.request import ChangeRequestStatus, RequestUpdate


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
        await RequestServices()._check_request_ownership(
            request_id=request_id, user_id=user_id, session=session
        )
        return await RequestRepository(session).update(id=request_id, data=data)

    @staticmethod
    async def delete_request(request_id: int, user_id: int, session: AsyncSession):
        await RequestServices()._check_request_ownership(
            request_id=request_id, user_id=user_id, session=session
        )
        await RequestRepository(session).delete(id=request_id)
