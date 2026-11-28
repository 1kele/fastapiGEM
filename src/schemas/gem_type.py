from pydantic import BaseModel, ConfigDict


class GemTypeRequest(BaseModel):
    name: str
    storage_key: str


class GemTypeResponse(GemTypeRequest):
    id: int

    model_config = ConfigDict(from_attributes=True)


class GemTypeUpdate(BaseModel):
    name: str | None = None
    storage_key: str | None = None
