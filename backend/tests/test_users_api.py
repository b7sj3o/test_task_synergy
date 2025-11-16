from __future__ import annotations

from fastapi.testclient import TestClient
from app.main import app
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine


client = TestClient(app)


def setup_module() -> None:
    # fresh tables for tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_and_list_user() -> None:
    payload = {
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
        ]
    }
    r = client.post("/users", json=payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["id"] > 0
    assert data["first_name"] == "John"
    assert len(data["addresses"]) == 1
    assert data["addresses"][0]["timezone"]["offset"] == "+02:00"

    r = client.get("/users?sort=first_name")
    assert r.status_code == 200
    items = r.json()
    assert isinstance(items, list)
    assert len(items) == 1


def test_update_and_delete_user() -> None:
    # list users to get id
    r = client.get("/users")
    uid = r.json()[0]["id"]

    upd = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "456",
        "gender": "female",
        "addresses": [
            {"street": "456 New St", "city": "Lviv", "country": "Ukraine", "postcode": "79000"}
        ],
    }
    r = client.put(f"/users/{uid}", json=upd)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["first_name"] == "Jane"
    assert data["addresses"][0]["city"] == "Lviv"

    r = client.delete(f"/users/{uid}")
    assert r.status_code == 204

    r = client.get(f"/users/{uid}")
    assert r.status_code == 404


