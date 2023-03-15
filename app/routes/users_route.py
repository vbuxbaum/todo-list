from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core import user_service
from app.infrastructure.repositories import UserRepo
from app.routes import current_user, get_db
from app.schemas import user_schema

route = APIRouter(prefix="/users", tags=["Users"])


@route.get("/", response_model=list[user_schema.User])
def get_users(db: Session = Depends(get_db)):
    return UserRepo(db).get_all()


@route.post("/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.create_new_user(UserRepo(db), user)
    except ValueError as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=e.args[0])


@route.get("/{id}", response_model=user_schema.User)
def get_user(
    id: int = Path(gt=0, description="user id"),
    db: Session = Depends(get_db),
):
    try:
        return user_service.get_user_by_id(UserRepo(db), id)
    except LookupError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.args[0])


@route.delete("/{id}", response_model=user_schema.User)
def delete_user(
    user: user_schema.User = Depends(current_user),
    db: Session = Depends(get_db),
):
    return UserRepo(db).delete_by_id(user.id)
