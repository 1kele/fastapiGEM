import pytest

from enums.request_status import RequestStatus
from src.enums.clarity_type import ClarityType
from src.enums.offer_status import OfferStatus
from src.enums.quantity_type import QuantityType
from src.enums.stone_size import StoneSize
from src.enums.treatment_type import TreatmentType
from src.exceptions.base import PermissionDeniedError


async def test_create_offer(client, gem_request, city, auth_user, user1):
    auth_user(user1)
    response = await client.post(
        f"/requests/{gem_request.id}/offers",
        json={
            "city_id": city.id,
            "shape": "Oval",
            "color": "cat-purple",
            "origin": "UK",
            "type_quantity": QuantityType.SINGLE,
            "weight": 4.21,
            "size": StoneSize.LARGE,
            "clarity": ClarityType.I3,
            "inclusions": "-",
            "treatment": TreatmentType.WAXING,
            "price": 5000.0,
            "additional_information": "doesn't matter actually",
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] > 0
    assert data["city_id"] == city.id
    assert data["request_id"] == gem_request.id
    assert data["status"] == OfferStatus.PENDING
    assert data["price"] == 5000.0
    assert data["seller_id"] == user1.id

    offer_id = data["id"]

    get_offer = await client.get(f"/offers/{offer_id}")

    assert get_offer.status_code == 200
    assert get_offer.json()["price"] == 5000.0

async def test_get_offers_by_request_empty(client, gem_request):
    response = await client.get(f"/requests/{gem_request.id}/offers")

    assert response.status_code == 404

async def test_get_offers_by_request_success(client, gem_request, auth_user, user1, offer_1, offer_2):
    auth_user(user1)
    response = await client.get(f"/requests/{gem_request.id}/offers")

    data = response.json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 2

    return_ids = {offer["id"] for offer in data}

    assert return_ids == {offer_1.id, offer_2.id}

async def test_get_my_offers(client, auth_user, user1, user2, offer_1, offer_2, offer_3):
    auth_user(user1)

    response = await client.get("/offers/my")

    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert isinstance(data, list)

    offer_ids = {offer["id"] for offer in data}

    assert offer_ids == {offer_1.id, offer_2.id}
    assert all(offer["seller_id"] == user1.id for offer in data)

async def test_get_my_offers_empty(client, auth_user, user1):
    auth_user(user1)
    response = await client.get("/offers/my")

    assert response.status_code == 404

async def test_get_offer_by_id(client, offer_1):
    response = await client.get(f"/offers/{offer_1.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == offer_1.id
    assert data["seller_id"] == offer_1.seller_id
    assert data["request_id"] == offer_1.request_id
    assert data["color"] == offer_1.color
    assert data["status"] == offer_1.status.value

async def test_update_offer_success(client, offer_1, auth_user, user1):
    auth_user(user1)

    assert offer_1.seller_id == user1.id

    response = await client.patch(
        f"/offers/{offer_1.id}",
        json={"origin": "KZ", "color": "Scarlet Sky"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["origin"] != offer_1.origin
    assert data["origin"] == "KZ"
    assert data["color"] != offer_1.color
    assert data["color"] == "Scarlet Sky"

async def test_update_offer_denied(client, offer_1, auth_user, user2):
    auth_user(user2)

    assert offer_1.seller_id != user2.id

    response = await client.patch(
        f"/offers/{offer_1.id}",
        json={"origin": "KZ", "color": "Scarlet Sky"}
    )

    assert response.status_code == 403

async def test_accept_offer_success(client, offer_1, gem_request, auth_user, user1):
    auth_user(user1)

    assert gem_request.creator_id == user1.id
    assert offer_1.request_id == gem_request.id
    assert offer_1.status == OfferStatus.PENDING

    response = await client.patch(
        f"/offers/{offer_1.id}/accepted"
    )

    assert response.status_code == 200

    get_offer = await client.get(f"/offers/{offer_1.id}")
    get_response = await client.get(f"/requests/{gem_request.id}")

    assert get_offer.status_code == 200
    assert get_offer.json()["status"] == OfferStatus.ACCEPTED.value
    assert get_response.json()["status"] == RequestStatus.CREATED.value

async def test_accept_offer_reject(client, offer_1, gem_request, auth_user, user2):
    auth_user(user2)

    assert gem_request.creator_id != user2.id

    response = await client.patch(
        f"/offers/{offer_1.id}/accepted"
    )

    assert response.status_code == 403

async def test_reject_offer_success(client, offer_1, gem_request, auth_user, user1):
    auth_user(user1)

    assert gem_request.creator_id == user1.id
    assert offer_1.request_id == gem_request.id

    response = await client.patch(
        f"/offers/{offer_1.id}/rejected"
    )

    assert response.status_code == 200

    get_offer = await client.get(f"/offers/{offer_1.id}")
    get_response = await client.get(f"/requests/{gem_request.id}")

    assert get_offer.status_code == 200
    assert get_offer.json()["status"] == OfferStatus.REJECTED.value
    assert get_response.json()["status"] == RequestStatus.CREATED.value

async def test_reject_offer_reject(client, offer_1, gem_request, auth_user, user2):
    auth_user(user2)

    assert gem_request.creator_id != user2.id

    response = await client.patch(
        f"/offers/{offer_1.id}/rejected"
    )

    assert response.status_code == 403

async def test_withdraw_offer_success(client, offer_1, gem_request, auth_user, user1):
    auth_user(user1)

    assert gem_request.creator_id == user1.id
    assert offer_1.request_id == gem_request.id

    response = await client.patch(
        f"/offers/{offer_1.id}/withdrawn"
    )

    assert response.status_code == 200

    get_offer = await client.get(f"/offers/{offer_1.id}")
    get_response = await client.get(f"/requests/{gem_request.id}")

    assert get_offer.status_code == 200
    assert get_offer.json()["status"] == OfferStatus.WITHDRAWN.value
    assert get_response.json()["status"] == RequestStatus.CREATED.value

async def test_withdraw_offer_reject(client, offer_1, gem_request, auth_user, user2):
    auth_user(user2)

    assert gem_request.creator_id != user2.id

    response = await client.patch(
        f"/offers/{offer_1.id}/withdrawn"
    )

    assert response.status_code == 403