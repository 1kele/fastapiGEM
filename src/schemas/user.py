from datetime import datetime

from pydantic import BaseModel, ConfigDict

from enums.user_role import UserRole


class UserRequest(BaseModel):
    city_id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    date_of_birthday: datetime
    organization: str
    experience: int
    address: str

class UserResponse(UserRequest):
    id: int
    role: UserRole

    model_config = ConfigDict(from_attributes=True)