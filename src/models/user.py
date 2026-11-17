from sqlalchemy import Date, ForeignKey, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.enums.user_role import UserRole


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(unique=True, nullable=False)
    date_of_birth: Mapped[Date] = mapped_column(Date, nullable=False)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id", ondelete="RESTRICT"))
    organization: Mapped[str] = mapped_column(String(255))
    experience: Mapped[int] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(String(150), nullable=False)
    passport_photo_storage_key: Mapped[str]
    profile_photo_storage_key: Mapped[str]
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(
            UserRole,
            name="user_roles",
            values_callable=lambda cls: [e.value for e in cls],
        ),
        nullable=False,
        default=UserRole.USER,
    )
