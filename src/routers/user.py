from fastapi import APIRouter

from src.database import SessionDep
from src.depends import CurrentUserDep
from src.repositories.user import UserRepository
from src.schemas.user import UserUpdate

router = APIRouter(tags=["User"], prefix="/user")


@router.get("/me")
async def get_me(current_user: CurrentUserDep):
    return current_user


@router.patch("/me")
async def edit_my_profile(
    data: UserUpdate, current_user: CurrentUserDep, session: SessionDep
):
    updated_user = await UserRepository(session).update(id=current_user.id, data=data)
    await session.commit()
    return updated_user


@router.get("/{user_id}")
async def get_user_by_id(user_id: int, session: SessionDep):
    return await UserRepository(session).get_or_raise(id=user_id)
