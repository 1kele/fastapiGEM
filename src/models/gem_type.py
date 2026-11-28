from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class GemTypeORM(Base):
    __tablename__ = "gem_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25), unique=True, nullable=False)
    storage_key: Mapped[str] = mapped_column(nullable=False)
