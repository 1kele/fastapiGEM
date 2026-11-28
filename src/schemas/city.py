from pydantic import BaseModel, ConfigDict


class CityRequest(BaseModel):
    name: str
    country_code: str


class CityResponse(CityRequest):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CityUpdate(BaseModel):
    name: str | None = None
    country_code: str | None = None
