from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    func,
)
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base
from src.enums.clarity_type import ClarityType
from src.enums.price_type import PriceType
from src.enums.quantity_type import TypeQuantity
from src.enums.request_status import RequestStatus
from src.enums.stone_size import StoneSize
from src.enums.treatment_type import TreatmentType


class GemRequestsORM(Base):
    __tablename__ = "gem_requests"

    __table_args__ = (
        CheckConstraint("weight_min >= 0", name="ck_gems_min_weight_positive"),
        CheckConstraint("weight_max >= 0", name="ck_gems_max_weight_positive"),
        CheckConstraint("price_min >= 0", name="ck_price_min_positive"),
        CheckConstraint("price_max >= 0", name="ck_price_max_positive"),
        CheckConstraint("price_max >= price_min", name="ck_request_price_range"),
        CheckConstraint(
            "created_at <= expires_at", name="ck_gem_requests_expires_after_created"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    stone_id: Mapped[int] = mapped_column(
        ForeignKey("gem_types.id", ondelete="RESTRICT"), nullable=False
    )
    shape: Mapped[str] = mapped_column(String(20), nullable=False)
    color: Mapped[str] = mapped_column(String(35), nullable=False)
    origin: Mapped[str] = mapped_column(String(3), nullable=False)
    type_quantity: Mapped[TypeQuantity] = mapped_column(
        SQLEnum(
            TypeQuantity,
            name="type_quantity",
            values_callable=lambda cls: [e.value for e in cls],
        ),
        nullable=False,
    )
    weight_min: Mapped[Decimal] = mapped_column(Numeric(9, 3))
    weight_max: Mapped[Decimal] = mapped_column(Numeric(9, 3))
    stone_size: Mapped[StoneSize] = mapped_column(
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
    price_type: Mapped[PriceType] = mapped_column(
        SQLEnum(
            PriceType,
            name="price_type",
            values_callable=lambda cls: [e.value for e in cls],
        ),
        nullable=False,
    )
    price_min: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    price_max: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    additional_information: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    is_profile_hidden: Mapped[bool] = mapped_column(nullable=False, default=False)
    city_id: Mapped[int | None] = mapped_column(
        ForeignKey("cities.id", ondelete="RESTRICT"), nullable=False
    )
    has_certificate: Mapped[bool] = mapped_column(nullable=False, default=False)
    status: Mapped[RequestStatus] = mapped_column(
        SQLEnum(
            RequestStatus,
            name="request_status",
            values_callable=lambda cls: [e.value for e in cls],
        )
    )
