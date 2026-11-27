from fastapi import APIRouter, status

from src.database import SessionDep
from src.depends import CurrentUserDep, PaginationDep, RequestFilterDep
from src.enums.request_sort import RequestSortField
from src.enums.sort import Sort
from src.repositories.request import RequestRepository
from src.schemas.request import (
    RequestCreate,
    RequestCreateInternal,
    RequestUpdate,
)
from src.services.request import RequestServices

router = APIRouter(tags=["Request"], prefix="/requests")


# Авторизация
@router.post("/")
async def create_request(
    data: RequestCreate, current_user: CurrentUserDep, session: SessionDep
):
    new_request = await RequestRepository(session).add(
        RequestCreateInternal(**data.model_dump(), creator_id=current_user.id)
    )
    await session.commit()

    return new_request


@router.get("/")
async def get_requests(
    session: SessionDep,
    pagination: PaginationDep,
    filters: RequestFilterDep,
    sort_by: RequestSortField | None = None,
    sort: Sort | None = None,
):
    return await RequestRepository(session).get_filter_by(
        filters=filters,
        sort_by=sort_by,
        sort=sort,
        offset=pagination.offset,
        limit=pagination.limit,
    )


# Авторизация
@router.get("/my")
async def get_my_requests(
    current_user: CurrentUserDep, pagination: PaginationDep, session: SessionDep
):
    return await RequestRepository(session).get_all(
        creator_id=current_user.id, offset=pagination.offset, limit=pagination.limit
    )


@router.get("/{request_id}")
async def get_requests_by_id(request_id: int, session: SessionDep):
    return await RequestRepository(session).get_or_raise(id=request_id)


# Авторизация(проверка владельца)
@router.patch("/{request_id}")
async def update_request(
    request_id: int,
    data: RequestUpdate,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    updated_request = await RequestServices().update_request(
        request_id=request_id, data=data, user_id=current_user.id, session=session
    )
    await session.commit()
    return updated_request


# Авторизация
@router.patch("/cancel/{request_id}", status_code=status.HTTP_200_OK)
async def cancelled_request(
    request_id: int, current_user: CurrentUserDep, session: SessionDep
):
    await RequestServices().cancel_request(
        request_id=request_id, user_id=current_user.id, session=session
    )
    await session.commit()


# Авторизация(проверка владельца)
@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_request(
    request_id: int, current_user: CurrentUserDep, session: SessionDep
):
    await RequestServices().delete_request(
        request_id=request_id, user_id=current_user.id, session=session
    )
    await session.commit()
