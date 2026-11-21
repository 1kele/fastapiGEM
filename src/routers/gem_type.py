from fastapi import APIRouter, status

from depends import PaginationDep
from src.database import SessionDep
from src.exceptions.base import NotFoundError
from src.repositories.gem_type import GemTypeRepository
from src.schemas.gem_type import GemTypeRequest, GemTypeUpdate

router = APIRouter(prefix="/gem-types", tags=["Gem Types"])


@router.get("/{gem_type_id}")
async def get_gem_by_id(gem_type_id: int, session: SessionDep):
    return await GemTypeRepository(session).get_or_raise(id=gem_type_id)


@router.get("/")
async def get_gem_types(session: SessionDep, pagination: PaginationDep):
    all_types = await GemTypeRepository(session).get_all(
        offset=pagination.offset, limit=pagination.limit
    )

    return all_types


# Авторизаци (проверка на админа)
@router.post("/")
async def create_gem_type(data: GemTypeRequest, session: SessionDep):
    new_gem_type = await GemTypeRepository(session).add(data)
    await session.commit()

    return new_gem_type


# Авторизаци (проверка на админа)
@router.post(
    "/bulk",
    status_code=status.HTTP_201_CREATED,
)
async def create_many_types(data: list[GemTypeRequest], session: SessionDep):
    await GemTypeRepository(session).add_bulk(data)
    await session.commit()


# Авторизаци (проверка на админа)
@router.patch("/{gem_type_id}")
async def update_gem_type(gem_type_id: int, data: GemTypeUpdate, session: SessionDep):
    updated_gem_type = await GemTypeRepository(session).update(gem_type_id, data)
    await session.commit()

    return updated_gem_type


# Авторизаци (проверка на админа)
@router.delete("/{gem_type_id}", status_code=status.HTTP_200_OK)
async def delete_gem_type(gem_type_id: int, session: SessionDep):
    await GemTypeRepository(session).delete(gem_type_id)
    await session.commit()
