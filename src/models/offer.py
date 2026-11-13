from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, func
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.enums.offer_status import OfferStatus
from src.enums.price_type import PriceType


class OfferORM(Base):
    __tablename__ = "offers"

    __table_args__ = (
        CheckConstraint("offered_price > 0", name="ck_offered_price_positive"),
        CheckConstraint(
            "offered_total_price > 0", name="ck_offered_total_price_positive"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int] = mapped_column(
        ForeignKey("gem_requests.id", ondelete="RESTRICT"), nullable=False
    )
    gem_id: Mapped[int] = mapped_column(
        ForeignKey("gems.id", ondelete="RESTRICT"), nullable=False
    )
    seller_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    price_type: Mapped[PriceType] = mapped_column(
        SQLEnum(
            PriceType,
            name="price_type",
            values_callable=lambda cls: [e.value for e in cls],
        ),
        nullable=False,
    )
    offered_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    offered_total_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    comment: Mapped[str]
    status: Mapped[OfferStatus] = mapped_column(
        nullable=False, default=OfferStatus.PENDING
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
