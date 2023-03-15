from pydantic import BaseModel as BaseSchema


class ItemBase(BaseSchema):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    board_id: int
    is_complete: int

    class Config:
        orm_mode = True
