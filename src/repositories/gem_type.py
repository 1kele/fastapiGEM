from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

from exceptions.base import UniqueViolationError
from src.models.gem_type import GemTypeORM
from src.repositories.base import BaseRepository
from src.schemas.gem_type import GemTypeResponse

from loguru import logger


class GemTypeRepository(BaseRepository):
    model = GemTypeORM
    schema = GemTypeResponse

    async def add(self, data: BaseModel) -> BaseModel:
        try:
            new_entry = self.model(**data.model_dump())

            self.session.add(new_entry)

            await self.session.flush()

            return self.schema.model_validate(new_entry)
        except IntegrityError:
            raise UniqueViolationError
        except Exception as exc:
            logger.warning(str(exc))
