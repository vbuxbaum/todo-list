from app.infrastructure.repositories import BoardRepo
from app.schemas import board_schema


def get_board_by_id(db: BoardRepo, id: int, owner_id: int):
    if (db_board := db.get_by_id(id)) is None or (
        db_board.owner_id != owner_id
    ):
        raise LookupError(f"Board not found for given id: {id}")

    return db_board


def get_boards_by_owner_id(db: BoardRepo, owner_id: int):
    if (db_board := db.get_all_by_owner_id(owner_id)) is None:
        raise LookupError(f"Board not found for given id: {id}")

    return db_board


def create_new_board(
    db: BoardRepo,
    board: board_schema.BoardCreate,
    owner_id: int,
):
    return db.create(board.dict(), owner_id)


def update_board(
    db: BoardRepo,
    id: int,
    board: board_schema.BoardCreate,
    owner_id: int,
):
    get_board_by_id(db, id, owner_id)

    return db.update(id, board.dict(exclude_unset=True))


def delete_board(
    db: BoardRepo,
    id: int,
    owner_id: int,
):
    get_board_by_id(db, id, owner_id)

    return db.delete_by_id(id)
