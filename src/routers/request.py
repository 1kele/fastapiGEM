from fastapi import APIRouter, status
from fastapi.params import Query

from database import SessionDep
from depends import PaginationDep
from enums.request_sort import RequestSortField
from enums.sort import Sort
from repositories.request import RequestRepository
from schemas.request import (
    RequestCreate,
    RequestCreateInternal,
    RequestFilter,
    RequestUpdate,
)
from services.request import RequestServices

router = APIRouter(tags=["Gem Request"], prefix="/request")


# Авторизация
@router.post("/")
async def create_request(data: RequestCreate, session: SessionDep):
    new_request = await RequestRepository(session).add(
        RequestCreateInternal(**data.model_dump(), creator_id=1)
    )
    await session.commit()

    return new_request


@router.get("/")
async def get_requests(
    session: SessionDep,
    sort_by: RequestSortField,
    pagination: PaginationDep,
    sort: Sort,
    filters: RequestFilter = Query(),
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
async def get_my_requests(session: SessionDep, pagination: PaginationDep):
    return await RequestRepository(session).get_all(
        creator_id=1, offset=pagination.offset, limit=pagination.limit
    )


@router.get("/{request_id}")
async def get_requests_by_id(request_id: int, session: SessionDep):
    return await RequestRepository(session).get_or_raise(id=request_id)


# Авторизация(проверка владельца)
@router.patch("/{request_id}")
async def update_request(session: SessionDep, request_id: int, data: RequestUpdate):
    updated_request = await RequestRepository(session).update(id=request_id, data=data)
    await session.commit()
    return updated_request


# Авторизация
@router.patch("/cancel/{request_id}", status_code=status.HTTP_200_OK)
async def cancelled_request(session: SessionDep, request_id: int):
    await RequestServices().cancel_request(session, request_id=request_id, user_id=1)
    await session.commit()


# Авторизация(проверка владельца)
@router.delete("/{request_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_request(request_id: int, session: SessionDep):
    await RequestRepository(session).delete(id=request_id)
    await session.commit()
