from src.enums.clarity_type import ClarityType
from src.enums.quantity_type import QuantityType
from src.enums.request_status import RequestStatus
from src.enums.stone_size import StoneSize
from src.enums.treatment_type import TreatmentType
from datetime import datetime, timedelta


async def test_create_request(client, gem_type, city, auth_user, user1):
    auth_user(user1)
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

    data = response.json()

    assert data["stone_id"] == gem_type.id
    assert data["id"] > 0
    assert data["creator_id"] == user1.id
    assert data["status"] == RequestStatus.CREATED

async def test_get_my_requests(client, gem_request1, gem_request2, auth_user, user1):
    auth_user(user1)
    response = await client.get("/requests/my")

    assert response.status_code == 200

    data = response.json()

    request_ids = {request["id"] for request in data}

    assert isinstance(data, list)
    assert len(data) == 2
    assert request_ids == {gem_request1.id, gem_request2.id}
    assert all(request["creator_id"] == user1.id for request in data)

async def test_get_requests(client, gem_request1, gem_type, city, auth_user, user1):
    auth_user(user1)
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

    data = response.json()

    request_creators_ids = {request["creator_id"] for request in data if not request["is_profile_hidden"]}

    assert all(creator_id == user1.id for creator_id in request_creators_ids)
    assert isinstance(data, list)
    assert len(data) == 2


async def test_get_requests_by_id_success(client, gem_request1):
    response = await client.get(f"/requests/{gem_request1.id}")

    assert response.status_code == 200
    assert response.json()["id"] == gem_request1.id

async def test_get_requests_by_id_denied(client):
    response = await client.get(f"/requests/0")

    assert response.status_code == 404


async def test_update_request_correct(client, gem_request1, auth_user, user1):
    auth_user(user1)
    response = await client.patch(
        f"/requests/{gem_request1.id}",
        json={"color": "Padparadscha"}
    )

    assert response.status_code == 200
    assert response.json()["color"] != gem_request1.color
    assert response.json()["color"] == "Padparadscha"

async def test_update_request_incorrect(client, gem_request1, auth_user, user1):
    auth_user(user1)
    response = await client.patch(
        f"/requests/{gem_request1.id}",
        json={"weight_min": 100000}
    )

    assert response.status_code == 422

async def test_update_request_denied(client, gem_request1, auth_user, user2):
    auth_user(user2)
    response = await client.patch(
        f"/requests/{gem_request1.id}",
        json={"color": "Padparadscha"}
    )

    assert response.status_code == 403

async def test_cancelled_request(client, gem_request1, auth_user, user1):
    auth_user(user1)
    response = await client.patch(f"/requests/cancel/{gem_request1.id}")
    assert response.status_code == 200

    request = await client.get(f"/requests/{gem_request1.id}")
    assert request.json()["status"] == RequestStatus.CANCELLED

async def test_cancelled_request_denied(client, gem_request1, auth_user, user2):
    auth_user(user2)
    response = await client.patch(f"/requests/cancel/{gem_request1.id}")
    assert response.status_code == 403

async def test_delete_request(client, gem_request1, auth_user, user1):
    auth_user(user1)
    response = await client.delete(f"/requests/{gem_request1.id}")

    assert response.status_code == 204
    assert response.content == b""

    request = await client.get(f"/requests/{gem_request1.id}")

    assert request.status_code == 404

async def test_delete_request_denied(client, gem_request1, auth_user, user2):
    auth_user(user2)
    response = await client.delete(f"/requests/{gem_request1.id}")
    assert response.status_code == 403