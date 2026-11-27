from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.enums.user_role import UserRole


class UserRequest(BaseModel):
    city_id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    date_of_birth: datetime
    organization: str
    experience: int
    address: str


class UserResponse(UserRequest):
    id: int
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    city_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    date_of_birth: datetime | None = None
    organization: str | None = None
    experience: int | None = None
    address: str | None = None


class UserStatusChange(BaseModel):
    role: UserRole
