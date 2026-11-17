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
from src.enums.quantity_type import QuantityType
from src.enums.request_status import RequestStatus
from src.enums.stone_size import StoneSize
from src.enums.treatment_type import TreatmentType


class GemRequestsORM(Base):
    __tablename__ = "requests"

    __table_args__ = (
        CheckConstraint("weight_min >= 0", name="ck_gems_min_weight_positive"),
        CheckConstraint("weight_max >= 0", name="ck_gems_max_weight_positive"),
        CheckConstraint("weight_max >= weight_min", name="ck_gems_weight_range"),
        CheckConstraint("price_per_carat_min >= 0", name="ck_price_min_positive"),
        CheckConstraint("price_per_carat_max >= 0", name="ck_price_max_positive"),
        CheckConstraint("price_per_carat_max >= price_per_carat_min", name="ck_request_price_range"),
        CheckConstraint("price_total_min >= 0", name="ck_price_total_min_positive"),
        CheckConstraint("price_total_max >= 0", name="ck_price_total_max_positive"),
        CheckConstraint("price_total_max >= price_total_min", name="ck_request_price_total_range"),
        CheckConstraint(
            "created_at <= expires_at", name="ck_requests_expires_after_created"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    stone_id: Mapped[int] = mapped_column(
        ForeignKey("gem_types.id", ondelete="RESTRICT"), nullable=False
    )
    city_id: Mapped[int | None] = mapped_column(
        ForeignKey("cities.id", ondelete="RESTRICT")
    )
    shape: Mapped[str | None] = mapped_column(String(20))
    color: Mapped[str | None] = mapped_column(String(35))
    origin: Mapped[str | None] = mapped_column(String(3))
    type_quantity: Mapped[QuantityType] = mapped_column(
        SQLEnum(
            QuantityType,
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
    price_per_carat_min: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    price_per_carat_max: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    price_total_min: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    price_total_max: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    additional_information: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    is_profile_hidden: Mapped[bool] = mapped_column(nullable=False, default=False)
    has_certificate: Mapped[bool] = mapped_column(nullable=False, default=False)
    status: Mapped[RequestStatus] = mapped_column(
        SQLEnum(
            RequestStatus,
            name="request_status",
            values_callable=lambda cls: [e.value for e in cls],
        )
        ,default=RequestStatus.CREATED, nullable=False
    )
