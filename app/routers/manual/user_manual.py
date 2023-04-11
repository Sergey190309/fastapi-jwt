from typing import Annotated

from fastapi import (
    Depends, APIRouter, HTTPException,
    # status
    )
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.models.user_model import (
    User, UserInDB, mock_users_db,
    mock_hash_password
    )

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded",
        mail="john@example.com",
        full_name="John Doe"
    )


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = mock_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = mock_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/me")
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
