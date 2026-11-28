from datetime import datetime, timedelta

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.depends import get_current_user
from src.enums.clarity_type import ClarityType
from src.enums.quantity_type import QuantityType
from src.enums.stone_size import StoneSize
from src.enums.treatment_type import TreatmentType
from src.enums.user_role import UserRole
from src.models import UserORM
from src.schemas.city import CityResponse
from src.schemas.gem_type import GemTypeResponse
from src.schemas.offer import OfferResponse
from src.schemas.request import RequestResponse
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
async def user1(session: AsyncSession, city):
    user = UserORM(
        city_id=city.id,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="+15559876543",
        date_of_birth=datetime(1995, 6, 15),
        organization="Global Gems Trading Ltd.",
        experience=7,
        address="221B Baker Street, London, UK",
        passport_photo_storage_key=None,
        profile_photo_storage_key=None,
        role=UserRole.USER,
    )

    session.add(user)
    await session.flush()

    return user

@pytest.fixture
async def user2(session: AsyncSession, city):
    user = UserORM(
        city_id=city.id,
        first_name="Alexander",
        last_name="Smith",
        email="alex.smith@example.com",
        phone="+15551234567",
        date_of_birth=datetime(1990, 3, 22),
        organization="Royal Stone Company",
        experience=12,
        address="45 Fifth Avenue, New York, USA",
        passport_photo_storage_key=None,
        profile_photo_storage_key=None,
        role=UserRole.USER,
    )

    session.add(user)
    await session.flush()
    return user

@pytest.fixture
def auth_user():
    def set_user(user: UserORM):
        app.dependency_overrides[get_current_user] = lambda : user

    yield set_user

    app.dependency_overrides.pop(get_current_user, None)

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
async def gem_request1(client, gem_type, city, auth_user, user1):
    auth_user(user1)
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

@pytest.fixture
async def gem_request2(client, gem_type, city, auth_user, user1):
    auth_user(user1)
    response = await client.post(
        "/requests/",
        json={
            "stone_id": gem_type.id,
            "city_id": city.id,
            "shape": "Cushion",
            "color": "Royal Blue",
            "origin": "LKA",
            "type_quantity": QuantityType.SINGLE,
            "weight_min": 2.50,
            "weight_max": 6.80,
            "stone_size": StoneSize.LARGE,
            "clarity": ClarityType.I3,
            "inclusions": "Small natural crystal inclusions",
            "treatment": TreatmentType.WAXING,
            "price_min": 2500.00,
            "price_max": 12000.00,
            "additional_information": "Looking for a natural blue gemstone with high color saturation",
            "created_at": f"{datetime.now()}",
            "expires_at": f"{datetime.now() + timedelta(days=14)}",
            "is_profile_hidden": False,
            "has_certificate": True,
        },
    )

    return RequestResponse(**response.json())

@pytest.fixture
async def offer_1(client, gem_request1, city, auth_user, user1):
    auth_user(user1)
    response = await client.post(
        f"/requests/{gem_request1.id}/offers",
        json={
            "city_id": city.id,
            "shape": "Cushion",
            "color": "Royal Blue",
            "origin": "RUS",
            "type_quantity": QuantityType.SINGLE,
            "weight": 2.85,
            "size": StoneSize.MEDIUM,
            "clarity": ClarityType.FL,
            "inclusions": "Minor natural inclusions",
            "treatment": TreatmentType.WAXING,
            "price": 3750.0,
            "additional_information": "Natural sapphire with excellent transparency and deep blue color.",
        },
    )

    return OfferResponse(**response.json())

@pytest.fixture
async def offer_2(client, gem_request1, city, auth_user, user1):
    auth_user(user1)
    response = await client.post(
        f"/requests/{gem_request1.id}/offers",
        json={
            "city_id": city.id,
            "shape": "Pear",
            "color": "Golden Yellow",
            "origin": "Brazil",
            "type_quantity": QuantityType.SINGLE,
            "weight": 1.87,
            "size": StoneSize.MEDIUM,
            "clarity": ClarityType.FL,
            "inclusions": "Tiny natural feather inclusions",
            "treatment": TreatmentType.WAXING,
            "price": 4250.0,
            "additional_information": "Natural golden gemstone with pear-shaped cut, excellent transparency and brilliant luster.",
        },
    )

    return OfferResponse(**response.json())

@pytest.fixture
async def offer_3(client, gem_request1, city, auth_user, user2):
    auth_user(user2)
    response = await client.post(
        f"/requests/{gem_request1.id}/offers",
        json={
            "city_id": city.id,
            "shape": "Emerald Cut",
            "color": "Vivid Green",
            "origin": "USA",
            "type_quantity": QuantityType.SINGLE,
            "weight": 3.42,
            "size": StoneSize.LARGE,
            "clarity": ClarityType.FL,
            "inclusions": "Small natural crystal inclusions",
            "treatment": TreatmentType.WAXING,
            "price": 8900.0,
            "additional_information": "Natural Colombian emerald with vivid green color and excellent brilliance.",
        },
    )

    return OfferResponse(**response.json())