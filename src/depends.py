from datetime import datetime
from typing import Annotated

from fastapi.params import Depends, Query

from src.enums.user_role import UserRole
from src.schemas.pagination import PaginationParams
from src.schemas.request import RequestFilter
from src.schemas.user import UserResponse

PaginationDep = Annotated[PaginationParams, Query()]


async def get_current_user():
    return UserResponse(
        id=1,
        city_id=1,
        first_name="Тестовый",
        last_name="Пользователь",
        email="test@example.com",
        phone="89618239112",
        date_of_birthday=datetime(2000, 12, 12),
        organization="GemScout",
        experience=2,
        address="Тестовый адрес",
        role=UserRole.USER,
    )


CurrentUserDep = Annotated[UserResponse, Depends(get_current_user)]
RequestFilterDep = Annotated[RequestFilter, Query()]
