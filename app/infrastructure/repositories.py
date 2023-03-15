from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.infrastructure import models


class BaseRepo(ABC):
    @abstractmethod
    def __init__(self, session_db: Session, model: models.Base) -> None:
        self.db = session_db
        self.model = model

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.scalars(
            select(self.model).offset(skip).limit(limit)
        ).all()

    def get_by_id(self, id: int):
        return self.db.scalar(select(self.model).where(self.model.id == id))

    def create(self, entity: dict):
        db_entity = self.model(**entity)

        self.db.add(db_entity)
        self.db.commit()
        self.db.refresh(db_entity)
        return db_entity

    def update(self, id: int, partial_entity: dict):
        db_entity = self.get_by_id(id)
        for key, value in partial_entity.items():
            db_entity.__setattr__(key, value)

        self.db.add(db_entity)
        self.db.commit()
        self.db.refresh(db_entity)
        return db_entity

    def delete_by_id(self, id: int):
        db_entity = self.get_by_id(id)
        self.db.delete(db_entity)
        self.db.commit()
        return db_entity

    def delete_all(self):
        return [self.delete_by_id(entity.id) for entity in self.get_all()]


class UserRepo(BaseRepo):
    def __init__(self, session_db: Session) -> None:
        super().__init__(session_db=session_db, model=models.User)

    def get_by_email(self, email: str):
        return self.db.scalar(
            select(models.User).where(models.User.email == email)
        )


class BoardRepo(BaseRepo):
    def __init__(self, session_db: Session) -> None:
        super().__init__(session_db=session_db, model=models.Board)

    def get_all_by_owner_id(
        self, owner_id: int, skip: int = 0, limit: int = 100
    ):
        return self.db.scalars(
            select(models.Board)
            .where(models.Board.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        ).all()

    def create(self, board: dict, user_id: int):
        board["owner_id"] = user_id
        return super().create(board)


class ItemRepo(BaseRepo):
    def __init__(self, session_db: Session) -> None:
        super().__init__(session_db=session_db, model=models.Item)

    def get_all_by_board_id(
        self, board_id: int, skip: int = 0, limit: int = 100
    ):
        return self.db.scalars(
            select(models.Item)
            .where(models.Item.board_id == board_id)
            .offset(skip)
            .limit(limit)
        ).all()

    def create(self, item: dict, board_id: int):
        item["board_id"] = board_id
        return super().create(item)
