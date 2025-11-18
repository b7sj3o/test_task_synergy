import httpx
from fastapi import APIRouter, Request
from app.core.rate_limiting import limiter

router = APIRouter(prefix="/external", tags=["external"])


@router.get("/random-user")
@limiter.limit("30/minute")
async def random_user(request: Request):
    async with httpx.AsyncClient() as client:
        r = await client.get("https://randomuser.me/api/?results=1")
        r.raise_for_status()
        data = r.json()
        user = data["results"][0]
        # Map to our simplified structure the frontend/backend expects
        mapped = {
            "first_name": user["name"]["first"],
            "last_name": user["name"]["last"],
            "email": user["email"],
            "phone": user.get("phone"),
            "gender": user.get("gender"),
            "addresses": [
                {
                    "street": f'{user["location"]["street"]["number"]} {user["location"]["street"]["name"]}',
                    "city": user["location"]["city"],
                    "state": user["location"].get("state"),
                    "country": user["location"]["country"],
                    "postcode": str(user["location"]["postcode"]),
                    "timezone": {
                        "offset": user["location"]["timezone"]["offset"],
                        "description": user["location"]["timezone"]["description"],
                    },
                }
            ],
        }
        return mapped
