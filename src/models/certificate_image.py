from datetime import date

from sqlalchemy import CheckConstraint, Date, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class CertificatesImageORM(Base):
    __tablename__ = "certificate_images"

    __table_args__ = (
        CheckConstraint("position >= 0", name="ch_certificate_position_positive"),
        UniqueConstraint("offers_id", "position", name="uq_certificate_images_position"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    offers_id: Mapped[int] = mapped_column(
        ForeignKey("offers.id", ondelete="CASCADE"), nullable=False
    )
    storage_key: Mapped[str] = mapped_column(nullable=False)
    position: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[date] = mapped_column(
        Date, nullable=False, default=func.current_date()
    )
