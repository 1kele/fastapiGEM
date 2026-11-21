from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from enums.clarity_type import ClarityType
from enums.offer_status import OfferStatus
from enums.quantity_type import QuantityType
from enums.stone_size import StoneSize
from enums.treatment_type import TreatmentType


class OfferRequest(BaseModel):
    request_id: int
    seller_id: int
    city_id: int
    shape: str
    color: str
    origin: str
    type_quantity: QuantityType
    weight: Decimal
    size: StoneSize
    clarity: ClarityType
    inclusions: str
    treatment: TreatmentType
    price: Decimal = Field(gt=0)
    additional_information: str


class OfferResponse(OfferRequest):
    id: int
    status: OfferStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OfferUpdate(BaseModel):
    city_id: int | None = None
    shape: str | None = None
    color: str | None = None
    origin: str | None = None
    type_quantity: QuantityType | None = None
    weight: Decimal | None = None
    size: StoneSize | None = None
    clarity: ClarityType | None = None
    inclusions: str | None = None
    treatment: TreatmentType | None = None
    price: Decimal | None = Field(default=None, gt=0)
    additional_information: str | None = None


class OfferChangeStatus(BaseModel):
    status: OfferStatus
