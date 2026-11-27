from fastapi import APIRouter

from src.database import SessionDep
from src.depends import CurrentUserDep, PaginationDep
from src.repositories.offer import OfferRepository
from src.schemas.offer import (
    OfferCreateInternal,
    OfferRequest,
    OfferStatusResponse,
    OfferUpdate,
)
from src.services.offer import OfferService

request_offer_router = APIRouter(tags=["Offer"])
router = APIRouter(tags=["Offer"], prefix="/offers")


# Авторизация
@request_offer_router.post("/requests/{request_id}/offers")
async def create_offer(
    data: OfferRequest,
    request_id: int,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    new_offer = await OfferRepository(session).add(
        OfferCreateInternal(
            **data.model_dump(), request_id=request_id, seller_id=current_user.id
        )
    )
    await session.commit()
    return new_offer


@request_offer_router.get("/requests/{request_id}/offers")
async def get_offer_by_request_id(
    request_id: int, pagination: PaginationDep, session: SessionDep
):
    return await OfferRepository(session).get_all(
        request_id=request_id, offset=pagination.offset, limit=pagination.limit
    )


# Авторизация
@router.get("/my")
async def get_my_offers(
    session: SessionDep, current_user: CurrentUserDep, pagination: PaginationDep
):
    return await OfferRepository(session).get_all(
        seller_id=current_user.id, offset=pagination.offset, limit=pagination.limit
    )


@router.get("/{offer_id}")
async def get_offer_by_id(offer_id: int, session: SessionDep):
    return await OfferRepository(session).get_or_raise(id=offer_id)


# Авторизация(проверка что это предложение у конкретного пользователя)
@router.patch("/{offer_id}")
async def update_offer(
    offer_id: int, data: OfferUpdate, current_user: CurrentUserDep, session: SessionDep
):
    updated_offer = await OfferService().update_offer(
        offer_id=offer_id, data=data, user_id=current_user.id, session=session
    )
    await session.commit()
    return updated_offer


# Авторизация(проверка что это запрос у конкретного пользователя)
# request_creator_id это пользователь кому пришел офер
@router.patch("/{offer_id}/accepted", response_model=OfferStatusResponse)
async def accept_offer(
    offer_id: int, current_user: CurrentUserDep, session: SessionDep
):
    offer = await OfferService().accept_offer(
        offer_id=offer_id, request_creator_id=current_user.id, session=session
    )
    await session.commit()
    return offer


# Авторизация(проверка что это запрос у конкретного пользователя)
@router.patch("/{offer_id}/rejected")
async def reject_offer(
    offer_id: int, current_user: CurrentUserDep, session: SessionDep
):
    offer = await OfferService().reject_offer(
        offer_id=offer_id, request_creator_id=current_user.id, session=session
    )
    await session.commit()
    return offer


# Авторизация(проверка что это запрос у конкретного пользователя)
@router.patch("/{offer_id}/withdrawn")
async def withdraw_offer(
    offer_id: int, current_user: CurrentUserDep, session: SessionDep
):
    offer = await OfferService().withdraw_offer(
        offer_id=offer_id, request_creator_id=current_user.id, session=session
    )
    await session.commit()
    return offer
