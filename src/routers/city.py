from fastapi import APIRouter, status

from database import SessionDep
from depends import PaginationDep
from repositories.city import CityRepository
from schemas.city import CityRequest, CityUpdate

router = APIRouter(tags=["Cities"], prefix="/city")


@router.post("/")
async def create_city(data: CityRequest, session: SessionDep):
    new_city = await CityRepository(session).add(data)
    await session.commit()
    return new_city

#Авторизация (только админу)
@router.post("/bulk", status_code=status.HTTP_204_NO_CONTENT)
async def create_many_cities(data: list[CityRequest], session: SessionDep):
    await CityRepository(session).add_bulk(data)
    await session.commit()


@router.get("/")
async def get_cities(session: SessionDep, pagination: PaginationDep):
    return await CityRepository(session).get_all(
        limit=pagination.limit, offset=pagination.offset
    )


@router.get("/{city_id}")
async def get_city_by_id(city_id: int, session: SessionDep):
    return await CityRepository(session).get_or_raise(id=city_id)

#Авторизация (только админу)
@router.patch("/{city_id}")
async def update_city(city_id: int, data: CityUpdate, session: SessionDep):
    updated_city = await CityRepository(session).update(id=city_id, data=data)
    await session.commit()
    return updated_city

#Авторизация (только админу)
@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int, session: SessionDep):
    await CityRepository(session).delete(id=city_id)
    await session.commit()
