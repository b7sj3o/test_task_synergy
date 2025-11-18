from __future__ import annotations

from fastapi.testclient import TestClient


def _sample_user_payload(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "123",
        "gender": "male",
        "addresses": [
            {
                "street": "123 Main St",
                "city": "Kyiv",
                "country": "Ukraine",
                "postcode": "01001",
                "timezone": {"offset": "+02:00", "description": "Kyiv"},
            }
        ],
    }
    base.update(overrides)
    return base


def test_create_and_list_user(client: TestClient) -> None:
    payload = _sample_user_payload()

    response = client.post("/users", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] > 0
    assert data["first_name"] == "John"
    assert len(data["addresses"]) == 1
    assert data["addresses"][0]["timezone"]["offset"] == "+02:00"

    response = client.get("/users?sort=first_name")
    assert response.status_code == 200

    items = response.json()
    assert isinstance(items, list)
    assert len(items) == 1


def test_update_and_delete_user(client: TestClient) -> None:
    create_response = client.post("/users", json=_sample_user_payload())
    assert create_response.status_code == 201

    uid = create_response.json()["id"]

    update_payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "456",
        "gender": "female",
        "addresses": [
            {
                "street": "456 New St",
                "city": "Lviv",
                "country": "Ukraine",
                "postcode": "79000",
                "timezone": {"offset": "+02:00", "description": "Kyiv"},
            }
        ],
    }

    update_response = client.put(f"/users/{uid}", json=update_payload)
    assert update_response.status_code == 200

    updated = update_response.json()
    assert updated["first_name"] == "Jane"
    assert updated["addresses"][0]["city"] == "Lviv"

    delete_response = client.delete(f"/users/{uid}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/users/{uid}")
    assert get_response.status_code == 404
