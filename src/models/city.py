from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class CityORM(Base):
    __tablename__ = "cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(180), nullable=False)
    country_code: Mapped[str] = mapped_column(String(3), nullable=False)
