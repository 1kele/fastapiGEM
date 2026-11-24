from src.models import UserORM
from src.repositories.base import BaseRepository
from src.schemas.user import UserResponse


class UserRepository(BaseRepository[UserORM]):
    model = UserORM
    schema = UserResponse
