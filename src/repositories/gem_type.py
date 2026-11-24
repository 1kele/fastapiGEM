from src.models.gem_type import GemTypeORM
from src.repositories.base import BaseRepository
from src.schemas.gem_type import GemTypeResponse


class GemTypeRepository(BaseRepository[GemTypeORM]):
    model = GemTypeORM
    schema = GemTypeResponse
