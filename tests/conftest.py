import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from schemas.city import CityResponse
from src.database import get_session, Base
from src.app import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL)
Test_session = async_sessionmaker(bind=engine, expire_on_commit=False)

@pytest.fixture
async def session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with Test_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client(session: AsyncSession):
    async def override_get_session():
        yield session
    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def city(client):
    response = await client.post(
        "/cities/",
        json={"name": "Москоу", "country_code":"RU"}
    )
    return CityResponse(**response.json())