from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    func,
    String,
    Computed,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from enums.clarity_type import ClarityType
from enums.quantity_type import QuantityType
from enums.stone_size import StoneSize
from enums.treatment_type import TreatmentType
from src.database import Base
from src.enums.offer_status import OfferStatus
from src.enums.price_type import PriceType


class OfferORM(Base):
    __tablename__ = "offers"

    __table_args__ = (
        CheckConstraint("weight > 0", name="ck_offers_weight_positive"),
        CheckConstraint("price >= 0", name="ck_offers_price_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int] = mapped_column(
        ForeignKey("requests.id", ondelete="RESTRICT"), nullable=False
    )
    seller_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    city_id: Mapped[int] = mapped_column(
        ForeignKey("cities.id", ondelete="RESTRICT"), nullable=False
    )
    shape: Mapped[str] = mapped_column(String(20))
    color: Mapped[str] = mapped_column(String(35))
    origin: Mapped[str] = mapped_column(String(3))
    type_quantity: Mapped[QuantityType] = mapped_column(
        SQLEnum(
            QuantityType,
            name="type_quantity",
            values_callable=lambda cls: [e.value for e in cls],
        ),
        nullable=False,
    )
    weight: Mapped[Decimal] = mapped_column(Numeric(9, 3), nullable=False)
    size: Mapped[StoneSize] = mapped_column(
        SQLEnum(
            StoneSize,
            name="stone_size",
            values_callable=lambda cls: [e.value for e in cls],
        ),
        nullable=False,
    )
    clarity: Mapped[ClarityType] = mapped_column(
        SQLEnum(
            ClarityType,
            name="clarity_type",
            values_callable=lambda cls: [e.value for e in cls],
        ),
        nullable=False,
    )
    inclusions: Mapped[str]
    treatment: Mapped[TreatmentType] = mapped_column(
        SQLEnum(
            TreatmentType,
            name="treatment_type",
            values_callable=lambda cls: [e.value for e in cls],
        ),
        nullable=False,
    )
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    additional_information: Mapped[str]
    status: Mapped[OfferStatus] = mapped_column(
        SQLEnum(
            OfferStatus,
            name="offer_status",
            values_callable=lambda cls: [e.value for e in cls],
        ),
        nullable=False,
        default=OfferStatus.PENDING,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
