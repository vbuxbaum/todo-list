from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core import board_service, item_service
from app.infrastructure.repositories import BoardRepo, ItemRepo
from app.routes import get_db, current_user
from app.schemas import board_schema, item_schema, user_schema

route = APIRouter(prefix="/boards", tags=["Boards"])


@route.get("/", response_model=list[board_schema.Board])
def get_boards(
    db: Session = Depends(get_db),
    user: user_schema.User = Depends(current_user),
):
    return board_service.get_boards_by_owner_id(BoardRepo(db), user.id)


@route.get("/{id}", response_model=board_schema.Board)
def get_board(
    id: int = Path(gt=0, description="board id"),
    user: user_schema.User = Depends(current_user),
    db: Session = Depends(get_db),
):
    try:
        return board_service.get_board_by_id(BoardRepo(db), id, user.id)
    except LookupError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.args[0])


@route.post("/", response_model=board_schema.Board)
def create_board(
    board: board_schema.BoardCreate,
    user: user_schema.User = Depends(current_user),
    db: Session = Depends(get_db),
):
    try:
        return board_service.create_new_board(BoardRepo(db), board, user.id)
    except LookupError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.args[0])


@route.post("/{id}/items", response_model=item_schema.Item, tags=["Items"])
def create_board_item(
    item: item_schema.ItemCreate,
    id: int = Path(gt=0, description="board id"),
    user: user_schema.User = Depends(current_user),
    db: Session = Depends(get_db),
):
    try:
        board_service.get_board_by_id(BoardRepo(db), id, user.id)
    except LookupError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.args[0])

    return item_service.create_new_item(ItemRepo(db), item, board_id=id)


@route.delete("/{id}", response_model=board_schema.Board)
def delete_board(
    id: int = Path(gt=0, description="board id"),
    user: user_schema.User = Depends(current_user),
    db: Session = Depends(get_db),
):
    try:
        return board_service.delete_board(BoardRepo(db), id, user.id)
    except LookupError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.args[0])


@route.patch("/{id}", response_model=board_schema.Board)
def update_board(
    board: board_schema.BoardBase,
    id: int = Path(gt=0, description="board id"),
    user: user_schema.User = Depends(current_user),
    db: Session = Depends(get_db),
):
    try:
        return board_service.update_board(BoardRepo(db), id, board, user.id)
    except LookupError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.args[0])
