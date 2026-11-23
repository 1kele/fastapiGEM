from datetime import date
from typing import Annotated

from fastapi.params import Query, Depends

from enums.user_role import UserRole
from schemas.pagination import PaginationParams
from schemas.user import UserResponse

PaginationDep = Annotated[PaginationParams, Query()]


async def get_current_user():
    return UserResponse(
        id=1,
        city_id=1,
        first_name="Тестовый",
        last_name="Пользователь",
        email="test@example.com",
        phone="89618239112",
        date_of_birthday=date(2000, 12, 12),
        organization="GemScout",
        experience=2,
        address="Тестовый адрес",
        passport_photo_storage_key="test/passport.jpg",
        profile_photo_storage_key="test/profile.jpg",
        role=UserRole.USER,
    )


CurrentUserDep = Annotated[UserResponse, Depends(get_current_user)]
