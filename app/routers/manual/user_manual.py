from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer

from app.models.user_model import User


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


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


@router.get("/me")
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
