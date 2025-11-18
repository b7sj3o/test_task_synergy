from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.domain.schemas.user import UserSchema, UserCreateSchema, UserUpdateSchema
from app.services.user_service import UserService
from app.core.rate_limiting import limiter

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserSchema, status_code=201)
@limiter.limit("30/minute")
def create_user_endpoint(
    request: Request, payload: UserCreateSchema, db: Session = Depends(get_db)
):
    return UserService(db).create_user(payload)


@router.get("", response_model=list[UserSchema], status_code=200)
@limiter.limit("30/minute")
def list_users_endpoint(
    request: Request,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(100, le=200),
    sort: str | None = Query(default=None, pattern="^(first_name|last_name|email)$"),
):
    return UserService(db).list_users(skip=skip, limit=limit, sort=sort)


@router.get("/{user_id}", response_model=UserSchema, status_code=200)
@limiter.limit("30/minute")
def get_user_endpoint(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = UserService(db).get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserSchema, status_code=200)
@limiter.limit("30/minute")
def update_user_endpoint(
    request: Request, user_id: int, payload: UserUpdateSchema, db: Session = Depends(get_db)
):
    user = UserService(db).update_user(user_id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=204)
@limiter.limit("30/minute")
def delete_user_endpoint(request: Request, user_id: int, db: Session = Depends(get_db)):
    ok = UserService(db).delete_user(user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return None
