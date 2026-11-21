from models import OfferORM
from repositories.base import BaseRepository
from schemas.offer import OfferResponse


class OfferRepository(BaseRepository):
    model = OfferORM
    schema = OfferResponse