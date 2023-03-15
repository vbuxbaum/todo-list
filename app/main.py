from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core import login_service
from app.infrastructure.database import SessionLocal
from app.infrastructure.repositories import UserRepo
from app.routes import boards_route, users_route, current_user, get_db
from app.schemas import user_schema

app = FastAPI(
    title=get_settings().app_name,
    description="A simple to-do list API for studying purposes",
)

app.include_router(users_route.route)
app.include_router(boards_route.route)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def health_check():
    return """
    <html>
        <body>
            <h1>Everything is ok! <a href="/docs">Go to documentation</a></h1>
        </body>
    </html>
    """


@app.post("/token", include_in_schema=False)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = user_schema.UserCreate(
        email=form_data.username, password=form_data.password
    )
    try:
        login_service.validate_user(UserRepo(db), user)
    except LookupError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.args[0]) from e
    except PermissionError as e:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, detail=e.args[0]
        ) from e

    return {
        "access_token": login_service.create_access_token(user.email),
        "token_type": "bearer",
    }


# dangerous operations below


@app.delete("/users/", tags=["DANGEROUS"], )
def delete_all_users(
    db: SessionLocal = Depends(get_db),
    _: str = Depends(current_user),
):
    return {"deleted_users": UserRepo(db).delete_all()}
