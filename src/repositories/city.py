from src.models import CityORM
from src.repositories.base import BaseRepository
from src.schemas.city import CityResponse


class CityRepository(BaseRepository[CityORM]):
    model = CityORM
    schema = CityResponse
