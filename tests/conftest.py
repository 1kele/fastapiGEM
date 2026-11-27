from datetime import datetime, timedelta

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from enums.clarity_type import ClarityType
from enums.quantity_type import QuantityType
from enums.stone_size import StoneSize
from enums.treatment_type import TreatmentType
from schemas.city import CityResponse
from schemas.gem_type import GemTypeResponse
from schemas.request import RequestResponse
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

@pytest.fixture
async def gem_type(client):
    response = await client.post(
        "/gem-types/",
        json={"name": "Round", "storage_key": "undefined"}
    )

    return GemTypeResponse(**response.json())

@pytest.fixture
async def gem_request(client, gem_type, city):
    response = await client.post(
        "/requests/",
        json={
            "stone_id": gem_type.id,
            "city_id": city.id,
            "shape": "Oval",
            "color": "Deep Red",
            "origin": "MMR",
            "type_quantity": QuantityType.SINGLE,
            "weight_min": 1.25,
            "weight_max": 4.75,
            "stone_size": StoneSize.MEDIUM,
            "clarity": ClarityType.FL,
            "inclusions": "Minor natural inclusions",
            "treatment": TreatmentType.OILING,
            "price_min": 1250.00,
            "price_max": 7800.00,
            "additional_information": "Looking for a natural gemstone with excellent color",
            "created_at": f"{datetime.now()}",
            "expires_at": f"{(datetime.now() + timedelta(days=7))}",
            "is_profile_hidden": True,
            "has_certificate": False,
        },
    )

    return RequestResponse(**response.json())