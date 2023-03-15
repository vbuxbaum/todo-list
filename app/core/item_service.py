from app.infrastructure.repositories import ItemRepo
from app.schemas import item_schema


def create_new_item(
    db: ItemRepo,
    item: item_schema.ItemCreate,
    board_id: int,
):
    return db.create(item.dict(), board_id)
