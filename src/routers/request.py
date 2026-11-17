from fastapi import APIRouter

from database import SessionDep
from repositories.request import GemRequestRepository
from schemas.request import GemRequestCreate, GemRequestCreateInternal, GemRequestFilter

router = APIRouter(tags=["Gem Request"], prefix="/request")

@router.post("/")
async def create_request(data: GemRequestCreate, session: SessionDep):
    new_request = await GemRequestRepository(session).add(GemRequestCreateInternal(**data.model_dump(), creator_id=1))
    await session.commit()

    return new_request

@router.get("/")
async def get_requests(session: SessionDep, filters: GemRequestFilter, page: int = 1, limit: int = 10):
    ...

@router.get("/{request_id}")
async def get_requests_by_id(request_id: int, session: SessionDep):
    return await GemRequestRepository(session).get_or_raise(id=request_id)