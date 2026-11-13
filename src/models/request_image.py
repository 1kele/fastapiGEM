from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class RequestImageORM(Base):
    __tablename__ = "request_images"

    __table_args__ = (
        CheckConstraint("position >= 0", name="ch_position_positive"),
        UniqueConstraint("request_id", "position", name="uq_request_images_position"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int] = mapped_column(
        ForeignKey("gem_requests.id", ondelete="CASCADE"), nullable=False
    )
    storage_key: Mapped[str] = mapped_column(nullable=False)
    position: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[date] = mapped_column(
        Date, nullable=False, default=func.current_date()
    )
