# app/api.py

from fastapi import FastAPI

from app.routers import root_way, posts, user
from app.routers.manual import security, user_manual

app = FastAPI()

app.include_router(
    user_manual.router, prefix='/users', tags=['users'])
app.include_router(
    security.router, prefix='/security', tags=['security'])
app.include_router(root_way.router, tags=['root'])
app.include_router(posts.router, prefix='/posts', tags=['posts'])
app.include_router(user.router, prefix='/user', tags=['user'])
