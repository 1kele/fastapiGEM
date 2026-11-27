import pytest

from enums.clarity_type import ClarityType
from enums.quantity_type import QuantityType
from enums.request_status import RequestStatus
from enums.stone_size import StoneSize
from enums.treatment_type import TreatmentType
from datetime import datetime, timedelta

from src.exceptions.request import InvalidWeightRangeError


async def test_create_request(client, gem_type, city):
    response = await client.post(
        "/requests/",
        json={
            "stone_id": f"{gem_type.id}",
            "city_id": f"{city.id}",
            "shape": "Rectangle",
            "color": "blue-eyed",
            "origin": "US",
            "type_quantity": QuantityType.SINGLE,
            "weight_min": 0.1,
            "weight_max": 2.0,
            "stone_size": StoneSize.MEDIUM,
            "clarity": ClarityType.FL,
            "inclusions": "",
            "treatment": TreatmentType.OILING,
            "price_min": 300.0,
            "price_max": 5000.0,
            "additional_information": "I don't wanna buy bull shit",
            "created_at": f"{datetime.now()}",
            "expires_at": f"{datetime.now() + timedelta(days=5)}",
            "is_profile_hidden": False,
            "has_certificate": True,
        }
    )

    assert response.status_code == 200
    assert response.json()["stone_id"] == gem_type.id
    assert "id" in response.json()

async def test_get_my_requests(client):
    response = await client.get("/requests/my")

    assert response.status_code == 200

async def test_get_requests(client, gem_request, gem_type, city):
    await client.post(
        "/requests/",
        json={
            "stone_id": f"{gem_type.id}",
            "city_id": f"{city.id}",
            "shape": "Rectangle",
            "color": "blue-eyed",
            "origin": "US",
            "type_quantity": QuantityType.SINGLE,
            "weight_min": 0.1,
            "weight_max": 2.0,
            "stone_size": StoneSize.MEDIUM,
            "clarity": ClarityType.FL,
            "inclusions": "",
            "treatment": TreatmentType.OILING,
            "price_min": 300.0,
            "price_max": 5000.0,
            "additional_information": "I don't wanna buy bull shit",
            "created_at": f"{datetime.now()}",
            "expires_at": f"{datetime.now() + timedelta(days=5)}",
            "is_profile_hidden": False,
            "has_certificate": True,
        }
    )
    response = await client.get("/requests/")

    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_requests_by_id(client, gem_request):
    response = await client.get(f"/requests/{gem_request.id}")

    assert response.status_code == 200
    assert response.json()["id"] == gem_request.id

async def test_update_request(client, gem_request):
    response = await client.patch(
        f"/requests/{gem_request.id}",
        json={"color": "Padparadscha"}
    )

    assert response.status_code == 200
    assert response.json()["color"] != gem_request.color
    assert response.json()["color"] == "Padparadscha"

    incorrect_response = await client.patch(
        f"/requests/{gem_request.id}",
        json={"weight_min": 100000}
    )

    assert incorrect_response.status_code == 422

async def test_cancelled_request(client, gem_request):
    response = await client.patch(f"/requests/cancel/{gem_request.id}")
    assert response.status_code == 200

    request = await client.get(f"/requests/{gem_request.id}")
    assert request.json()["status"] == RequestStatus.CANCELLED

async def test_delete_request(client, gem_request):
    response = await client.delete(f"/requests/{gem_request.id}")

    assert response.status_code == 204
    assert response.content == b""

    request = await client.get(f"/requests/{gem_request.id}")

    assert request.status_code == 404