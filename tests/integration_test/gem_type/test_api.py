async def test_create_gem_type(client):
    response = await client.post(
        "/gem-types/",
        json={"name": "Heart", "storage_key": "undefined"}
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Heart"
    assert "id" in response.json()

async def test_get_gem_by_id(client, gem_type):
    response = await client.get(
        f"/gem-types/{gem_type.id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == gem_type.id

async def test_get_gem_types(client, gem_type):
    await client.post(
        "/gem-types/",
        json={"name": "Heart", "storage_key": "undefined"}
    )

    response = await client.get(
        "/gem-types/",
    )

    assert response.status_code == 200
    assert len(response.json()) == 2

async def test_create_many_types(client):
    response = await client.post(
        "/gem-types/bulk",
        json=[{"name": "Trillion", "storage_key": "undefined"}, {"name": "Marquise", "storage_key": "undefined"}]
    )

    assert response.status_code == 201

async def test_update_gem_type(client, gem_type):
    response = await client.patch(
        f"/gem-types/{gem_type.id}",
        json={"name": "Cabochon"}
    )

    assert response.status_code == 200
    assert response.json()["name"] != gem_type.name
    assert response.json()["name"] == "Cabochon"

async def test_delete_gem_type(client, gem_type):
    response = await client.delete(
        f"/gem-types/{gem_type.id}"
    )

    assert response.status_code == 204
    assert response.content == b""

    get_deleted_type = await client.get(
        f"/gem-types/{gem_type.id}"
    )
    assert get_deleted_type.status_code == 404