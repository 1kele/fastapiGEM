from sqlalchemy.ext.asyncio import AsyncSession

from enums.request_status import RequestStatus
from exceptions.base import PermissionDeniedError
from exceptions.request import InvalidStatusTransitionError
from repositories.request import RequestRepository
from schemas.request import RequestResponse, ChangeRequestStatus


class RequestServices:
    async def cancel_request(
        self, session: AsyncSession, request_id: int, user_id: int
    ) -> None:
        instance = await RequestRepository(session).get_or_raise(id=request_id)

        request = RequestResponse.model_validate(instance)
        if request.status != RequestStatus.CREATED:
            raise InvalidStatusTransitionError(
                f"Cannot cancel request with status {request.status}"
            )
        if request.creator_id != user_id:
            raise PermissionDeniedError(
                "Доступ запрещен! Нельзя редактировать чужую заявку"
            )

        await RequestRepository(session).update(
            id=request_id, data=ChangeRequestStatus(status=RequestStatus.CANCELLED)
        )
