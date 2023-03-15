from fastapi import Depends, HTTPException, status
from app.core import login_service
from app.infrastructure.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer

from app.infrastructure.repositories import UserRepo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def current_user(
    db: SessionLocal = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    try:
        return login_service.get_current_user(UserRepo(db), token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.args[0],
            headers={"WWW-Authenticate": "Bearer"},
        )
