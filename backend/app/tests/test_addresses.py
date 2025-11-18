from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.domain.models import Address


def _user_with_address_payload(
    street: str = "123 Main St",
    city: str = "Kyiv",
    country: str = "Ukraine",
) -> dict[str, object]:
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "123",
        "gender": "male",
        "addresses": [
            {
                "street": street,
                "city": city,
                "country": country,
                "postcode": "01001",
                "timezone": {"offset": "+02:00", "description": "Kyiv"},
            }
        ],
    }


def test_address_created_and_linked_to_user(client: TestClient, db_session: Session) -> None:
    response = client.post("/users", json=_user_with_address_payload())
    assert response.status_code == 201

    user_id = response.json()["id"]

    addresses = db_session.query(Address).all()
    assert len(addresses) == 1

    addr = addresses[0]
    assert addr.user_id == user_id
    assert addr.city == "Kyiv"
    assert addr.country == "Ukraine"


def test_addresses_replaced_on_user_update(client: TestClient, db_session: Session) -> None:
    create_response = client.post("/users", json=_user_with_address_payload())
    assert create_response.status_code == 201

    user_id = create_response.json()["id"]

    update_payload = _user_with_address_payload(
        street="456 New St",
        city="Lviv",
    )

    update_response = client.put(f"/users/{user_id}", json=update_payload)
    assert update_response.status_code == 200

    addresses = db_session.query(Address).all()
    # replace_for_user should leave exactly one updated address
    assert len(addresses) == 1
    addr = addresses[0]
    assert addr.street == "456 New St"
    assert addr.city == "Lviv"
