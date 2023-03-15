from pydantic import BaseModel as BaseSchema
from app.schemas.board_schema import Board


class UserBase(BaseSchema):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    boards: list[Board] = []

    class Config:
        orm_mode = True
