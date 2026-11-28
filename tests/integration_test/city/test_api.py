async def test_create_city(client):
    response = await client.post(
        "/cities/",
        json={"name": "Москоу", "country_code":"RU"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Москоу"
    assert "id" in response.json()

async def test_get_cities(client, city):
    await client.post(
        "/cities/",
        json={"name": "Казань", "country_code":"RU"}
    )
    response = await client.get("/cities/")

    assert response.status_code == 200
    assert len(response.json()) == 2

async def test_add_bulk(client):
    response = await client.post(
        "/cities/bulk",
        json=[{"name": "Казань", "country_code":"RU"},{"name": "Питер", "country_code":"RU"}]
    )

    assert response.status_code == 201

async def test_get_city_by_id(client, city):
    response = await client.get(f"/cities/{city.id}")

    assert response.status_code == 200
    assert response.json()["id"] == city.id

async def test_update_city(client, city):
    response = await client.patch(
        f"/cities/{city.id}",
        json={"name": "Ижевск"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Ижевск"

async def test_delete_city(client, city):
    response = await client.delete(f"/cities/{city.id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = await client.get(f"/cities/{city.id}")
    assert get_response.status_code == 404