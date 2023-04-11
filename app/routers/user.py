from fastapi import APIRouter, Body

from app.models.model import UserLoginSchema, UserSchema
from app.auth.auth_handler import signJWT

router = APIRouter()

users = []

# print('\n\nuser\n\n')


@router.post("/signup")
async def create_user(user: UserSchema = Body(...)):
    users.append(user)  # replace with db call, making sure to
    #  hash the password first
    return signJWT(user.email)


@router.post("/login")
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }


def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False
