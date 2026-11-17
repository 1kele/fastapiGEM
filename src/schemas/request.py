from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from enums.clarity_type import ClarityType
from enums.price_type import PriceType
from enums.quantity_type import QuantityType
from enums.request_status import RequestStatus
from enums.stone_size import StoneSize
from enums.treatment_type import TreatmentType

class GemRequestCreate(BaseModel):
    stone_id: int
    city_id: int
    shape: str
    color: str
    origin: str
    type_quantity: QuantityType
    weight_min: Decimal = Field(ge=0)
    weight_max: Decimal = Field(gt=0)
    stone_size: StoneSize
    clarity: ClarityType
    inclusions: str
    treatment: TreatmentType
    price_type: PriceType
    price_min: Decimal
    price_max: Decimal
    additional_information: str
    created_at: datetime
    expires_at: datetime
    is_profile_hidden: bool
    has_certificate: bool

class GemRequestCreateInternal(GemRequestCreate):
    creator_id: int

class GemRequestResponse(GemRequestCreateInternal):
    id: int
    status: RequestStatus
    model_config = ConfigDict(from_attributes=True)

class GemRequestUpdate(BaseModel):
    stone_id: int | None = None
    city_id: int | None = None
    shape: str | None = None
    color: str | None = None
    origin: str | None = None
    type_quantity: QuantityType | None = None
    weight_min: Decimal | None = Field(default=None, ge=0)
    weight_max: Decimal | None = Field(default=None, gt=0)
    stone_size: StoneSize | None = None
    clarity: ClarityType | None = None
    inclusions: str | None = None
    treatment: TreatmentType | None = None
    price_type: PriceType | None = None
    price_min: Decimal | None = None
    price_max: Decimal | None = None
    additional_information: str | None = None
    created_at: datetime
    expires_at: datetime | None = None
    is_profile_hidden: bool | None = None
    has_certificate: bool | None = None

class GemRequestFilter(BaseModel):
    stone_id: list[int] | None = None
    city_id: list[int] | None = None
    shape: list[str] | None = None
    color: list[str] | None = None
    origin: list[str] | None = None
    type_quantity: list[QuantityType] | None = None
    weight_min: Decimal | None = Field(default=None, ge=0)
    weight_max: Decimal | None = Field(default=None, gt=0)
    stone_size: list[StoneSize] | None = None
    clarity: list[ClarityType] | None = None
    inclusions: str | None = None
    treatment: list[TreatmentType] | None = None
    price_type: list[PriceType] | None = None
    price_min: Decimal | None = None
    price_max: Decimal | None = None
    certificate: bool | None = None
