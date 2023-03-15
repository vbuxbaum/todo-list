from app.infrastructure.encrypt_utils import encrypt_str
from app.infrastructure.repositories import UserRepo
from app.schemas import user_schema


def create_new_user(db: UserRepo, user: user_schema.UserCreate):
    if db.get_by_email(user.email):
        raise ValueError(f"User with email '{user.email}' already exists")

    user_dict = user.dict()
    user_dict["hashed_password"] = encrypt_str(user.password)
    del user_dict["password"]

    return db.create(user_dict)


def get_user_by_id(db: UserRepo, id: int):
    if (db_user := db.get_by_id(id)) is None:
        raise LookupError(f"User not found for given id: {id}")

    return db_user
