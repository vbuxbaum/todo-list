from pydantic import BaseModel as BaseSchema

from app.schemas.item_schema import Item


class BoardBase(BaseSchema):
    title: str | None = None
    description: str | None = None


class BoardCreate(BoardBase):
    pass


class Board(BoardBase):
    id: int
    owner_id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
