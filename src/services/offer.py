from sqlalchemy.ext.asyncio import AsyncSession

from database import Base
from enums.offer_status import OfferStatus
from enums.request_status import RequestStatus
from exceptions.base import PermissionDeniedError
from exceptions.offer import InvalidStatusTransitionError
from repositories.offer import OfferRepository
from repositories.request import RequestRepository
from schemas.offer import OfferUpdate, OfferStatusChange
from schemas.request import ChangeRequestStatus
from services.request import RequestServices


class OfferService:
    @staticmethod
    async def update_offer(
        offer_id: int, data: OfferUpdate, user_id: int, session: AsyncSession
    ) -> Base:
        offer = await OfferRepository(session).get_or_raise(id=offer_id)

        if offer.seller_id != user_id:
            raise PermissionDeniedError("You can not edit offer that are not your own")
        if offer.status != OfferStatus.PENDING:
            raise InvalidStatusTransitionError(
                "You can not edit offer that is not in pending status"
            )

        updated_offer = await OfferRepository(session).update(id=offer_id, data=data)
        return updated_offer

    @staticmethod
    async def _check_offer_transition(
        offer_id: int,
        request_creator_id: int,
        target_status: OfferStatus,
        session: AsyncSession,
    ):
        offer = await OfferRepository(session).get_or_raise(id=offer_id)
        request = await OfferRepository(session).get_request_from_offer(
            offer_id=offer_id
        )

        if request.creator_id != request_creator_id:
            raise PermissionDeniedError(
                f"You cannot {target_status.value} another seller's offer"
            )

        if request.status != RequestStatus.CREATED:
            raise InvalidStatusTransitionError(
                f"You cannot {target_status.value} request with status {request.status}"
            )

        if offer.status != OfferStatus.PENDING:
            raise InvalidStatusTransitionError(
                f"You cannot {target_status.value} offer with status {offer.status.value}"
            )

        updated_offer = await OfferRepository(session).update(
            id=offer_id, data=OfferStatusChange(status=target_status)
        )

        return updated_offer

    @staticmethod
    async def accept_offer(
        offer_id: int, request_creator_id: int, session: AsyncSession
    ) -> Base:
        return await OfferService._check_offer_transition(
            offer_id=offer_id,
            request_creator_id=request_creator_id,
            target_status=OfferStatus.ACCEPTED,
            session=session,
        )

    @staticmethod
    async def reject_offer(
        offer_id: int, request_creator_id: int, session: AsyncSession
    ) -> Base:
        return await OfferService._check_offer_transition(
            offer_id=offer_id,
            request_creator_id=request_creator_id,
            target_status=OfferStatus.REJECTED,
            session=session,
        )

    @staticmethod
    async def withdraw_offer(
        offer_id: int, request_creator_id: int, session: AsyncSession
    ) -> Base:
        return await OfferService._check_offer_transition(
            offer_id=offer_id,
            request_creator_id=request_creator_id,
            target_status=OfferStatus.WITHDRAWN,
            session=session,
        )