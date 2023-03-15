from datetime import datetime, timedelta

from jose import JWTError, jwt

from app.config import get_settings
from app.infrastructure.encrypt_utils import check_encrypted_str
from app.infrastructure.repositories import UserRepo
from app.schemas import user_schema

from datetime import timezone
SECRET_KEY = get_settings().jwt_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def validate_user(db: UserRepo, user: user_schema.UserCreate):
    if (db_user := db.get_by_email(user.email)) is None:
        raise LookupError(f"User not found for given email: '{user.email}'")

    if not check_encrypted_str(user.password, db_user.hashed_password):
        raise PermissionError(
            f"Incorrect password for given email: '{user.email}'"
        )
    return db_user


def create_access_token(user_email: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {
        "sub": user_email,
        "exp": expire,
    }

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(db: UserRepo, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise ValueError(f"Invalid JWT signature: {e.args[0]}") from e

    if (user_email := payload.get("sub")) is None:
        raise ValueError("Token missing 'sub' attribute")

    if (user := db.get_by_email(user_email)) is None:
        raise LookupError(f"User not found for given email: {user_email}")

    return user
