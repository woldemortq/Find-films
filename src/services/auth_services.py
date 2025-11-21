from core.security import create_access_token
from repositories.user_repository import *


async def register_user(username: str, password: str):
    user = create_user(username, password)
    return user

async def login_user(username: str, password: str, db):
    user = await get_user(username, db)
    if not user:
        return None
    token = create_access_token(user.id)
    return token