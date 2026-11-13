from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class GemImageORM(Base):
    __tablename__ = "gem_images"

    __table_args__ = (
        CheckConstraint("position >= 0", name="ch_position_positive"),
        UniqueConstraint("gem_id", "position", name="uq_gem_images_position"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    gem_id: Mapped[int] = mapped_column(
        ForeignKey("gems.id", ondelete="CASCADE"), nullable=False
    )
    storage_key: Mapped[str] = mapped_column(nullable=False)
    position: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[date] = mapped_column(
        Date, nullable=False, default=func.current_date()
    )
