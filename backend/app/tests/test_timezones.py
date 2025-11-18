from __future__ import annotations
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.domain.models import Address, Timezone
from app.domain.schemas.timezone import TimezoneCreateSchema
from app.services.timezone_service import TimezoneService


def _user_payload_with_timezone(offset: str, description: str) -> dict[str, object]:
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": f"{uuid4()}@example.com",
        "phone": "123",
        "gender": "male",
        "addresses": [
            {
                "street": "123 Main St",
                "city": "Kyiv",
                "country": "Ukraine",
                "postcode": "01001",
                "timezone": {"offset": offset, "description": description},
            }
        ],
    }


def test_timezones_are_deduplicated_for_same_offset_and_description(
    client: TestClient, db_session: Session
) -> None:
    # create two users with the same timezone
    response1 = client.post("/users", json=_user_payload_with_timezone("+02:00", "Kyiv"))
    response2 = client.post("/users", json=_user_payload_with_timezone("+02:00", "Kyiv"))

    assert response1.status_code == 201
    assert response2.status_code == 201

    timezones = db_session.query(Timezone).all()
    assert len(timezones) == 1

    tz_id = timezones[0].id
    addresses = db_session.query(Address).all()
    assert len(addresses) == 2
    assert {addr.timezone_id for addr in addresses} == {tz_id}
