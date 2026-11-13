from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Computed,
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
from src.enums.gem_status import GemStatus
from src.enums.price_type import PriceType
from src.enums.quantity_type import TypeQuantity
from src.enums.stone_size import StoneSize
from src.enums.treatment_type import TreatmentType


class GemORM(Base):
    __tablename__ = "gems"

    __table_args__ = (
        CheckConstraint("weight > 0", name="ck_gems_weight_positive"),
        CheckConstraint("price >= 0", name="ck_gems_price_positive"),
        CheckConstraint("price_total >= 0", name="ck_gems_total_price_positive"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(
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
    price_type: Mapped[PriceType] = mapped_column(
        SQLEnum(
            PriceType,
            name="price_type",
            values_callable=lambda cls: [e.value for e in cls],
        ),
        nullable=False,
    )
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    price_total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        Computed(
            """
            CASE
                WHEN price_type = 'total_price'
                    THEN price
                WHEN price_type = 'price_per_carat'
                    THEN ROUND(price * weight, 2)
            END
            """,
            persisted=True,
        ),
        nullable=False,
    )
    certificate_number: Mapped[str] = mapped_column(String(100))
    description: Mapped[str]
    status: Mapped[GemStatus] = mapped_column(
        SQLEnum(
            GemStatus,
            name="gem_status",
            values_callable=lambda cls: [e.value for e in cls],
        ),
        nullable=False,
        default=GemStatus.DRAFT,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
