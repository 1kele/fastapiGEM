from models import CityORM
from schemas.city import CityResponse
from src.repositories.base import BaseRepository


class CityRepository(BaseRepository):
    model = CityORM
    schema = CityResponse
