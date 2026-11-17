from sqlalchemy import select

from models import GemRequestsORM
from repositories.base import BaseRepository
from schemas.request import GemRequestResponse, GemRequestFilter


class GemRequestRepository(BaseRepository):
    model = GemRequestsORM
    schema = GemRequestResponse

    async def get_filter_by(self,filters: GemRequestFilter, page: int, limit: int):
        stmt = select(self.model)

